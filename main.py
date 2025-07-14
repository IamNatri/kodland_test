import pgzrun
import math
import random
import os
from pygame import Rect
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Game constants from .env
WIDTH = int(os.getenv('GAME_WIDTH', 800))
HEIGHT = int(os.getenv('GAME_HEIGHT', 600))
GRAVITY = float(os.getenv('GRAVITY', 0.5))
JUMP_SPEED = int(os.getenv('JUMP_SPEED', 12))
PLAYER_SPEED = int(os.getenv('PLAYER_SPEED', 3))
ENEMY_SPEED = int(os.getenv('ENEMY_SPEED', 1))
PLATFORM_WIDTH = int(os.getenv('PLATFORM_WIDTH', 150))
PLATFORM_HEIGHT = int(os.getenv('PLATFORM_HEIGHT', 20))
STAIR_VERTICAL_GAP = int(os.getenv('STAIR_VERTICAL_GAP', 80))
STAIR_HORIZONTAL_GAP = int(os.getenv('STAIR_HORIZONTAL_GAP', 120))
ZIGZAG_PLATFORMS = int(os.getenv('ZIGZAG_PLATFORMS', 6))
MUSIC_VOLUME = float(os.getenv('MUSIC_VOLUME', 0.5))
SCORE_MULTIPLIER = int(os.getenv('SCORE_MULTIPLIER', 50))
ENEMY_SPAWN_CHANCE = float(os.getenv('ENEMY_SPAWN_CHANCE', 0.15))
PLATFORMS_GENERATED_AHEAD = int(os.getenv('PLATFORMS_GENERATED_AHEAD', 8))
INITIAL_PLATFORMS = int(os.getenv('INITIAL_PLATFORMS', 20))

# Game state
game_state = "menu"
music_enabled = os.getenv('MUSIC_ENABLED', 'true').lower() == 'true'
sounds_enabled = os.getenv('SOUNDS_ENABLED', 'true').lower() == 'true'
camera_y = score = highest_platform = last_platform_y = platforms_in_direction = 0
last_platform_x = 50
going_right = True
game_over = False

class Animation:
    def __init__(self, images, speed=0.15):
        self.images, self.speed, self.frame, self.timer = images, speed, 0, 0
        
    def update(self, dt):
        self.timer += dt
        if self.timer >= self.speed:
            self.frame = (self.frame + 1) % len(self.images)
            self.timer = 0
    
    def get_current_image(self):
        return self.images[self.frame]

class Player:
    def __init__(self, x, y):
        self.x, self.y, self.width, self.height = x, y, 32, 48
        self.velocity_x = self.velocity_y = 0
        self.on_ground = self.facing_right = False
        self.idle_anim = Animation(['player_idle1', 'player_idle2'], 0.5)
        self.walk_anim = Animation(['player_walk1', 'player_walk2', 'player_walk3'], 0.2)
        self.jump_anim = Animation(['player_jump'], 1.0)
        self.current_anim = self.idle_anim
        
    def update(self, dt):
        global camera_y, score, highest_platform
        
        # Input handling
        self.velocity_x = 0
        if keyboard.left:
            self.velocity_x, self.facing_right = -PLAYER_SPEED, False
            if self.on_ground: self.current_anim = self.walk_anim
        elif keyboard.right:
            self.velocity_x, self.facing_right = PLAYER_SPEED, True
            if self.on_ground: self.current_anim = self.walk_anim
        else:
            if self.on_ground: self.current_anim = self.idle_anim
                
        if keyboard.space and self.on_ground:
            self.velocity_y, self.on_ground = -JUMP_SPEED, False
            self.current_anim = self.jump_anim
            if sounds_enabled:
                try: sounds.jump.play()
                except: pass
        
        # Physics
        self.velocity_y += GRAVITY
        self.x += self.velocity_x
        self.y += self.velocity_y
        
        # Collision & boundaries
        self.check_platform_collisions()
        self.x = max(0, min(WIDTH - self.width, self.x))
        
        # Death check
        if self.y > camera_y + HEIGHT + 100:
            self.die()
            
        # Camera & scoring
        target_camera_y = self.y - HEIGHT + 200
        if target_camera_y < camera_y:
            camera_y = target_camera_y
            new_score = int(abs(camera_y) / SCORE_MULTIPLIER)
            if new_score > score:
                score = new_score
                highest_platform = max(highest_platform, score)
                generate_platforms_ahead()
            
        self.current_anim.update(dt)
        
    def check_platform_collisions(self):
        player_rect = Rect(self.x, self.y, self.width, self.height)
        self.on_ground = False
        
        for platform in platforms:
            if player_rect.colliderect(platform):
                if self.velocity_y > 0 and self.y < platform.y:
                    self.y = platform.y - self.height
                    self.velocity_y = 0
                    self.on_ground = True
                elif self.velocity_y < 0 and self.y > platform.y:
                    self.y = platform.y + platform.height
                    self.velocity_y = 0
                    
    def reset_position(self):
        global camera_y, score, highest_platform, platforms_in_direction, going_right, last_platform_x, last_platform_y
        self.x, self.y = 100, 500
        self.velocity_x = self.velocity_y = 0
        camera_y = score = platforms_in_direction = 0
        last_platform_y = 580
        going_right = True
        last_platform_x = 50
        generate_platforms()
        
    def die(self):
        global game_over
        game_over = True
        if sounds_enabled:
            try: sounds.hit.play()
            except: pass
        self.reset_position()
        
    def draw(self):
        screen.blit(self.current_anim.get_current_image(), (self.x, self.y))

