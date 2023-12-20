import pygame
import sys
import colorsys

pygame.init()

WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
NUM_COLORS = 360
PADDLE_WIDTH, PADDLE_HEIGHT = 20, 100
BALL_SIZE = 20

player1_y = HEIGHT // 2 - PADDLE_HEIGHT // 2
player2_y = HEIGHT // 2 - PADDLE_HEIGHT // 2
ball_x, ball_y = WIDTH // 2, HEIGHT // 2
ball_speed_x, ball_speed_y = 5, 5
player1_score = 0
player2_score = 0

angle1 = 0
angle2 = 180

# Controls for Player 1 and Player 2
player1_controls_azerty = {"up_key": pygame.K_z, "down_key": pygame.K_s}
player2_controls_azerty = {"up_key": pygame.K_p, "down_key": pygame.K_m}

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong")

clock = pygame.time.Clock()

keys = pygame.key.get_pressed()
if keys[pygame.K_w] and player1_y > 0:
    player1_y -= 5
if keys[pygame.K_s] and player1_y < HEIGHT - PADDLE_HEIGHT:
    player1_y += 5
if keys[pygame.K_UP] and player2_y > 0:
    player2_y -= 5
if keys[pygame.K_DOWN] and player2_y < HEIGHT - PADDLE_HEIGHT:
    player2_y += 5
    
def reset_ball():
    return WIDTH // 2, HEIGHT // 2

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
    if event.type == pygame.KEYDOWN:
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
        # Draw menu options
        font = pygame.font.Font(None, 36)
        play_option = font.render("Play", True, WHITE)
        settings_option = font.render("Settings", True, WHITE)
        screen.blit(play_option, (WIDTH // 2 - 40, HEIGHT // 2 - 20))
        screen.blit(settings_option, (WIDTH // 2 - 70, HEIGHT // 2 + 20))

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
            ball_x, ball_y = reset_ball()

        elif ball_x >= WIDTH - BALL_SIZE:
            player1_score += 1
            ball_x, ball_y = reset_ball()

        if player1_score == 5 or player2_score == 5:
            running = False

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()