import pygame
import json
from pygame.locals import *

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
RED = (255, 0, 0)
GREEN = (0, 0, 255)

# Function to save total wins to a file
def save_total_wins(total_wins):
    with open('total_wins.json', 'w') as file:
        json.dump({'total_wins': total_wins}, file)

# Function to load total wins from a file
def load_total_wins():
    try:
        with open('total_wins.json', 'r') as file:
            data = json.load(file)
            return data.get('total_wins', 0)
    except FileNotFoundError:
        return 0

# Load total wins at the start of the game
total_wins = load_total_wins()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong")

player1_y = HEIGHT // 2 - PADDLE_HEIGHT // 2
player2_y = HEIGHT // 2 - PADDLE_HEIGHT // 2
ball_x, ball_y = WIDTH // 2, HEIGHT // 2
ball_speed_x, ball_speed_y = 5, 5

player1_score = 0
player2_score = 0

player1_color = RED
player2_color = GREEN

game_state = "menu"

player1_controls_azerty = {pygame.K_z: -5, pygame.K_s: 5}
player1_controls_qwerty = {pygame.K_w: -5, pygame.K_s: 5}
player2_controls_azerty = {pygame.K_UP: -5, pygame.K_DOWN: 5}
player2_controls_qwerty = {pygame.K_w: -5, pygame.K_s: 5}

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

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_SPACE:
                paused = not paused

    if paused:
        clock.tick(FPS)
        continue

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] and player1_y > 0:
        player1_y -= 5
    if keys[pygame.K_s] and player1_y < HEIGHT - PADDLE_HEIGHT:
        player1_y += 5
    if keys[pygame.K_UP] and player2_y > 0:
        player2_y -= 5
    if keys[pygame.K_DOWN] and player2_y < HEIGHT - PADDLE_HEIGHT:
        player2_y += 5

    if game_state == "menu":
        screen.fill(BLACK)
        font = pygame.font.Font(None, 36)
        play_option = font.render("Jouer", True, WHITE)
        settings_option = font.render("Paramètres", True, WHITE)

        screen.blit(play_option, (WIDTH // 2 - 40, HEIGHT // 2 - 20))
        screen.blit(settings_option, (WIDTH // 2 - 70, HEIGHT // 2 + 20))

        wins_display = font.render(f"Victoires: {total_wins}", True, WHITE)
        screen.blit(wins_display, (10, 10))

        mouse_x, mouse_y = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if WIDTH // 2 - 40 < mouse_x < WIDTH // 2 + 40 and HEIGHT // 2 - 20 < mouse_y < HEIGHT // 2 + 10:
                set_game_state("playing")
            elif WIDTH // 2 - 70 < mouse_x < WIDTH // 2 + 70 and HEIGHT // 2 + 20 < mouse_y < HEIGHT // 2 + 60:
                set_game_state("settings")

    elif game_state == "playing":
        screen.fill(BLACK)
        pygame.draw.rect(screen, player1_color, (0, player1_y, PADDLE_WIDTH, PADDLE_HEIGHT))
        pygame.draw.rect(screen, player2_color, (WIDTH - PADDLE_WIDTH, player2_y, PADDLE_WIDTH, PADDLE_HEIGHT))
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
            if player2_score == 5:
                total_wins += 1
                # Save total wins when a game is finished
                save_total_wins(total_wins)
                winner_display_time = pygame.time.get_ticks()
                game_state = "winner_message"
            else:
                ball_x, ball_y = reset_ball()

        elif ball_x >= WIDTH - BALL_SIZE:
            player1_score += 1
            if player1_score == 5:
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
