import pygame

# Initialisation de Pygame
pygame.init()

# Définition des variables
WIDTH, HEIGHT = 800, 600
FPS = 60
PADDLE_WIDTH, PADDLE_HEIGHT = 20, 100
BALL_SIZE = 20
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 0, 255)

# Création de la fenêtre
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong Game")

# Initialisation des positions des raquettes et de la balle
player1_y = HEIGHT // 2 - PADDLE_HEIGHT // 2
player2_y = HEIGHT // 2 - PADDLE_HEIGHT // 2
ball_x, ball_y = WIDTH // 2, HEIGHT // 2
ball_speed_x, ball_speed_y = 5, 5

# Ajout de variables pour les points
player1_score = 0
player2_score = 0

# Couleurs des raquettes
player1_color = RED
player2_color = GREEN

# État du jeu (menu, en cours d'exécution, paramètres)
game_state = "menu"

# Contrôles des joueurs (clavier AZERTY et QWERTY)
player1_controls_azerty = {pygame.K_z: -5, pygame.K_s: 5}
player1_controls_qwerty = {pygame.K_w: -5, pygame.K_s: 5}
player2_controls_azerty = {pygame.K_UP: -5, pygame.K_DOWN: 5}
player2_controls_qwerty = {pygame.K_w: -5, pygame.K_s: 5}

# Boucle principale du jeu
clock = pygame.time.Clock()
running = True
paused = False

def reset_ball():
    return WIDTH // 2, HEIGHT // 2

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
        # Si le jeu est en pause, ne pas mettre à jour les mouvements
        clock.tick(FPS)
        continue

    # Mouvements des raquettes
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
        # Affichage du menu
        screen.fill(BLACK)
        font = pygame.font.Font(None, 36)
        play_option = font.render("Jouer", True, WHITE)
        settings_option = font.render("Paramètres", True, WHITE)

        # Affichage des options
        screen.blit(play_option, (WIDTH // 2 - 40, HEIGHT // 2 - 20))
        screen.blit(settings_option, (WIDTH // 2 - 70, HEIGHT // 2 + 20))

        # Vérification des clics pour choisir une option
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if WIDTH // 2 - 40 < mouse_x < WIDTH // 2 + 40 and HEIGHT // 2 - 20 < mouse_y < HEIGHT // 2 + 10:
                game_state = "playing"
            elif WIDTH // 2 - 70 < mouse_x < WIDTH // 2 + 70 and HEIGHT // 2 + 20 < mouse_y < HEIGHT // 2 + 60:
                game_state = "settings"

    elif game_state == "playing":
        # Dessin sur l'écran pendant le jeu
        screen.fill(BLACK)
        pygame.draw.rect(screen, player1_color, (0, player1_y, PADDLE_WIDTH, PADDLE_HEIGHT))
        pygame.draw.rect(screen, player2_color, (WIDTH - PADDLE_WIDTH, player2_y, PADDLE_WIDTH, PADDLE_HEIGHT))
        pygame.draw.ellipse(screen, WHITE, (ball_x, ball_y, BALL_SIZE, BALL_SIZE))

        # Affichage des scores
        font = pygame.font.Font(None, 36)
        score_display = font.render(f"{player1_score} - {player2_score}", True, WHITE)
        screen.blit(score_display, (WIDTH // 2 - 40, 20))

        # Gestion des mouvements
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

        # Mouvement de la balle
        ball_x += ball_speed_x
        ball_y += ball_speed_y

        # Rebondissement de la balle sur les murs
        if ball_y <= 0 or ball_y >= HEIGHT - BALL_SIZE:
            ball_speed_y = -ball_speed_y

        # Collision avec les raquettes
        if (
            (ball_x <= PADDLE_WIDTH and player1_y <= ball_y <= player1_y + PADDLE_HEIGHT)
            or (ball_x >= WIDTH - PADDLE_WIDTH - BALL_SIZE and player2_y <= ball_y <= player2_y + PADDLE_HEIGHT)
        ):
            ball_speed_x = -ball_speed_x

        # Gestion des points
        if ball_x <= 0:
            player2_score += 1
            ball_x, ball_y = reset_ball()

        elif ball_x >= WIDTH - BALL_SIZE:
            player1_score += 1
            ball_x, ball_y = reset_ball()

        # Vérifier si l'un des joueurs a atteint 5 points
        if player1_score == 5 or player2_score == 5:
            running = False

    elif game_state == "settings":
        # Affichage des paramètres
        screen.fill(BLACK)
        font = pygame.font.Font(None, 36)
        back_option = font.render("Retour", True, WHITE)

        # Affichage des options de contrôles
        player1_controls_option = font.render("Controle Joueur 1 (AZERTY): Z, S", True, WHITE)
        player2_controls_option = font.render("Controle Joueur 1 (QWERTY): W, S", True, WHITE)

        # Affichage des options de contrôles pour QWERTY (optionnel)
        player1_controls_option_qwerty = font.render("Controle Joueur 2 (AZERTY): UP, DOWN", True, WHITE)
        player2_controls_option_qwerty = font.render("Controle Joueur 2 (QWERTY): UP, DOWN", True, WHITE)

        # Affichage des options
        screen.blit(player1_controls_option, (WIDTH // 4, HEIGHT // 2 - 20))
        screen.blit(player2_controls_option, (WIDTH // 4, HEIGHT // 2 + 20))

        # Affichage des options QWERTY (optionnel)
        screen.blit(player1_controls_option_qwerty, (WIDTH // 4, HEIGHT // 2 + 60))
        screen.blit(player2_controls_option_qwerty, (WIDTH // 4, HEIGHT // 2 + 100))

        screen.blit(back_option, (WIDTH // 2 - 40, HEIGHT - 50))

        # Vérification des clics pour choisir une option
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if WIDTH // 2 - 40 < mouse_x < WIDTH // 2 + 40 and HEIGHT - 50 < mouse_y < HEIGHT - 30:
                game_state = "menu"

    # Actualisation de l'écran
    pygame.display.flip()

    clock.tick(FPS)

# Quitter Pygame
pygame.quit()
