import pygame
import random
import time
import os

pygame.init()

WIDTH, HEIGHT = 300, 600
GRID_SIZE = 30
GRID_WIDTH = WIDTH // GRID_SIZE
GRID_HEIGHT = HEIGHT // GRID_SIZE
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("PALIKKA")

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Define color constants (we'll use these as keys for our block images)
RED = "red"
GREEN = "green"
BLUE = "blue"
PURPLE = "purple"
YELLOW = "yellow"
CYAN = "cyan"

ALL_COLORS = [RED, GREEN, BLUE, PURPLE, YELLOW, CYAN]

grid = [[BLACK for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]

LEVEL_THRESHOLD = 100  # Points needed to level up, easily adjustable

level = 1

# Load block images
def load_block_images(directory="images"):
    block_images = {}
    for color in ALL_COLORS:
        try:
            image_path = os.path.join(directory, f"{color}4.png")
            image = pygame.image.load(image_path)
            image = pygame.transform.scale(image, (GRID_SIZE, GRID_SIZE))
            block_images[color] = image
        except pygame.error:
            print(f"Couldn't load image for {color}. Using fallback color.")
            block_images[color] = pygame.Surface((GRID_SIZE, GRID_SIZE))
            block_images[color].fill(pygame.Color(color))
    return block_images

# Load background images
def load_background_images(directory="images"):
    background_images = []
    for i in range(1, 9):  # Load exactly 8 images
        try:
            image_path = os.path.join(directory, f"background_mono_{i}.png")
            image = pygame.image.load(image_path)
            image = pygame.transform.scale(image, (WIDTH, HEIGHT))
            background_images.append(image)
        except pygame.error:
            print(f"Couldn't load background_{i}.png. Using fallback color.")
            fallback_image = pygame.Surface((WIDTH, HEIGHT))
            fallback_image.fill((50, 50, 80))  # Fallback color
            background_images.append(fallback_image)
    return background_images

# Set images to be used as default
use_png_blocks = True
use_background_images = True

# Global variables for images
block_images = load_block_images()
background_images = load_background_images()

class Block:
    def __init__(self, colors):
        self.colors = [random.choice(colors) for _ in range(3)]
        self.x = GRID_WIDTH // 2
        self.y = 0
        self.landed = False

    def move(self, dx):
        if not self.landed:
            new_x = self.x + dx
            if 0 <= new_x < GRID_WIDTH and all(grid[self.y + i][new_x] == BLACK for i in range(3) if self.y + i < GRID_HEIGHT):
                self.x = new_x

    def rotate(self):
        if not self.landed:
            self.colors = [self.colors[-1]] + self.colors[:-1]

    def fall(self):
        if not self.landed:
            if self.y < GRID_HEIGHT - 3 and grid[self.y + 3][self.x] == BLACK:
                self.y += 1
                return True
            else:
                self.landed = True
                return False
        return False

def check_and_remove_matches():
    matches = set()

    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            if grid[y][x] != BLACK:
                # Horizontal
                if x < GRID_WIDTH - 2 and grid[y][x] == grid[y][x+1] == grid[y][x+2]:
                    matches.update((y, x+i) for i in range(3))
                # Vertical
                if y < GRID_HEIGHT - 2 and grid[y][x] == grid[y+1][x] == grid[y+2][x]:
                    matches.update((y+i, x) for i in range(3))
                # Diagonal (top-left to bottom-right)
                if x < GRID_WIDTH - 2 and y < GRID_HEIGHT - 2 and grid[y][x] == grid[y+1][x+1] == grid[y+2][x+2]:
                    matches.update((y+i, x+i) for i in range(3))
                # Diagonal (top-right to bottom-left)
                if x > 1 and y < GRID_HEIGHT - 2 and grid[y][x] == grid[y+1][x-1] == grid[y+2][x-2]:
                    matches.update((y+i, x-i) for i in range(3))

    if matches:
        # Animate matched blocks
        for _ in range(3):  # Flash 3 times
            for y, x in matches:
                pygame.draw.rect(screen, WHITE, (x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE))
            pygame.display.flip()
            time.sleep(0.1)
            draw_grid()
            pygame.display.flip()
            time.sleep(0.1)

        # Remove matched blocks
        for y, x in matches:
            grid[y][x] = BLACK

    return len(matches)

def apply_gravity():
    for x in range(GRID_WIDTH):
        column = [grid[y][x] for y in range(GRID_HEIGHT) if grid[y][x] != BLACK]
        column = [BLACK] * (GRID_HEIGHT - len(column)) + column
        for y in range(GRID_HEIGHT):
            grid[y][x] = column[y]

def game_over():
    return any(grid[0][x] != BLACK for x in range(GRID_WIDTH))

def draw_game_over():
    font = pygame.font.Font(None, 74)
    text = font.render("GAME OVER", True, WHITE)
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(text, text_rect)

def draw_grid():
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            if grid[y][x] != BLACK:
                if use_png_blocks:
                    screen.blit(block_images[grid[y][x]], (x * GRID_SIZE, y * GRID_SIZE))
                else:
                    pygame.draw.rect(screen, pygame.Color(grid[y][x]), 
                                   (x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE))

def draw_score(score):
    font = pygame.font.Font(None, 36)
    text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(text, (10, 10))

def draw_level(level):
    font = pygame.font.Font(None, 36)
    text = font.render(f"Level: {level}", True, WHITE)
    screen.blit(text, (WIDTH - 120, 10))

def draw_combo(combo):
    if combo > 1:
        font = pygame.font.Font(None, 48)
        text = font.render(f"COMBO x{combo}!", True, WHITE)
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(text, text_rect)

def get_gradient_color(y, color):
    gradient = y / HEIGHT
    # return tuple(max(0, min(255, int(c * (1 - gradient * 0.8)))) for c in color)
    return tuple(min(255, int(c + (255 - c) * gradient * 0.6)) for c in color)

def draw_background(level):
    if use_background_images and background_images:
        background_index = (level - 1) % len(background_images)
        screen.blit(background_images[background_index], (0, 0))
    else:
        # Create a gradient background
        base_color = (50, 50, 80)
        gradient_top = tuple(min(255, c + 20) for c in base_color)
        gradient_bottom = tuple(max(0, c - 20) for c in base_color)
        
        for y in range(HEIGHT):
            progress = y / HEIGHT
            current_color = tuple(
                int(gradient_top[i] * (1 - progress) + gradient_bottom[i] * progress)
                for i in range(3)
            )
            pygame.draw.line(screen, current_color, (0, y), (WIDTH, y))

def draw_pause():
    s = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    s.fill((0, 0, 0, 128))
    screen.blit(s, (0, 0))
    font = pygame.font.Font(None, 74)
    text = font.render("PAUSED", True, WHITE)
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(text, text_rect)

def draw_menu(settings, selected_option):
    screen.fill(BLACK)
    font = pygame.font.Font(None, 74)
    title = " PALIKKA"
    for i, char in enumerate(title):
        color = ALL_COLORS[i % len(ALL_COLORS)]
        text = font.render(char, True, color)
        text_rect = text.get_rect(center=(WIDTH // 2 + (i - len(title)/2) * 38, HEIGHT // 4))
        screen.blit(text, text_rect)
    
    font = pygame.font.Font(None, 36)
    options = [
        "Start Game",
        f"Colors: {settings['colors']}",
        f"Debris: {settings['debris']}",
        "Quit Game"
    ]
    
    for i, option in enumerate(options):
        color = WHITE if i == selected_option else (150, 150, 150)
        text = font.render(option, True, color)
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + i * 50))
        screen.blit(text, text_rect)

    # Credits
    font = pygame.font.Font(None, 22)
    text1 = font.render("Use arrow keys to play", True, WHITE)
    text2 = font.render("P = pause, C = block, B = background", True, WHITE)
    text3 = font.render("Made by Jussi & Claude 3.5", True, YELLOW)
    text_rect1 = text1.get_rect(center=(WIDTH // 2, HEIGHT - 80))
    text_rect2 = text2.get_rect(center=(WIDTH // 2, HEIGHT - 50))
    text_rect3 = text3.get_rect(center=(WIDTH // 2, HEIGHT - 20))
    screen.blit(text1, text_rect1)
    screen.blit(text2, text_rect2)
    screen.blit(text3, text_rect3)

def main_menu():
    settings = {'colors': 4, 'debris': 0}
    selected_option = 0
    draw_menu(settings, selected_option)
    pygame.display.flip()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False, settings
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected_option = (selected_option - 1) % 4
                elif event.key == pygame.K_DOWN:
                    selected_option = (selected_option + 1) % 4
                elif event.key == pygame.K_ESCAPE:
                    return False, None # Quit game from ESC
                elif event.key in (pygame.K_SPACE, pygame.K_LEFT, pygame.K_RIGHT):
                    if selected_option == 0:  # Start Game
                        return True, settings
                    elif selected_option == 1:  # Colors
                        if event.key in (pygame.K_SPACE, pygame.K_RIGHT):
                            settings['colors'] = min(6, settings['colors'] + 1)
                        else:
                            settings['colors'] = max(4, settings['colors'] - 1)
                    elif selected_option == 2:  # Debris
                        if event.key in (pygame.K_SPACE, pygame.K_RIGHT):
                            settings['debris'] = min(10, settings['debris'] + 5)
                        else:
                            settings['debris'] = max(0, settings['debris'] - 5)
                    elif selected_option == 3:  # Quit Game
                        return False, None
                draw_menu(settings, selected_option)
                pygame.display.flip()
    return False, settings

def add_debris(grid, debris_amount, colors):
    for _ in range(debris_amount):
        y = GRID_HEIGHT - 1
        while y >= 0 and any(grid[y][x] != BLACK for x in range(GRID_WIDTH)):
            y -= 1
        if y >= 0:
            for x in range(GRID_WIDTH):
                if random.random() < 1.0:
                    available_colors = colors.copy()
                    while available_colors:
                        color = random.choice(available_colors)
                        # Check for horizontal matches
                        h_match = (x > 1 and grid[y][x-1] == grid[y][x-2] == color) or \
                                (x > 0 and x < GRID_WIDTH-1 and grid[y][x-1] == grid[y][x+1] == color) or \
                                (x < GRID_WIDTH-2 and grid[y][x+1] == grid[y][x+2] == color)
                        
                        # Check for vertical matches
                        v_match = (y > 1 and grid[y-1][x] == grid[y-2][x] == color) or \
                                (y > 0 and y < GRID_HEIGHT-1 and grid[y-1][x] == grid[y+1][x] == color) or \
                                (y < GRID_HEIGHT-2 and grid[y+1][x] == grid[y+2][x] == color)
                        
                        # Check for diagonal matches
                        d1_match = (x > 1 and y > 1 and grid[y-1][x-1] == grid[y-2][x-2] == color) or \
                                 (x < GRID_WIDTH-2 and y < GRID_HEIGHT-2 and grid[y+1][x+1] == grid[y+2][x+2] == color)
                        
                        d2_match = (x < GRID_WIDTH-2 and y > 1 and grid[y-1][x+1] == grid[y-2][x+2] == color) or \
                                 (x > 1 and y < GRID_HEIGHT-2 and grid[y+1][x-1] == grid[y+2][x-2] == color)

                        if not (h_match or v_match or d1_match or d2_match):
                            grid[y][x] = color
                            break
                        available_colors.remove(color)
    return grid

def main_game(settings):
    global grid
    colors = ALL_COLORS[:settings['colors']]
    current_block = Block(colors)
    clock = pygame.time.Clock()
    running = True
    paused = False
    score = 0
    combo = 1
    level = 1
    win_displayed = False

    # Variables for movement
    move_cooldown = 0
    move_delay = 10  # Increased delay for slower horizontal movement
    left_pressed = False
    right_pressed = False

    # Variables for fall speed control
    base_fall_speed = 3  # Slower initial fall speed (1.5 seconds per fall)
    fall_speed = base_fall_speed
    fall_timer = 0
    last_fall_time = time.time()
    accelerated_fall = False

    # Variables for grace period and accelerated fall
    grace_period = 0.3  # 300 milliseconds grace period
    grace_timer = 0

    while running:
        current_time = time.time()
        delta_time = current_time - last_fall_time

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    current_block.rotate()
                elif event.key == pygame.K_DOWN:
                    accelerated_fall = True
                elif event.key == pygame.K_LEFT:
                    current_block.move(-1)
                elif event.key == pygame.K_RIGHT:
                    current_block.move(1)
                elif event.key == pygame.K_p:
                    paused = not paused
                elif event.key == pygame.K_c:
                    global use_png_blocks
                    use_png_blocks = not use_png_blocks
                elif event.key == pygame.K_b:
                    global use_background_images
                    use_background_images = not use_background_images
                elif event.key == pygame.K_ESCAPE:
                    return
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:
                    accelerated_fall = False

        if paused:
            draw_pause()
            pygame.display.flip()
            continue

        # Handle block falling
        fall_timer += delta_time
        if accelerated_fall:
            fall_speed = base_fall_speed / 20  # 20 times faster when down is pressed
        else:
            fall_speed = base_fall_speed - (level - 1) * 0.1  # Gradual speed increase
            fall_speed = max(1.0, fall_speed)  # Cap at 1.0

        if fall_timer >= fall_speed:
            if not current_block.fall():
                if grace_timer < grace_period:
                    grace_timer += delta_time
                else:
                    for i in range(3):
                        grid[current_block.y + i][current_block.x] = current_block.colors[i]
                    current_block = Block(colors)
                    grace_timer = 0
                    
                    match_chain = True
                    first_match = True
                    while match_chain:
                        match_size = check_and_remove_matches()
                        if match_size > 0:
                            if match_size == 3:
                                points = 3
                            elif match_size == 4:
                                points = 5
                            else:
                                points = 10
                            score += points * combo
                            if not first_match:
                                combo += 1
                            else:
                                first_match = False
                            apply_gravity()
                            
                            new_level = min(99, score // LEVEL_THRESHOLD + 1)
                            if new_level > level:
                                level = new_level
                                background_color = (random.randint(30, 70), random.randint(30, 70), random.randint(30, 70))
                                if level == 99 and not win_displayed:
                                    win_displayed = True
                            
                            draw_background(level)
                            draw_grid()
                            draw_score(score)
                            draw_level(level)
                            if combo > 1:
                                draw_combo(combo)
                            if win_displayed:
                                draw_win_message()
                            pygame.display.flip()
                            time.sleep(0.5)
                        else:
                            match_chain = False
                            combo = 1
            else:
                grace_timer = 0
            fall_timer = 0
            last_fall_time = current_time

        draw_background(level)
        draw_grid()
        draw_score(score)
        draw_level(level)
        if win_displayed:
            draw_win_message()

        # Draw the current block
        for i in range(3):
            if use_png_blocks:
                screen.blit(block_images[current_block.colors[i]], 
                        (current_block.x * GRID_SIZE, (current_block.y + i) * GRID_SIZE))
            else:
                pygame.draw.rect(screen, pygame.Color(current_block.colors[i]),
                                (current_block.x * GRID_SIZE, 
                                (current_block.y + i) * GRID_SIZE,
                                GRID_SIZE, GRID_SIZE))

        if game_over():
            draw_game_over()
            running = False

        pygame.display.flip()
        clock.tick(60)  # Set a fixed frame rate

    pygame.time.wait(2000)

def draw_win_message():
    font = pygame.font.Font(None, 74)
    text = font.render("YOU WIN!", True, (255, 255, 255))
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 4))
    s = pygame.Surface((text_rect.width + 20, text_rect.height + 20))
    s.set_alpha(200)
    s.fill((0, 0, 0))
    screen.blit(s, (text_rect.x - 10, text_rect.y - 10))
    screen.blit(text, text_rect)

# Main game loop
while True:
    play, settings = main_menu()
    if play:
        grid = [[BLACK for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        colors = ALL_COLORS[:settings['colors']]
        grid = add_debris(grid, settings['debris'], colors)
        main_game(settings)
    else:
        break

pygame.quit()
