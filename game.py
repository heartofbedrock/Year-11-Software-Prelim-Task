import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up the display
width, height = 960, 640
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Basic Character Movement")

# Load and scale the background image
background = pygame.image.load("assets\images\Main-Background.png")
background = pygame.transform.scale(background, (width, height))

# Load the character image and set its starting position
character = pygame.image.load("assets\images\main-character.png")
character_rect = character.get_rect()
character_rect.center = (width // 2, height // 2)

# Movement speed of the character
speed = 2

clock = pygame.time.Clock()

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

    # Draw the background and the character on the screen
    screen.blit(background, (0, 0))
    screen.blit(character, character_rect)

    pygame.display.flip()  # Update the display

pygame.quit()
sys.exit()
