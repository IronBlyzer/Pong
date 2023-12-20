import pygame
import sys
import colorsys

pygame.init()

WIDTH, HEIGHT = 800, 600

WHITE = (255, 255, 255)
BLACK = (0,0,0)

NUM_COLORS = 360

angle1 = 0
angle2 = 180

player1_controls_azerty = {"up_key": pygame.K_z, "down_key": pygame.K_s}
player2_controls_azerty = {"up_key": pygame.K_p, "down_key": pygame.K_m}

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Menu de Sélection de Couleurs")

clock = pygame.time.Clock()


    
def get_rainbow_color(angle):
    """Obtenir une couleur de l'arc-en-ciel en fonction de l'angle."""
    angle %= NUM_COLORS  
    rgb = colorsys.hsv_to_rgb(angle / NUM_COLORS, 1.0, 1.0)
    return (int(rgb[0] * 255), int(rgb[1] * 255), int(rgb[2] * 255))

def draw_color_menu(angle, x_position, player_text, controls):
    
    font_title = pygame.font.Font(None, 36)
    text_title = font_title.render("Paramètres", True, (255, 255, 255))
    screen.blit(text_title, (400 - text_title.get_width() // 2, 50))
    
    current_color = get_rainbow_color(angle)

    pygame.draw.rect(screen, current_color, (x_position - 50, 235, 100, 50))

    font = pygame.font.Font(None, 24)
    text = font.render(player_text, True, (255, 255, 255))
    screen.blit(text, (x_position - text.get_width() // 2, 150))

    pygame.draw.rect(screen, (200, 200, 200), (x_position - 80, 235, 30, 50))  # Bouton gauche
    pygame.draw.rect(screen, (200, 200, 200), (x_position + 50, 235, 30, 50))  # Bouton droit

    font = pygame.font.Font(None, 18)
    text_up_key = pygame.key.name(controls.get("up_key", 0))
    text_down_key = pygame.key.name(controls.get("down_key", 0))
    text_up = font.render(f"Up ({text_up_key})", True, (255, 255, 255))
    text_down = font.render(f"Down ({text_down_key})", True, (255, 255, 255))
    
    y_up = 335
    y_down = 355
    
    screen.blit(text_up, (x_position - text_up.get_width() // 2, y_up))
    screen.blit(text_down, (x_position - text_down.get_width() // 2, y_down))
    
    font_title = pygame.font.Font(None, 26)
    text_title = font_title.render("RETOUR", True, (255, 255, 255))
    screen.blit(text_title, (400 - text_title.get_width() // 2, 500))

def change_controls(controls, event):
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_UP:
            print("Appuyez sur la nouvelle touche pour 'Up'")
            new_key = wait_for_key()
            controls["up_key"] = new_key
        elif event.key == pygame.K_DOWN:
            print("Appuyez sur la nouvelle touche pour 'Down'")
            new_key = wait_for_key()
            controls["down_key"] = new_key

def wait_for_key():
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                return event.key

def change_controls_player1(event):
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_UP:
            print("Appuyez sur la nouvelle touche pour 'Up' de Player 1")
            new_key = wait_for_key()
            player1_controls_azerty["up_key"] = new_key
        elif event.key == pygame.K_LEFT:
            print("Appuyez sur la nouvelle touche pour 'Down' de Player 1")
            new_key = wait_for_key()
            player1_controls_azerty["down_key"] = new_key

def change_controls_player2(event):
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_DOWN:
            print("Appuyez sur la nouvelle touche pour 'Down' de Player 2")
            new_key = wait_for_key()
            player2_controls_azerty["down_key"] = new_key
        elif event.key == pygame.K_RIGHT:
            print("Appuyez sur la nouvelle touche pour 'Up' de Player 2")
            new_key = wait_for_key()
            player2_controls_azerty["up_key"] = new_key
mouse_x, mouse_y = pygame.mouse.get_pos( )                     
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Clic gauche
                if WIDTH // 4 - 80 <= event.pos[0] <= WIDTH // 4 - 50 and 235 <= event.pos[1] <= 285:
                    angle1 -= 10
                elif WIDTH // 4 + 50 <= event.pos[0] <= WIDTH // 4 + 80 and 235 <= event.pos[1] <= 285:
                    angle1 += 10
                elif WIDTH * 3 // 4 - 80 <= event.pos[0] <= WIDTH * 3 // 4 - 50 and 235 <= event.pos[1] <= 285:
                    angle2 -= 10
                elif WIDTH * 3 // 4 + 50 <= event.pos[0] <= WIDTH * 3 // 4 + 80 and 235 <= event.pos[1] <= 285:
                    angle2 += 10
                if WIDTH // 2 - 40 < mouse_x < WIDTH // 2 + 40 and HEIGHT - 50 < mouse_y < HEIGHT - 30:
                    game_state = "menu"
        elif event.type in [pygame.KEYDOWN, pygame.KEYUP]:
            if event.type == pygame.KEYDOWN:
                change_controls_player1(event)
                change_controls_player2(event)
                

    angle1 %= NUM_COLORS
    angle2 %= NUM_COLORS
    screen.fill(BLACK) 
    draw_color_menu(angle1, WIDTH // 4, "Joueur 1", player1_controls_azerty)
    draw_color_menu(angle2, WIDTH * 3 // 4, "Joueur 2", player2_controls_azerty)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()

