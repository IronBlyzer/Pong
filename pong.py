import pygame
import json
from pygame.locals import *
import colorsys
import sys


pygame.init()

pygame.mixer.init()
pygame.mixer.music.load('fast.mp3')
pygame.mixer.music.play()

WIDTH, HEIGHT = 800, 600
FPS = 60
PADDLE_WIDTH, PADDLE_HEIGHT = 20, 100
BALL_SIZE = 20
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
NUM_COLORS = 360


player1_y = HEIGHT // 2 - PADDLE_HEIGHT // 2
player2_y = HEIGHT // 2 - PADDLE_HEIGHT // 2
ball_x, ball_y = WIDTH // 2, HEIGHT // 2
ball_speed_x, ball_speed_y = 5, 5
player1_score = 0
player2_score = 0

angle1 = 0
angle2 = 180

# Function to save total wins to a file
def save_total_wins(total_wins):
    with open('total_wins.json', 'w') as file:
        json.dump({'total_wins': total_wins}, file)

# Function to load total wins and colors from a file
def load_game_data():
    try:
        with open('total_wins.json', 'r') as file:
            data = json.load(file)
            return (
                data.get('total_wins', 0),
                data.get('player1_color', (255, 0, 0)),
                data.get('player2_color', (0, 0, 255))
            )
    except FileNotFoundError:
        return 0, (255, 0, 0), (0, 0, 255)

# Load total wins and colors at the start of the game
total_wins, player1_color, player2_color = load_game_data()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong")

player1_y = HEIGHT // 2 - PADDLE_HEIGHT // 2
player2_y = HEIGHT // 2 - PADDLE_HEIGHT // 2
ball_x, ball_y = WIDTH // 2, HEIGHT // 2
ball_speed_x, ball_speed_y = 5, 5

player1_score = 0
player2_score = 0

game_state = "menu"

player1_controls_azerty = {pygame.K_z: -5, pygame.K_s: 5}
player1_controls_qwerty = {pygame.K_w: -5, pygame.K_s: 5}
player2_controls_azerty = {pygame.K_UP: -5, pygame.K_DOWN: 5}
player2_controls_qwerty = {pygame.K_w: -5, pygame.K_s: 5}

angle1 = 0
angle2 = 180

clock = pygame.time.Clock()
running = True
paused = False

winner_display_time = 0
winner_display_duration = 15000  # 15 seconds in milliseconds

def reset_ball():
    return WIDTH // 2, HEIGHT // 2

class Button:
    def __init__(self, text, x, y, width, height, action):
        self.text = text
        self.rect = pygame.Rect(x, y, width, height)
        self.action = action

    def draw(self):
        pygame.draw.rect(screen, WHITE, self.rect)
        font = pygame.font.Font(None, 36)
        text = font.render(self.text, True, BLACK)
        text_rect = text.get_rect(center=self.rect.center)
        screen.blit(text, text_rect)

def set_game_state(state):
    global game_state, player1_score, player2_score, ball_x, ball_y
    game_state = state
    player1_score = 0
    player2_score = 0
    ball_x, ball_y = reset_ball()

