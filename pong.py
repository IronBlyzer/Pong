import pygame
import json
import os
from pygame.locals import *
import colorsys
import sys
import random


pygame.init()

music_folder = "musiques"
all_files = os.listdir(music_folder)
music_files = [file for file in all_files if file.endswith(('.mp3', '.wav', '.ogg'))]
selected_music = os.path.join(music_folder, random.choice(music_files))
pygame.mixer.music.load(selected_music)
pygame.mixer.music.play()


WIDTH, HEIGHT = 1600, 900
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
NUM_COLORS = 360
PADDLE_WIDTH, PADDLE_HEIGHT = 20, 100
BALL_SIZE = 20

def set_game_state(state):
    global game_state, joueur1_score, joueur2_score, ball_x, ball_y
    if state == "menu":
        joueur1_score = 0
        joueur2_score = 0
        ball_x, ball_y = WIDTH // 2, HEIGHT // 2
        game_state = state
    elif state == "joué":
        game_state = state
    elif state == "gagnant":
        game_state = state
    elif state == "paramètres":
        game_state = state
    elif state == "boutique":
        game_state = state

joueur1_y = HEIGHT // 2 - PADDLE_HEIGHT // 2
joueur2_y = HEIGHT // 2 - PADDLE_HEIGHT // 2
ball_x, ball_y = WIDTH // 2, HEIGHT // 2
ball_speed_x, ball_speed_y = 5, 5
joueur1_score = 0
joueur2_score = 0
vitpad = 10
couleur_joueur1 = 0
couleur_joueur2 = 180
joueur1_controls_Up = pygame.K_a
joueur1_controls_Down = pygame.K_q
joueur2_controls_Down = pygame.K_m
joueur2_controls_Up = pygame.K_p
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong")

clock = pygame.time.Clock()
winner_display_time = 0
winner_display_duration = 15000 

repertoire_images = "images"
boutique_images = [f for f in os.listdir(repertoire_images) if f.endswith(('.png', '.jpg', '.jpeg'))]
selected_image = None

background_images_folder = "images"
background_images = [f for f in os.listdir(background_images_folder) if f.endswith(('.png', '.jpg', '.jpeg'))]
background_image = None

def get_random_background():
    return pygame.image.load(os.path.join(background_images_folder, random.choice(background_images)))



