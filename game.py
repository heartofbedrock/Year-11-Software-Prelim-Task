import pygame
import sys
import pytmx

# Initialize Pygame
pygame.init()

# Set up the display
width, height = 960, 640
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Character Movement with Boundaries")

# Function to load collision rectangles from a Tiled map file
def load_collision_rects(tmx_file):
    tmx_data = pytmx.TiledMap(tmx_file)
    collision_rects = []
    for obj in tmx_data.objects:
        # You can either check the object name or a custom property (e.g., obj.properties.get("collidable"))
        if obj.name == "Collision":
            rect = pygame.Rect(obj.x, obj.y, obj.width, obj.height)
            collision_rects.append(rect)
    return collision_rects

# Load collision data from Tiled maps for each scene
collision_rects_scene1 = load_collision_rects("assets/maps/Main.tmx")
collision_rects_scene2 = load_collision_rects("assets/maps/Saloon.tmx")

# Load and scale the background images (for visual purposes)
background1 = pygame.image.load("assets/images/Main-Background.png")
background1 = pygame.transform.scale(background1, (width, height))
background2 = pygame.image.load("assets/images/saloon-background.png")
background2 = pygame.transform.scale(background2, (width, height))

# Load the character image and set its starting position
character = pygame.image.load("assets/images/main-character.png")
character_rect = character.get_rect()
character_rect.center = (width // 2, height // 2)

# Movement speed of the character
speed = 2

clock = pygame.time.Clock()

# Variable to track the current scene (1 or 2)
current_scene = 1

running = True
while running:
    clock.tick(60)  # Cap the frame rate to 60 FPS
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Store the old position in case we need to revert
    old_x, old_y = character_rect.x, character_rect.y

    # Get keyboard input for movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        character_rect.y -= speed  # Move up
    if keys[pygame.K_s]:
        character_rect.y += speed  # Move down
    if keys[pygame.K_a]:
        character_rect.x -= speed  # Move left
    if keys[pygame.K_d]:
        character_rect.x += speed  # Move right

    # Prevent the character from moving off the screen
    if character_rect.top < 0:
        character_rect.top = 0
    if character_rect.bottom > height:
        character_rect.bottom = height
    if character_rect.left < 0:
        character_rect.left = 0
    if character_rect.right > width:
        character_rect.right = width

    # Get the current scene's collision rectangles
    if current_scene == 1:
        collision_rects = collision_rects_scene1
    elif current_scene == 2:
        collision_rects = collision_rects_scene2
    else:
        collision_rects = []

    

    # Check collision with each boundary rectangle
    for rect in collision_rects:
        if character_rect.colliderect(rect):
            # Collision detected, revert to the previous position
            character_rect.x, character_rect.y = old_x, old_y
            break

    # Scene transition example: in scene 1, if the character enters the right edge zone, switch to scene 2
    transition_zone = pygame.Rect(800, 0, 160, 640)
    if current_scene == 1 and character_rect.colliderect(transition_zone):
        current_scene = 2
        character_rect.center = (width // 2, height // 2)  # Reset character position

    # Draw the current scene's background
    if current_scene == 1:
        screen.blit(background1, (0, 0))
    elif current_scene == 2:
        screen.blit(background2, (0, 0))

    # Draw the character
    screen.blit(character, character_rect)

    # Update the display
    pygame.display.flip()

pygame.quit()
sys.exit()
