import pygame
import json
from pygame.locals import *
import colorsys
import sys

pygame.init()

WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
NUM_COLORS = 360
PADDLE_WIDTH, PADDLE_HEIGHT = 20, 100
BALL_SIZE = 20

def set_game_state(state):
    global game_state, player1_score, player2_score, ball_x, ball_y
    if state == "menu":
        # Reset game variables when returning to the menu
        player1_score = 0
        player2_score = 0
        ball_x, ball_y = WIDTH // 2, HEIGHT // 2
        game_state = state
    elif state == "playing":
        # Add any additional setup needed when transitioning to the playing state
        game_state = state
    elif state == "winner_message":
        # Add any additional setup needed when transitioning to the winner message state
        game_state = state
    elif state == "settings":
        # Add any additional setup needed when transitioning to the settings state
        game_state = state

player1_y = HEIGHT // 2 - PADDLE_HEIGHT // 2
player2_y = HEIGHT // 2 - PADDLE_HEIGHT // 2
ball_x, ball_y = WIDTH // 2, HEIGHT // 2
ball_speed_x, ball_speed_y = 5, 5
player1_score = 0
player2_score = 0
vitpad = 10
angle1 = 0
angle2 = 180
scoremax = 10
player1_controls_Up = pygame.K_a
player1_controls_Down = pygame.K_q
player2_controls_Down = pygame.K_m
player2_controls_Up = pygame.K_p
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong")

clock = pygame.time.Clock()
winner_display_time = 0
winner_display_duration = 15000  # 15 seconds in milliseconds

# Function to save total wins and colors to a file
def save_game_data(total_wins, angle1, angle2):
    with open('total_wins.json', 'w') as file:
        json.dump({
            'total_wins': total_wins,
            'angle1': angle1,
            'angle2': angle2
        }, file)

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

# Function to load total wins and colors from a file
def load_game_data():
    try:
        with open('total_wins.json', 'r') as file:
            data = json.load(file)
            return (
                data.get('total_wins', 0),
                data.get('angle1', angle1),
                data.get('angle2', angle2)
            )
    except FileNotFoundError:
        return 0, angle1, angle2

# Load total wins and colors at the start of the game
total_wins, angle1, angle2 = load_game_data()

def reset_ball():
    return WIDTH // 2, HEIGHT // 2