class Enemy:
    def __init__(self, x, y, patrol_start, patrol_end):
        self.x, self.y, self.width, self.height = x, y, 32, 32
        self.patrol_start, self.patrol_end = patrol_start, patrol_end
        self.direction, self.speed, self.facing_right = 1, ENEMY_SPEED, True
        self.walk_anim = Animation(['enemy_walk1', 'enemy_walk2'], 0.3)
        
    def update(self, dt):
        self.x += self.speed * self.direction
        if self.x <= self.patrol_start:
            self.direction, self.facing_right = 1, True
        elif self.x >= self.patrol_end:
            self.direction, self.facing_right = -1, False
        self.walk_anim.update(dt)
        
    def draw(self):
        screen.blit(self.walk_anim.get_current_image(), (self.x, self.y))
            
    def get_rect(self):
        return Rect(self.x, self.y, self.width, self.height)

def generate_platforms():
    global platforms, enemies, last_platform_y, last_platform_x, platforms_in_direction, going_right
    platforms, enemies = [Rect(0, 580, WIDTH, 20)], []
    last_platform_y, platforms_in_direction = 580, 0
    going_right = True
    current_x, current_y = 50, 500
    last_platform_x = current_x
    
    for i in range(INITIAL_PLATFORMS):
        platforms.append(Rect(current_x, current_y, PLATFORM_WIDTH, PLATFORM_HEIGHT))
        
        if i > 2 and random.random() < ENEMY_SPAWN_CHANCE:
            enemies.append(Enemy(current_x + 20, current_y - 32, current_x, current_x + PLATFORM_WIDTH - 32))
        
        current_y -= STAIR_VERTICAL_GAP
        platforms_in_direction += 1
        
        if platforms_in_direction >= ZIGZAG_PLATFORMS:
            going_right = not going_right
            platforms_in_direction = 0
        
        current_x += STAIR_HORIZONTAL_GAP if going_right else -STAIR_HORIZONTAL_GAP
        current_x = max(50, min(WIDTH - PLATFORM_WIDTH - 50, current_x))
        last_platform_x = current_x
    
    last_platform_y = current_y

def generate_platforms_ahead():
    global platforms, enemies, last_platform_y, last_platform_x, platforms_in_direction, going_right
    
    current_x, current_y = last_platform_x, last_platform_y
    
    for i in range(PLATFORMS_GENERATED_AHEAD):
        current_y -= STAIR_VERTICAL_GAP
        platforms_in_direction += 1
        
        if platforms_in_direction >= ZIGZAG_PLATFORMS:
            going_right = not going_right
            platforms_in_direction = 0
        
        current_x += STAIR_HORIZONTAL_GAP if going_right else -STAIR_HORIZONTAL_GAP
        current_x = max(50, min(WIDTH - PLATFORM_WIDTH - 50, current_x))
        
        platforms.append(Rect(current_x, current_y, PLATFORM_WIDTH, PLATFORM_HEIGHT))
        
        if i > 1 and random.random() < ENEMY_SPAWN_CHANCE:
            enemies.append(Enemy(current_x + 20, current_y - 32, current_x, current_x + PLATFORM_WIDTH - 32))
    
    last_platform_y, last_platform_x = current_y, current_x

