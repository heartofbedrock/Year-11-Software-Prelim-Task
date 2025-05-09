# game.py
import pygame
import sys
import pytmx

# --- Initialization ---
pygame.init()
width, height = 960, 640
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Definitely not Stardew Valley")
clock = pygame.time.Clock()

# --- Load Animation Frames ---
walk_down = [
    pygame.image.load("assets/character/image1x1.png").convert_alpha(),
    pygame.image.load("assets/character/image2x1.png").convert_alpha(),
    pygame.image.load("assets/character/image3x1.png").convert_alpha(),
    pygame.image.load("assets/character/image4x1.png").convert_alpha(),
]
walk_right = [
    pygame.image.load("assets/character/image1x2.png").convert_alpha(),
    pygame.image.load("assets/character/image2x2.png").convert_alpha(),
    pygame.image.load("assets/character/image3x2.png").convert_alpha(),
    pygame.image.load("assets/character/image4x2.png").convert_alpha(),
]
walk_up = [
    pygame.image.load("assets/character/image1x3.png").convert_alpha(),
    pygame.image.load("assets/character/image2x3.png").convert_alpha(),
    pygame.image.load("assets/character/image3x3.png").convert_alpha(),
    pygame.image.load("assets/character/image4x3.png").convert_alpha(),
]
walk_left = [
    pygame.image.load("assets/character/image1x4.png").convert_alpha(),
    pygame.image.load("assets/character/image2x4.png").convert_alpha(),
    pygame.image.load("assets/character/image3x4.png").convert_alpha(),
    pygame.image.load("assets/character/image4x4.png").convert_alpha(),
]
animations = {
    "down":  walk_down,
    "right": walk_right,
    "up":    walk_up,
    "left":  walk_left,
}

# --- View & Camera Setup ---
zoom = 2.0
view_width, view_height = int(width / zoom), int(height / zoom)

# --- Tiled Utility Functions ---
def load_collision_rects(tmx_file):
    tmx = pytmx.TiledMap(tmx_file)
    rects = []
    for obj in tmx.objects:
        if obj.name == "Collision":
            rects.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))
    return rects

def get_object_rect(tmx_file, name):
    tmx = pytmx.TiledMap(tmx_file)
    for obj in tmx.objects:
        if obj.name.lower() == name.lower():
            return pygame.Rect(obj.x, obj.y, obj.width, obj.height)
    return None

# --- Load Maps, Collision & Zones ---
collision_scene1 = load_collision_rects("assets/maps/Main.tmx")
collision_scene2 = load_collision_rects("assets/maps/Salon.tmx")
entrance_Salon = get_object_rect("assets/maps/Main.tmx", "entrance_saloon")
exit_Salon     = get_object_rect("assets/maps/Salon.tmx", "Exit")

# --- Load Backgrounds ---
bg1 = pygame.image.load("assets/images/Main-Background.png").convert()
bg2 = pygame.image.load("assets/images/Salon.png").convert()

# --- Quest & Objects ---
quest_started = False
has_carrot    = False
npc_rect   = get_object_rect("assets/maps/Salon.tmx", "NPC")
carrot_rect = get_object_rect("assets/maps/Main.tmx",  "carrot")

# --- Movement & Animation State ---
speed = 2
current_scene = 1

# Start with the down–idle frame
direction     = "down"
frame_index   = 1            # middle frame = idle
last_update   = pygame.time.get_ticks()
frame_duration = 200         # ms between frames

