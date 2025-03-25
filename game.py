import pygame
import sys
import pytmx

# Initialize Pygame
pygame.init()

# Set up the display (screen resolution)
width, height = 960, 640
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Character Movement with Boundaries and Camera")

# Zoom factor and camera view dimensions (world view size)
zoom = 2.0
view_width, view_height = int(width / zoom), int(height / zoom)

# Function to load collision rectangles from a Tiled map file
def load_collision_rects(tmx_file):
    tmx_data = pytmx.TiledMap(tmx_file)
    collision_rects = []
    for obj in tmx_data.objects:
        # Check if the object is marked as a collision area (by name or property)
        if obj.name == "Collision":
            rect = pygame.Rect(obj.x, obj.y, obj.width, obj.height)
            collision_rects.append(rect)
    return collision_rects

# Load collision data from Tiled maps for each scene
collision_rects_scene1 = load_collision_rects("assets/maps/Main.tmx")
collision_rects_scene2 = load_collision_rects("assets/maps/Saloon.tmx")

# Load the background images for each scene.
# These images represent the full world.
background1 = pygame.image.load("assets/images/Main-Background.png")
background2 = pygame.image.load("assets/images/saloon-background.png")

# For initial world dimensions, assume scene 1's background defines the world size.
world_width, world_height = background1.get_width(), background1.get_height()

# Load the character image and scale it down (50% of original size)
character_original = pygame.image.load("assets/images/main-character.png")
character = pygame.transform.scale(character_original, (character_original.get_width() // 2, character_original.get_height() // 2))
character_rect = character.get_rect()
# Place the character initially at the center of the scene 1 world
character_rect.center = (world_width // 2, world_height // 2)

# Movement speed in world coordinates
speed = 2

clock = pygame.time.Clock()

# Track the current scene (1 or 2)
current_scene = 1

running = True
while running:
    clock.tick(60)  # Cap the frame rate to 60 FPS
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Save old position in case of collision
    old_x, old_y = character_rect.x, character_rect.y

    # Process keyboard input (movement in world coordinates)
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        character_rect.y -= speed
    if keys[pygame.K_s]:
        character_rect.y += speed
    if keys[pygame.K_a]:
        character_rect.x -= speed
    if keys[pygame.K_d]:
        character_rect.x += speed

    # Clamp character within world boundaries
    if character_rect.left < 0:
        character_rect.left = 0
    if character_rect.right > world_width:
        character_rect.right = world_width
    if character_rect.top < 0:
        character_rect.top = 0
    if character_rect.bottom > world_height:
        character_rect.bottom = world_height

    # Determine current scene's collision rectangles and world/background
    if current_scene == 1:
        collision_rects = collision_rects_scene1
        world = background1
        world_width, world_height = background1.get_width(), background1.get_height()
    elif current_scene == 2:
        collision_rects = collision_rects_scene2
        world = background2
        world_width, world_height = background2.get_width(), background2.get_height()
    else:
        collision_rects = []
        world = background1

    # Check for collisions with boundaries from Tiled
    for rect in collision_rects:
        if character_rect.colliderect(rect):
            # On collision, revert to the previous position
            character_rect.x, character_rect.y = old_x, old_y
            break

    # Scene transition example:
    # In scene 1, if the character enters a specific zone, switch to scene 2.
    transition_zone = pygame.Rect(846, 0, 160, 624)  # Adjust these coordinates as needed
    if current_scene == 1 and character_rect.colliderect(transition_zone):
        current_scene = 2
        # Set the character's starting position in scene 2 (adjust as desired)
        character_rect.center = (100, 200)

    # --- Camera Implementation ---
    # Compute the camera's top-left so that the view is centered on the character.
    camera_x = character_rect.centerx - view_width // 2
    camera_y = character_rect.centery - view_height // 2

    # Clamp the camera to the world boundaries
    if camera_x < 0:
        camera_x = 0
    if camera_y < 0:
        camera_y = 0
    if camera_x + view_width > world_width:
        camera_x = world_width - view_width
    if camera_y + view_height > world_height:
        camera_y = world_height - view_height

    # Create a temporary camera surface (the "view" of the world)
    camera_surface = pygame.Surface((view_width, view_height))
    
    # Draw the world (background) on the camera surface, offset by the camera position
    camera_surface.blit(world, (-camera_x, -camera_y))

    # Draw the character on the camera surface (using its world coordinates)
    char_draw_x = character_rect.x - camera_x
    char_draw_y = character_rect.y - camera_y
    camera_surface.blit(character, (char_draw_x, char_draw_y))
    
    # Scale the camera surface up to the screen size (this creates the zoom effect)
    final_surface = pygame.transform.scale(camera_surface, (width, height))
    screen.blit(final_surface, (0, 0))
    
    pygame.display.flip()

pygame.quit()
sys.exit()
