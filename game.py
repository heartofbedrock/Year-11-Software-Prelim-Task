import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up the display
width, height = 960, 640
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Basic Character Movement")

# Load and scale the background images
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

# Variable to track the current scene
current_scene = 1

running = True
while running:
    clock.tick(60)  # Cap the frame rate to 60 FPS
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Get the current state of all keyboard buttons
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
    if character_rect.top <= 0:
        character_rect.top = 0
    if character_rect.bottom >= height:
        character_rect.bottom = height
    if character_rect.left <= 0:
        character_rect.left = 0
    if character_rect.right >= width:
        character_rect.right = width

    # Check if the character reaches a specific point to switch scenes
    if current_scene == 1 and character_rect.colliderect(pygame.Rect(800, 0, 160, 640)):
        current_scene = 2
        character_rect.center = (width // 2, height // 2)  # Reset character position

    # Draw the appropriate background and the character on the screen
    if current_scene == 1:
        screen.blit(background1, (0, 0))
    elif current_scene == 2:
        screen.blit(background2, (0, 0))

    screen.blit(character, character_rect)

    pygame.display.flip()  # Update the display

pygame.quit()
sys.exit()