# Game objects
player = Player(100, 400)
platforms, enemies = [], []
generate_platforms()

# Menu
menu_buttons = {
    'start': Rect(300, 200, 200, 50),
    'music': Rect(300, 280, 200, 50),
    'exit': Rect(300, 360, 200, 50)
}

def update(dt):
    global game_state
    if game_state == "playing":
        player.update(dt)
        for enemy in enemies:
            enemy.update(dt)
        check_enemy_collisions()
        if keyboard.escape:
            game_state = "menu"

def on_mouse_down(pos):
    global game_state, music_enabled
    if game_state == "menu":
        if menu_buttons['start'].collidepoint(pos):
            game_state = "playing"
            player.reset_position()
            play_sound('menu_select')
        elif menu_buttons['music'].collidepoint(pos):
            music_enabled = not music_enabled
            toggle_music()
            play_sound('menu_select')
        elif menu_buttons['exit'].collidepoint(pos):
            play_sound('menu_select')
            exit()

def check_enemy_collisions():
    player_rect = Rect(player.x, player.y, player.width, player.height)
    for enemy in enemies:
        if player_rect.colliderect(enemy.get_rect()):
            play_sound('hit')
            player.reset_position()
            break

def play_sound(sound_name):
    if sounds_enabled:
        try: getattr(sounds, sound_name).play()
        except: pass

def toggle_music():
    try:
        if music_enabled:
            music.play('background_music')
            music.set_volume(MUSIC_VOLUME)
        else:
            music.stop()
    except Exception as e:
        print(f"Music error: {e}")

def draw():
    screen.fill((135, 206, 235))
    draw_menu() if game_state == "menu" else draw_game()

def draw_menu():
    screen.draw.text("PLATFORM ADVENTURE", center=(WIDTH//2, 120), fontsize=48, color="white", shadow=(2, 2))
    
    for button_name, button_rect in menu_buttons.items():
        color = "lightblue" if button_name != 'music' else ("green" if music_enabled else "red")
        screen.draw.filled_rect(button_rect, color)
        screen.draw.rect(button_rect, "white")
        
        text = {"start": "START GAME", "music": f"MUSIC: {'ON' if music_enabled else 'OFF'}", "exit": "EXIT"}[button_name]
        screen.draw.text(text, center=button_rect.center, fontsize=24, color="white")
    
    screen.draw.text("Arrow keys to move, SPACE to jump", center=(WIDTH//2, 480), fontsize=20, color="white")
    screen.draw.text("Climb as high as you can!", center=(WIDTH//2, 510), fontsize=20, color="white")
    if highest_platform > 0:
        screen.draw.text(f"Best Height: {highest_platform}", center=(WIDTH//2, 540), fontsize=18, color="yellow")

def draw_game():
    # Draw platforms
    for platform in platforms:
        if camera_y - 50 < platform.y < camera_y + HEIGHT + 50:
            adjusted_rect = Rect(platform.x, platform.y - camera_y, platform.width, platform.height)
            screen.draw.filled_rect(adjusted_rect, "brown")
            screen.draw.rect(adjusted_rect, "black")
    
    # Draw player
    screen.blit(player.current_anim.get_current_image(), (player.x, player.y - camera_y))
    
    # Draw enemies
    for enemy in enemies:
        if camera_y - 50 < enemy.y < camera_y + HEIGHT + 50:
            screen.blit(enemy.walk_anim.get_current_image(), (enemy.x, enemy.y - camera_y))
    
    # UI
    screen.draw.text("ESC - Return to Menu", (10, 10), fontsize=16, color="white")
    screen.draw.text(f"Height: {score}", (10, 30), fontsize=20, color="yellow")
    screen.draw.text(f"Best: {highest_platform}", (10, 55), fontsize=16, color="green")
    screen.draw.text(f"Music: {'ON' if music_enabled else 'OFF'}", (10, 80), fontsize=14, color="white")
    screen.draw.text("↑ CLIMB HIGHER ↑", center=(WIDTH//2, 30), fontsize=24, color="white")

# Initialize
def start_background_music():
    if music_enabled:
        try:
            music.play('background_music')
            music.set_volume(MUSIC_VOLUME)
            print("Background music started successfully")
        except Exception as e:
            print(f"Failed to start background music: {e}")

start_background_music()
pgzrun.go()
