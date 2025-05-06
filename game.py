# This is a simple 2D game using Pygame and Tiled maps.
# The game features a character that can move around a world, with collision detection and scene transitions.
# The game also includes a minimap that shows the player's position in the world.   
# The game uses Tiled maps to define the world and collision areas, and Pygame to handle graphics and input.

# Import necessary libraries
import pygame
import sys
import pytmx

# Initialize Pygame
pygame.init()

# Set up the display (screen resolution)
width, height = 960, 640
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Defenitly not Stardew Valley")

# Zoom factor and camera view dimensions (world view size)
zoom = 2.0
view_width, view_height = int(width / zoom), int(height / zoom)

# Function to load collision rectangles from a Tiled map file
def load_collision_rects(tmx_file):
    tmx_data = pytmx.TiledMap(tmx_file)
    collision_rects = []
    for obj in tmx_data.objects:
        if obj.name == "Collision":
            rect = pygame.Rect(obj.x, obj.y, obj.width, obj.height)
            collision_rects.append(rect)
    return collision_rects

# Function to get an object's rectangle by its name from a Tiled map file
def get_object_rect(tmx_file, object_name):
    tmx_data = pytmx.TiledMap(tmx_file)
    for obj in tmx_data.objects:
        if obj.name == object_name:
            return pygame.Rect(obj.x, obj.y, obj.width, obj.height)
    return None

# Load collision data from Tiled maps for each scene
collision_rects_scene1 = load_collision_rects("assets/maps/Main.tmx")
collision_rects_scene2 = load_collision_rects("assets/maps/Saloon.tmx")

# Load the transition zone (entrance_saloon) from the Main map
entrance_saloon_rect = get_object_rect("assets/maps/Main.tmx", "entrance_saloon")

# Load the background images for each scene.
background1 = pygame.image.load("assets/images/Main-Background.png")
background2 = pygame.image.load("assets/images/saloon-background.png")

# Use scene 1's background to determine the world dimensions initially.
world_width, world_height = background1.get_width(), background1.get_height()

# Load the character image and scale it down.
character_original = pygame.image.load("assets/images/main-character.png")
character = pygame.transform.scale(
    character_original, (character_original.get_width() // 2, character_original.get_height() // 2)
)
character_rect = character.get_rect()
character_rect.center = (world_width // 2, world_height // 2)

# Movement speed in world coordinates
speed = 2

clock = pygame.time.Clock()

# Track the current scene (1 or 2)
current_scene = 1

def fade(screen, fade_in=True, duration=500):
    fade_surface = pygame.Surface(screen.get_size())
    fade_surface.fill((0, 0, 0))
    fade_clock = pygame.time.Clock()
    start_time = pygame.time.get_ticks()
    
    while True:
        elapsed = pygame.time.get_ticks() - start_time
        if elapsed >= duration:
            break
        # Calculate alpha: rising for fade-out, falling for fade-in.
        if fade_in:
            alpha = int(255 * (elapsed / duration))
        else:
            alpha = 255 - int(255 * (elapsed / duration))
        fade_surface.set_alpha(alpha)
        
        # Draw the current screen (assumes the scene is already drawn) and apply the fade overlay
        screen.blit(fade_surface, (0, 0))
        pygame.display.flip()
        fade_clock.tick(60)

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
            character_rect.x, character_rect.y = old_x, old_y
            break

    # Scene transition: if in scene 1 and colliding with the 'entrance_saloon' zone, trigger transition
    if current_scene == 1 and entrance_saloon_rect is not None and character_rect.colliderect(entrance_saloon_rect):
        fade(screen, fade_in=True, duration=500)  # Fade out
        current_scene = 2
        Spawnpoint_saloon_rect = get_object_rect("assets/maps/Saloon.tmx", "Spawnpoint")
        character_rect.center = Spawnpoint_saloon_rect.center
        fade(screen, fade_in=False, duration=500)  # Fade in

    # --- Camera Implementation ---
    camera_x = character_rect.centerx - view_width // 2
    camera_y = character_rect.centery - view_height // 2

    if camera_x < 0:
        camera_x = 0
    if camera_y < 0:
        camera_y = 0
    if camera_x + view_width > world_width:
        camera_x = world_width - view_width
    if camera_y + view_height > world_height:
        camera_y = world_height - view_height

    camera_surface = pygame.Surface((view_width, view_height))
    camera_surface.blit(world, (-camera_x, -camera_y))

    char_draw_x = character_rect.x - camera_x
    char_draw_y = character_rect.y - camera_y
    camera_surface.blit(character, (char_draw_x, char_draw_y))
    
    final_surface = pygame.transform.scale(camera_surface, (width, height))
    screen.blit(final_surface, (0, 0))

  # --- Minimap implementation ---
    minimap_width, minimap_height = width // 4.5, height // 4.5

    # 1. Shrink the full world to minimap dimensions:
    minimap_surface = pygame.transform.scale(world, (minimap_width, minimap_height))

    # 2. Compute the player's dot position on the minimap:
    #    (character_rect.x is world‐space; world_width/world_height from the current scene)
    dot_x = int(character_rect.x / world_width * minimap_width)
    dot_y = int(character_rect.y / world_height * minimap_height)

    # 3. Draw a small red square (5×5 pixels) at that position:
    pygame.draw.rect(minimap_surface, (255, 0, 0), (dot_x, dot_y, 5, 5))

    # 4. Optional: draw a border around the minimap
    border_rect = pygame.Rect(10, 10, minimap_width, minimap_height)
    pygame.draw.rect(screen, (255, 255, 255), border_rect, 2)

    # 5. Blit to the top‐left of the screen
    screen.blit(minimap_surface, (10, 10))
    pygame.display.flip()

pygame.quit()
sys.exit()