# Character rect & image
character = animations[direction][frame_index]
character_rect = character.get_rect(center=(bg1.get_width()//1.8, bg1.get_height()//1.8))

# --- Helper Functions ---
def show_dialog(screen, text, w=400, h=100):
    font = pygame.font.SysFont(None, 24)
    box = pygame.Surface((w, h))
    box.set_alpha(200)
    box.fill((30,30,30))
    txt = font.render(text, True, (255,255,255))
    tr = txt.get_rect(center=(w//2, h//2))
    pos = ((screen.get_width()-w)//2, (screen.get_height()-h)//2)
    waiting = True
    while waiting:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if e.type == pygame.KEYDOWN and e.key == pygame.K_SPACE:
                waiting = False
        screen.blit(box, pos)
        screen.blit(txt, (pos[0]+tr.x, pos[1]+tr.y))
        pygame.display.flip()
        clock.tick(30)

def fade(screen, fade_in=True, duration=500):
    overlay = pygame.Surface(screen.get_size())
    overlay.fill((0,0,0))
    start = pygame.time.get_ticks()
    while True:
        elapsed = pygame.time.get_ticks() - start
        if elapsed >= duration:
            break
        alpha = int(255 * (elapsed/duration)) if fade_in else 255 - int(255*(elapsed/duration))
        overlay.set_alpha(alpha)
        screen.blit(overlay, (0,0))
        pygame.display.flip()
        clock.tick(60)

# --- Main Loop ---
running = True
while running:
    clock.tick(60)
    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            running = False

    # Save old pos for collision check
    old_x, old_y = character_rect.x, character_rect.y

    # Handle input & set direction
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        character_rect.y -= speed; direction = "up"
    if keys[pygame.K_s]:
        character_rect.y += speed; direction = "down"
    if keys[pygame.K_a]:
        character_rect.x -= speed; direction = "left"
    if keys[pygame.K_d]:
        character_rect.x += speed; direction = "right"

    # Clamp to world bounds (use current background’s size)
    world = bg1 if current_scene==1 else bg2
    wW, wH = world.get_width(), world.get_height()
    character_rect.clamp_ip(pygame.Rect(0,0,wW,wH))

    # Check collisions
    coll_list = collision_scene1 if current_scene==1 else collision_scene2
    for cr in coll_list:
        if character_rect.colliderect(cr):
            character_rect.x, character_rect.y = old_x, old_y
            break

    # Scene transitions
    if current_scene==1 and entrance_Salon and character_rect.colliderect(entrance_Salon):
        fade(screen, True)
        current_scene = 2
        spawn = get_object_rect("assets/maps/Salon.tmx","Spawn")
        character_rect.center = spawn.center
        fade(screen, False)
    if current_scene==2 and exit_Salon and character_rect.colliderect(exit_Salon):
        fade(screen, True)
        current_scene = 1
        spawn = get_object_rect("assets/maps/Main.tmx","exit_saloon")
        character_rect.center = spawn.center
        fade(screen, False)

    # Quest logic
    if current_scene==2 and not quest_started and npc_rect and character_rect.colliderect(npc_rect):
        show_dialog(screen, "NPC: Hey! Can you get me a carrot from the farm?")
        quest_started = True

    if current_scene==1 and quest_started and not has_carrot and carrot_rect and character_rect.colliderect(carrot_rect):
        show_dialog(screen, "You picked up the carrot!")
        has_carrot = True
        carrot_rect = None

    if current_scene==2 and quest_started and has_carrot and npc_rect and character_rect.colliderect(npc_rect):
        show_dialog(screen, "NPC: Thank you! Quest complete.")
        quest_started = False
        has_carrot   = False

    # --- Animation Update ---
    moved = (character_rect.x != old_x or character_rect.y != old_y)
    now = pygame.time.get_ticks()
    if moved:
        if now - last_update > frame_duration:
            frame_index = (frame_index + 1) % len(animations[direction])
            last_update = now
    else:
        frame_index = 1  # idle frame

    character = animations[direction][frame_index]

    # --- Camera & Drawing ---
    cam_x = character_rect.centerx - view_width//2
    cam_y = character_rect.centery - view_height//2
    cam_x = max(0, min(cam_x, wW - view_width))
    cam_y = max(0, min(cam_y, wH - view_height))

    cam_surf = pygame.Surface((view_width, view_height))
    cam_surf.blit(world, (-cam_x, -cam_y))
    cam_surf.blit(character, (character_rect.x - cam_x, character_rect.y - cam_y))

    final = pygame.transform.scale(cam_surf, (width, height))
    screen.blit(final, (0,0))

    # --- Minimap ---
    mm_w, mm_h = width//4.5, height//4.5
    mm = pygame.transform.scale(world, (mm_w, mm_h))
    dot_x = int(character_rect.x / wW * mm_w)
    dot_y = int(character_rect.y / wH * mm_h)
    pygame.draw.rect(mm, (255,0,0), (dot_x, dot_y, 5,5))
    pygame.draw.rect(screen, (255,255,255), (10,10,mm_w,mm_h), 2)
    screen.blit(mm, (10,10))

    pygame.display.flip()

pygame.quit()
sys.exit()
