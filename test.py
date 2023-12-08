import pygame
import sys
import colorsys

# Initialisation de Pygame
pygame.init()

# Définition de la taille de la fenêtre
WIDTH, HEIGHT = 800, 600

# Définition des couleurs
WHITE = (255, 255, 255)
BLACK = (0,0,0)

# Définition du nombre de couleurs dans l'arc-en-ciel
NUM_COLORS = 360

# Définition des angles par défaut
angle1 = 0
angle2 = 180

# Contrôles par défaut
player1_controls_azerty = {"up_key": pygame.K_z, "down_key": pygame.K_s}
player2_controls_azerty = {"up_key": pygame.K_p, "down_key": pygame.K_m}

# Création de la fenêtre
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Menu de Sélection de Couleurs")

clock = pygame.time.Clock()

def get_rainbow_color(angle):
    """Obtenir une couleur de l'arc-en-ciel en fonction de l'angle."""
    angle %= NUM_COLORS  # Assurez-vous que l'angle reste dans la plage 0-359
    rgb = colorsys.hsv_to_rgb(angle / NUM_COLORS, 1.0, 1.0)
    return (int(rgb[0] * 255), int(rgb[1] * 255), int(rgb[2] * 255))

def draw_color_menu(angle, x_position, player_text, controls):
    # Calcul de la couleur de l'arc-en-ciel en fonction de l'angle
    current_color = get_rainbow_color(angle)

    # Affichage du sélecteur de couleurs
    pygame.draw.rect(screen, current_color, (x_position - 50, 235, 100, 50))

    # Affichage du texte du joueur
    font = pygame.font.Font(None, 24)
    text = font.render(player_text, True, (255, 255, 255))
    screen.blit(text, (x_position - text.get_width() // 2, 150))

    # Affichage des boutons de défilement
    pygame.draw.rect(screen, (200, 200, 200), (x_position - 80, 235, 30, 50))  # Bouton gauche
    pygame.draw.rect(screen, (200, 200, 200), (x_position + 50, 235, 30, 50))  # Bouton droit

    # Affichage des labels "Up" et "Down" avec les touches associées
    font = pygame.font.Font(None, 18)
    text_up_key = pygame.key.name(controls.get("up_key", 0))
    text_down_key = pygame.key.name(controls.get("down_key", 0))
    text_up = font.render(f"Up ({text_up_key})", True, (255, 255, 255))
    text_down = font.render(f"Down ({text_down_key})", True, (255, 255, 255))
    
    # Ajustement des positions pour aligner verticalement
    y_up = 335
    y_down = 355
    
    screen.blit(text_up, (x_position - text_up.get_width() // 2, y_up))
    screen.blit(text_down, (x_position - text_down.get_width() // 2, y_down))

def change_controls(controls, event):
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_UP:
            print("Appuyez sur une nouvelle touche pour 'Up'")
            new_key = wait_for_key()
            controls["up_key"] = new_key
        elif event.key == pygame.K_DOWN:
            print("Appuyez sur une nouvelle touche pour 'Down'")
            new_key = wait_for_key()
            controls["down_key"] = new_key

def wait_for_key():
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                return event.key

# Nouvelles fonctions pour gérer les événements de chaque joueur
def change_controls_player1(event):
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_UP:
            print("Appuyez sur une nouvelle touche pour 'Up' de Player 1")
            new_key = wait_for_key()
            player1_controls_azerty["up_key"] = new_key
        elif event.key == pygame.K_LEFT:
            print("Appuyez sur une nouvelle touche pour 'Down' de Player 1")
            new_key = wait_for_key()
            player1_controls_azerty["down_key"] = new_key

def change_controls_player2(event):
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_DOWN:
            print("Appuyez sur une nouvelle touche pour 'Down' de Player 2")
            new_key = wait_for_key()
            player2_controls_azerty["down_key"] = new_key
        elif event.key == pygame.K_RIGHT:
            print("Appuyez sur une nouvelle touche pour 'Up' de Player 2")
            new_key = wait_for_key()
            player2_controls_azerty["up_key"] = new_key

# Boucle principale
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Clic gauche
                # Vérification du clic sur les boutons de défilement
                if WIDTH // 4 - 80 <= event.pos[0] <= WIDTH // 4 - 50 and 80 <= event.pos[1] <= 130:
                    angle1 -= 10
                elif WIDTH // 4 + 50 <= event.pos[0] <= WIDTH // 4 + 80 and 80 <= event.pos[1] <= 130:
                    angle1 += 10
                elif WIDTH * 3 // 4 - 80 <= event.pos[0] <= WIDTH * 3 // 4 - 50 and 80 <= event.pos[1] <= 130:
                    angle2 -= 10
                elif WIDTH * 3 // 4 + 50 <= event.pos[0] <= WIDTH * 3 // 4 + 80 and 80 <= event.pos[1] <= 130:
                    angle2 += 10
        elif event.type in [pygame.KEYDOWN, pygame.KEYUP]:
            # Appeler la fonction appropriée en fonction du joueur
            if event.type == pygame.KEYDOWN:
                change_controls_player1(event)
                change_controls_player2(event)

    angle1 %= NUM_COLORS  # Assurez-vous que l'angle reste dans la plage 0-359
    angle2 %= NUM_COLORS
    screen.fill(BLACK)  # Efface l'écran pour dessiner les nouveaux sélecteurs
    draw_color_menu(angle1, WIDTH // 4, "Joueur 1", player1_controls_azerty)
    draw_color_menu(angle2, WIDTH * 3 // 4, "Joueur 2", player2_controls_azerty)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()