def draw_boutique():
    screen.fill(BLACK)
    font = pygame.font.Font(None, 36)
    boutique_title = font.render("Image boutique", True, WHITE)
    screen.blit(boutique_title, (WIDTH // 2 - boutique_title.get_width() // 2, 50))

    for i, image in enumerate(boutique_images):
        image_surface = pygame.image.load(os.path.join(repertoire_images, image))
        image_surface = pygame.transform.scale(image_surface, (100, 100))
        screen.blit(image_surface, (50, 150 + i * 120))
        text = font.render(f"{image} - 5 points", True, WHITE)
        screen.blit(text, (200, 150 + i * 120))

    text_points = font.render(f"Points: {points}", True, WHITE)
    screen.blit(text_points, (50, 50))

def draw_return_button():
    font_return = pygame.font.Font(None, 26)
    text_return = font_return.render("RETURN", True, WHITE)
    screen.blit(text_return, (WIDTH // 2 - text_return.get_width() // 2, HEIGHT - 50))

    pygame.display.flip()


def save_game_data(points, couleur_joueur1, couleur_joueur2):
    with open('points.json', 'w') as file:
        json.dump({
            'points': points,
            'couleur_joueur1': couleur_joueur1,
            'couleur_joueur2': couleur_joueur2
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

def load_game_data():
    try:
        with open('points.json', 'r') as file:
            data = json.load(file)
            return (
                data.get('points', 0),
                data.get('couleur_joueur1', couleur_joueur1),
                data.get('couleur_joueur2', couleur_joueur2)
            )
    except FileNotFoundError:
        return 0, couleur_joueur1, couleur_joueur2

points, couleur_joueur1, couleur_joueur2 = load_game_data()

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

    pygame.draw.rect(screen, (BLACK), (x_position - 100, 235, 50, 50))
    pygame.draw.rect(screen, (BLACK), (x_position + 51, 235, 50, 50)) 
    font_title = pygame.font.Font(None, 152)
    fleche1 = font_title.render("<", True, (255, 255, 255))
    fleche2 = font_title.render(">", True, (255, 255, 255))
    screen.blit(fleche1, (x_position - 105, 200))
    screen.blit(fleche2, (x_position + 46, 200))

game_state = "menu"
player_images = []

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if game_state == "menu":
                if WIDTH // 2 - 40 < event.pos[0] < WIDTH // 2 + 40 and HEIGHT // 2 - 20 < event.pos[1] < HEIGHT // 2 + 10:
                    set_game_state("joué")
                elif WIDTH // 2 - 70 < event.pos[0] < WIDTH // 2 + 70 and HEIGHT // 2 + 20 < event.pos[1] < HEIGHT // 2 + 60:
                    set_game_state("paramètres")
                elif WIDTH - 120 <= event.pos[0] <= WIDTH - 120 + boutique_button.rect.width and 10 <= event.pos[1] <= 10 + boutique_button.rect.height:
                    set_game_state("boutique")
            elif game_state == "paramètres":
                if WIDTH // 2 - 40 < event.pos[0] < WIDTH // 2 + 40 and HEIGHT - 50 < event.pos[1] < HEIGHT - 30:
                    save_game_data(points, couleur_joueur1, couleur_joueur2)
                    set_game_state("menu")
                else:
                    if WIDTH // 4 - 80 <= event.pos[0] <= WIDTH // 4 - 50 and 235 <= event.pos[1] <= 285:
                        couleur_joueur1 -= 10
                    elif WIDTH // 4 + 50 <= event.pos[0] <= WIDTH // 4 + 80 and 235 <= event.pos[1] <= 285:
                        couleur_joueur1 += 10
                    elif WIDTH * 3 // 4 - 80 <= event.pos[0] <= WIDTH * 3 // 4 - 50 and 235 <= event.pos[1] <= 285:
                        couleur_joueur2 -= 10
                    elif WIDTH * 3 // 4 + 50 <= event.pos[0] <= WIDTH * 3 // 4 + 80 and 235 <= event.pos[1] <= 285:
                        couleur_joueur2 += 10
                    save_game_data(points, couleur_joueur1, couleur_joueur2)
            elif game_state == "boutique":
                x, y = event.pos
                for i, image in enumerate(boutique_images):
                    if 50 <= x <= 150 and 150 + i * 120 <= y <= 150 + (i + 1) * 120:
                        selected_image = image
                        if points >= 5:
                            points -= 5
                            player_images.append(selected_image)
                            print(f"Achat approuvé: {selected_image}")
                            selected_image = None
                            set_game_state("menu")
                        else:
                            print("Points insuffisants")
                if WIDTH // 2 - 60 <= x <= WIDTH // 2 + 60 and HEIGHT - 50 <= y <= HEIGHT - 10:
                    set_game_state("menu")

    couleur_joueur1 %= NUM_COLORS
    couleur_joueur2 %= NUM_COLORS

    if background_image is None:
        background_image = get_random_background()

    screen.blit(background_image, (0, 0))


    if game_state == "menu":
        font = pygame.font.Font(None, 36)
        play_option = font.render("Jouer", True, WHITE)
        paramètres_option = font.render("Paramètres", True, WHITE)
        boutique_option = font.render("Boutique", True, WHITE)  
        boutique_button = Button("Boutique", WIDTH - 120, 10, boutique_option.get_width(), boutique_option.get_height(), lambda: set_game_state("boutique"))
        screen.blit(boutique_option, (WIDTH - 120, 10))
        screen.blit(play_option, (WIDTH // 2 - 40, HEIGHT // 2 - 20))
        screen.blit(paramètres_option, (WIDTH // 2 - 70, HEIGHT // 2 + 20))
        wins_display = font.render(f"Points: {points}", True, WHITE)
        screen.blit(wins_display, (10, 10))

    elif game_state == "paramètres":
        font_title = pygame.font.Font(None, 36)
        text_title = font_title.render("Paramètres", True, WHITE)
        screen.blit(text_title, (WIDTH // 2 - text_title.get_width() // 2, 50))

        draw_color_menu(couleur_joueur1, WIDTH // 4, "Joeur 1")
        draw_color_menu(couleur_joueur2, WIDTH * 3 // 4, "Joeur 2")
        
        font = pygame.font.Font(None, 18)
        text_up1 = font.render(f"Up ({pygame.key.name(joueur1_controls_Up)})", True, WHITE)
        text_down1 = font.render(f"Down ({pygame.key.name(joueur1_controls_Down)})", True, WHITE)
        text_up2 = font.render(f"Up ({pygame.key.name(joueur2_controls_Up)})", True, WHITE)
        text_down2 = font.render(f"Down ({pygame.key.name(joueur2_controls_Down)})", True, WHITE)
        y_up = 335
        y_down = 355
        screen.blit(text_up1, (WIDTH // 4 - text_up1.get_width() // 2, y_up))
        screen.blit(text_down1, (WIDTH // 4 - text_down1.get_width() // 2, y_down))
        screen.blit(text_up2, (WIDTH * 3 // 4 - text_up2.get_width() // 2, y_up))
        screen.blit(text_down2, (WIDTH * 3 // 4 - text_down2.get_width() // 2, y_down))
  
        font_return = pygame.font.Font(None, 26)
        text_return = font_return.render("Retour", True, WHITE)
        screen.blit(text_return, (WIDTH // 2 - text_return.get_width() // 2, HEIGHT - 50))

    elif game_state == "boutique":
        draw_boutique()
        font_return = pygame.font.Font(None, 26)
        text_return = font_return.render("Retour", True, WHITE)
        screen.blit(text_return, (WIDTH // 2 - text_return.get_width() // 2, HEIGHT - 50))

    elif game_state == "joué":
        pygame.draw.rect(screen, get_rainbow_color(couleur_joueur1), (0, joueur1_y, PADDLE_WIDTH, PADDLE_HEIGHT))
        pygame.draw.rect(screen, get_rainbow_color(couleur_joueur2), (WIDTH - PADDLE_WIDTH, joueur2_y, PADDLE_WIDTH, PADDLE_HEIGHT))
        pygame.draw.ellipse(screen, WHITE, (ball_x, ball_y, BALL_SIZE, BALL_SIZE))

        font = pygame.font.Font(None, 36)
        score_display = font.render(f"{joueur1_score} - {joueur2_score}", True, WHITE)
        screen.blit(score_display, (WIDTH // 2 - 40, 20))

        keys = pygame.key.get_pressed()
        if keys[joueur1_controls_Up] and joueur1_y > 0:
            joueur1_y -= vitpad
        elif keys[joueur1_controls_Down] and joueur1_y < HEIGHT - PADDLE_HEIGHT:
            joueur1_y += vitpad
        elif keys[joueur2_controls_Down] and joueur2_y < HEIGHT - PADDLE_HEIGHT:
            joueur2_y += vitpad
        elif keys[joueur2_controls_Up] and joueur2_y > 0:
            joueur2_y -= vitpad

        ball_x += ball_speed_x
        ball_y += ball_speed_y

        if ball_y <= 0 or ball_y >= HEIGHT - BALL_SIZE:
            ball_speed_y = -ball_speed_y

        if (
            (ball_x <= PADDLE_WIDTH and joueur1_y <= ball_y <= joueur1_y + PADDLE_HEIGHT)
            or (ball_x >= WIDTH - PADDLE_WIDTH - BALL_SIZE and joueur2_y <= ball_y <= joueur2_y + PADDLE_HEIGHT)
        ):
            ball_speed_x = -ball_speed_x

        if ball_x <= 0:
            joueur2_score += 1
            if joueur2_score == 5:
                points += 1
                save_game_data(points, couleur_joueur1, couleur_joueur2)
                winner_display_time = pygame.time.get_ticks()
                set_game_state("gagnant")
            else:
                ball_x, ball_y = reset_ball()

        elif ball_x >= WIDTH - BALL_SIZE:
            joueur1_score += 1
            if joueur1_score == 5:
                points += 1
                save_game_data(points, couleur_joueur1, couleur_joueur2)
                winner_display_time = pygame.time.get_ticks()
                set_game_state("gagnant")
            else:
                ball_x, ball_y = reset_ball()

    elif game_state == "gagnant":
        screen.fill(BLACK)
        font = pygame.font.Font(None, 36)
        winner_text = f"Joueur {1 if joueur1_score == 5 else 2} gagne!"
        winner_display = font.render(winner_text, True, WHITE)
        winner_rect = winner_display.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(winner_display, winner_rect)
        menu_button.draw()

        mouse_x, mouse_y = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if menu_button.rect.collidepoint(mouse_x, mouse_y):
                set_game_state("menu")

    if game_state == "gagnant" and winner_display_time > 0 and pygame.time.get_ticks() - winner_display_time > winner_display_duration:
        set_game_state("menu")
        winner_display_time = 0

    pygame.display.flip()

    clock.tick(60)

pygame.quit()
sys.exit()