menu_button = Button("Retour", WIDTH // 2 - 60, HEIGHT // 2 + 40, 120, 40, lambda: set_game_state("menu"))

def get_rainbow_color(angle):
    angle %= NUM_COLORS
    rgb = colorsys.hsv_to_rgb(angle / NUM_COLORS, 1.0, 1.0)
    return (int(rgb[0] * 255), int(rgb[1] * 255), int(rgb[2] * 255))

def draw_color_menu(angle, x_position, player_text, controls):
    current_color = get_rainbow_color(angle)

    pygame.draw.rect(screen, current_color, (x_position - 50, 235, 100, 50))

    font = pygame.font.Font(None, 24)
    text = font.render(player_text, True, WHITE)
    screen.blit(text, (x_position - text.get_width() // 2, 150))

    pygame.draw.rect(screen, (200, 200, 200), (x_position - 80, 235, 30, 50))  # Left button
    pygame.draw.rect(screen, (200, 200, 200), (x_position + 50, 235, 30, 50))  # Right button

    font = pygame.font.Font(None, 18)
    text_up_key = pygame.key.name(controls.get("up_key", 0))
    text_down_key = pygame.key.name(controls.get("down_key", 0))
    text_up = font.render(f"Up ({text_up_key})", True, WHITE)
    text_down = font.render(f"Down ({text_down_key})", True, WHITE)

    y_up = 335
    y_down = 355

    screen.blit(text_up, (x_position - text_up.get_width() // 2, y_up))
    screen.blit(text_down, (x_position - text_down.get_width() // 2, y_down))

def change_controls(controls, event):
        if event.key == pygame.K_UP:
            print("Press a new key for 'Up'")
            new_key = wait_for_key()
            controls["up_key"] = new_key
        elif event.key == pygame.K_DOWN:
            print("Press a new key for 'Down'")
            new_key = wait_for_key()
            controls["down_key"] = new_key

def wait_for_key():
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                return event.key

# Continue with the rest of the code...

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if game_state == "menu":
                if WIDTH // 2 - 40 < event.pos[0] < WIDTH // 2 + 40 and HEIGHT // 2 - 20 < event.pos[1] < HEIGHT // 2 + 10:
                    game_state = "playing"
                elif WIDTH // 2 - 70 < event.pos[0] < WIDTH // 2 + 70 and HEIGHT // 2 + 20 < event.pos[1] < HEIGHT // 2 + 60:
                    game_state = "settings"
            elif game_state == "settings":
                if WIDTH // 2 - 40 < event.pos[0] < WIDTH // 2 + 40 and HEIGHT - 50 < event.pos[1] < HEIGHT - 30:
                    game_state = "menu"
                else:
                    # Handle color menu clicks
                    if WIDTH // 4 - 80 <= event.pos[0] <= WIDTH // 4 - 50 and 235 <= event.pos[1] <= 285:
                        angle1 -= 10
                    elif WIDTH // 4 + 50 <= event.pos[0] <= WIDTH // 4 + 80 and 235 <= event.pos[1] <= 285:
                        angle1 += 10
                    elif WIDTH * 3 // 4 - 80 <= event.pos[0] <= WIDTH * 3 // 4 - 50 and 235 <= event.pos[1] <= 285:
                        angle2 -= 10
                    elif WIDTH * 3 // 4 + 50 <= event.pos[0] <= WIDTH * 3 // 4 + 80 and 235 <= event.pos[1] <= 285:
                        angle2 += 10
        if game_state == "playing" : 
            keys = pygame.key.get_pressed()
            if keys[pygame.K_w] and player1_y > 0:
                player1_y -= 15
            if keys[pygame.K_s] and player1_y < HEIGHT - PADDLE_HEIGHT:
                player1_y += 15
            if keys[pygame.K_UP] and player2_y > 0:
                player2_y -= 15
            if keys[pygame.K_DOWN] and player2_y < HEIGHT - PADDLE_HEIGHT:
                player2_y += 15
                
        elif event.type in [pygame.KEYDOWN, pygame.KEYUP]:
            if game_state == "settings":
                change_controls(player1_controls_azerty, event)
                change_controls(player2_controls_azerty, event)

    angle1 %= NUM_COLORS
    angle2 %= NUM_COLORS

    screen.fill(BLACK)

    if game_state == "menu":
        screen.fill(BLACK)
        font = pygame.font.Font(None, 36)
        play_option = font.render("Jouer", True, WHITE)
        settings_option = font.render("Paramètres", True, WHITE)

        screen.blit(play_option, (WIDTH // 2 - 40, HEIGHT // 2 - 20))
        screen.blit(settings_option, (WIDTH // 2 - 70, HEIGHT // 2 + 20))

        wins_display = font.render(f"Victoires: {total_wins}", True, WHITE)
        screen.blit(wins_display, (10, 10))


    elif game_state == "settings":
        # Draw settings
        font_title = pygame.font.Font(None, 36)
        text_title = font_title.render("Settings", True, WHITE)
        screen.blit(text_title, (WIDTH // 2 - text_title.get_width() // 2, 50))

        draw_color_menu(angle1, WIDTH // 4, "Player 1", player1_controls_azerty)
        draw_color_menu(angle2, WIDTH * 3 // 4, "Player 2", player2_controls_azerty)

        font_return = pygame.font.Font(None, 26)
        text_return = font_return.render("RETURN", True, WHITE)
        screen.blit(text_return, (WIDTH // 2 - text_return.get_width() // 2, HEIGHT - 50))

    elif game_state == "playing":
        screen.fill(BLACK)
        pygame.draw.rect(screen, get_rainbow_color(angle1), (0, player1_y, PADDLE_WIDTH, PADDLE_HEIGHT))
        pygame.draw.rect(screen, get_rainbow_color(angle2), (WIDTH - PADDLE_WIDTH, player2_y, PADDLE_WIDTH, PADDLE_HEIGHT))
        pygame.draw.ellipse(screen, WHITE, (ball_x, ball_y, BALL_SIZE, BALL_SIZE))

        font = pygame.font.Font(None, 36)
        score_display = font.render(f"{player1_score} - {player2_score}", True, WHITE)
        screen.blit(score_display, (WIDTH // 2 - 40, 20))

        keys = pygame.key.get_pressed()
        if keys[pygame.K_z] and player1_y > 0:
            player1_y += player1_controls_azerty.get(pygame.K_z, 0)
        if keys[pygame.K_s] and player1_y < HEIGHT - PADDLE_HEIGHT:
            player1_y += player1_controls_azerty.get(pygame.K_s, 0)
        if keys[pygame.K_w] and player1_y > 0:
            player1_y += player1_controls_qwerty.get(pygame.K_w, 0)
        if keys[pygame.K_s] and player1_y < HEIGHT - PADDLE_HEIGHT:
            player1_y += player1_controls_qwerty.get(pygame.K_s, 0)

        if keys[pygame.K_UP] and player2_y > 0:
            player2_y += player2_controls_azerty.get(pygame.K_UP, 0)
        if keys[pygame.K_DOWN] and player2_y < HEIGHT - PADDLE_HEIGHT:
            player2_y += player2_controls_azerty.get(pygame.K_DOWN, 0)
        if keys[pygame.K_UP] and player2_y > 0:
            player2_y += player2_controls_qwerty.get(pygame.K_w, 0)
        if keys[pygame.K_DOWN] and player2_y < HEIGHT - PADDLE_HEIGHT:
            player2_y += player2_controls_qwerty.get(pygame.K_s, 0)

        ball_x += ball_speed_x
        ball_y += ball_speed_y

        if ball_y <= 0 or ball_y >= HEIGHT - BALL_SIZE:
            ball_speed_y = -ball_speed_y

        if (
            (ball_x <= PADDLE_WIDTH and player1_y <= ball_y <= player1_y + PADDLE_HEIGHT)
            or (ball_x >= WIDTH - PADDLE_WIDTH - BALL_SIZE and player2_y <= ball_y <= player2_y + PADDLE_HEIGHT)
        ):
            ball_speed_x = -ball_speed_x

        if ball_x <= 0:
            player2_score += 1
            if player2_score == 10:
                total_wins += 1
                # Save total wins when a game is finished
                save_total_wins(total_wins)
                winner_display_time = pygame.time.get_ticks()
                game_state = "winner_message"
            else:
                ball_x, ball_y = reset_ball()

        elif ball_x >= WIDTH - BALL_SIZE:
            player1_score += 1
            if player1_score == 10:
                total_wins += 1
                # Save total wins when a game is finished
                save_total_wins(total_wins)
                winner_display_time = pygame.time.get_ticks()
                game_state = "winner_message"
            else:
                ball_x, ball_y = reset_ball()

    elif game_state == "settings":
        screen.fill(BLACK)
        
        font = pygame.font.Font(None, 36)
        back_option = font.render("Retour", True, WHITE)

        screen.blit(back_option, (WIDTH // 2 - 40, HEIGHT - 50))

        mouse_x, mouse_y = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if WIDTH // 2 - 40 < mouse_x < WIDTH // 2 + 40 and HEIGHT - 50 < mouse_y < HEIGHT - 30:
                set_game_state("menu")

    elif game_state == "winner_message":
        screen.fill(BLACK)
        font = pygame.font.Font(None, 36)
        winner_text = f"Player {1 if player1_score == 5 else 2} wins!"
        winner_display = font.render(winner_text, True, WHITE)
        winner_rect = winner_display.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(winner_display, winner_rect)
        menu_button.draw()

        mouse_x, mouse_y = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if menu_button.rect.collidepoint(mouse_x, mouse_y):
                set_game_state("menu")

    # Check if 15 seconds have passed since displaying the winner message
    if game_state == "winner_message" and winner_display_time > 0 and pygame.time.get_ticks() - winner_display_time > winner_display_duration:
        set_game_state("menu")
        winner_display_time = 0

    pygame.display.flip()

    clock.tick(FPS)

pygame.quit()