menu_button = Button("Retour", WIDTH // 2 - 60, HEIGHT // 2 + 40, 120, 40, lambda: set_game_state("menu"))

def get_rainbow_color(angle):
    angle %= NUM_COLORS
    rgb = colorsys.hsv_to_rgb(angle / NUM_COLORS, 1.0, 1.0)
    return (int(rgb[0] * 255), int(rgb[1] * 255), int(rgb[2] * 255))

def draw_color_menu(angle, x_position, player_text):
    current_color = get_rainbow_color(angle)

    pygame.draw.rect(screen, current_color, (x_position - 50, 235, 100, 50))

    font = pygame.font.Font(None, 24)
    text = font.render(player_text, True, WHITE)
    screen.blit(text, (x_position - text.get_width() // 2, 150))

    pygame.draw.rect(screen, (BLACK), (x_position - 100, 235, 50, 50))  # Left button
    pygame.draw.rect(screen, (BLACK), (x_position + 51, 235, 50, 50))  # Right button
    font_title = pygame.font.Font(None, 152)
    fleche1 = font_title.render("<", True, (255, 255, 255))
    fleche2 = font_title.render(">", True, (255, 255, 255))
    screen.blit(fleche1, (x_position - 105, 200))
    screen.blit(fleche2, (x_position + 46, 200))

# Initial game state
game_state = "menu"



# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if game_state == "menu":
                if WIDTH // 2 - 40 < event.pos[0] < WIDTH // 2 + 40 and HEIGHT // 2 - 20 < event.pos[1] < HEIGHT // 2 + 10:
                    set_game_state("playing")
                elif WIDTH // 2 - 70 < event.pos[0] < WIDTH // 2 + 70 and HEIGHT // 2 + 20 < event.pos[1] < HEIGHT // 2 + 60:
                    set_game_state("settings")
            elif game_state == "settings":
                if WIDTH // 2 - 40 < event.pos[0] < WIDTH // 2 + 40 and HEIGHT - 50 < event.pos[1] < HEIGHT - 30:
                    # Save colors immediately when returning to menu
                    save_game_data(total_wins, angle1, angle2)
                    set_game_state("menu")
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
                    # Save colors immediately when changed
                    save_game_data(total_wins, angle1, angle2)

    angle1 %= NUM_COLORS
    angle2 %= NUM_COLORS

    screen.fill(BLACK)

    if game_state == "menu":
        # Draw menu options
        font = pygame.font.Font(None, 36)
        play_option = font.render("Jouer", True, WHITE)
        settings_option = font.render("Paramètres", True, WHITE)
        screen.blit(play_option, (WIDTH // 2 - 40, HEIGHT // 2 - 20))
        screen.blit(settings_option, (WIDTH // 2 - 70, HEIGHT // 2 + 20))
        wins_display = font.render(f"Points: {total_wins}", True, WHITE)
        screen.blit(wins_display, (10, 10))
        
    elif game_state == "settings":
        # Draw settings
        font_title = pygame.font.Font(None, 36)
        text_title = font_title.render("Paramètres", True, WHITE)
        screen.blit(text_title, (WIDTH // 2 - text_title.get_width() // 2, 50))

        draw_color_menu(angle1, WIDTH // 4, "Joeur 1")
        draw_color_menu(angle2, WIDTH * 3 // 4, "Joeur 2")
        
        font = pygame.font.Font(None, 18)
        text_up1 = font.render(f"Up ({pygame.key.name(player1_controls_Up)})", True, WHITE)
        text_down1 = font.render(f"Down ({pygame.key.name(player1_controls_Down)})", True, WHITE)
        text_up2 = font.render(f"Up ({pygame.key.name(player2_controls_Up)})", True, WHITE)
        text_down2 = font.render(f"Down ({pygame.key.name(player2_controls_Down)})", True, WHITE)
        y_up = 335
        y_down = 355
        screen.blit(text_up1, (WIDTH // 4 - text_up1.get_width() // 2, y_up))
        screen.blit(text_down1, (WIDTH // 4 - text_down1.get_width() // 2, y_down))
        screen.blit(text_up2, (WIDTH * 3 // 4 - text_up2.get_width() // 2, y_up))
        screen.blit(text_down2, (WIDTH * 3 // 4 - text_down2.get_width() // 2, y_down))
  
        font_return = pygame.font.Font(None, 26)
        text_return = font_return.render("RETURN", True, WHITE)
        screen.blit(text_return, (WIDTH // 2 - text_return.get_width() // 2, HEIGHT - 50))
    
    elif game_state == "playing":
        pygame.draw.rect(screen, get_rainbow_color(angle1), (0, player1_y, PADDLE_WIDTH, PADDLE_HEIGHT))
        pygame.draw.rect(screen, get_rainbow_color(angle2), (WIDTH - PADDLE_WIDTH, player2_y, PADDLE_WIDTH, PADDLE_HEIGHT))
        pygame.draw.ellipse(screen, WHITE, (ball_x, ball_y, BALL_SIZE, BALL_SIZE))

        font = pygame.font.Font(None, 36)
        score_display = font.render(f"{player1_score} - {player2_score}", True, WHITE)
        screen.blit(score_display, (WIDTH // 2 - 40, 20))

        keys = pygame.key.get_pressed()
        if keys[player1_controls_Up] and player1_y > 0:
            player1_y -= vitpad
        elif keys[player1_controls_Down] and player1_y < HEIGHT - PADDLE_HEIGHT:
            player1_y += vitpad
        elif keys[player2_controls_Down] and player2_y < HEIGHT - PADDLE_HEIGHT:
            player2_y += vitpad
        elif keys[player2_controls_Up] and player2_y > 0:
            player2_y -= vitpad

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
            if player2_score == 1:
                total_wins += 1
                # Save total wins and colors when a game is finished
                save_game_data(total_wins, angle1, angle2)
                winner_display_time = pygame.time.get_ticks()
                set_game_state("winner_message")
            else:
                ball_x, ball_y = reset_ball()

        elif ball_x >= WIDTH - BALL_SIZE:
            player1_score += 1
            if player1_score == 1:
                total_wins += 1
                # Save total wins and colors when a game is finished
                save_game_data(total_wins, angle1, angle2)
                winner_display_time = pygame.time.get_ticks()
                set_game_state("winner_message")
            else:
                ball_x, ball_y = reset_ball()

    elif game_state == "winner_message":
        screen.fill(BLACK)
        font = pygame.font.Font(None, 36)
        winner_text = f"Joueur {1 if player1_score == 1 else 2} gagne!"
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

    clock.tick(60)

pygame.quit()
sys.exit()