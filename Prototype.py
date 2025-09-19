import pygame # type: ignore
import random

# Pygame initialisieren
pygame.init()

# Fenstergröße
window_width = 800
window_hight = 600
window = pygame.display.set_mode((window_width, window_hight))
pygame.display.set_caption("Pixel Bros.")

def save_highscore(highscore):
    with open("highscore.txt", "w") as file:
        file.write(str(highscore))

WHITE = (255, 255, 255)
GREEN = (0, 255, 31)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

def load_highscore():
    try:
        with open("highscore.txt", "r") as file:
            return int(file.read())
    except (FileNotFoundError, ValueError):
        return 0

pygame.font.init()
score_font = pygame.font.Font(None, 36)
start = pygame.font.Font(None, 120)

# Uhr für Framerate
clock = pygame.time.Clock()

# Spielfigur (Rechteck)
player_hight = 50
player_width = player_hight // 2
player_x = window_width // 2 - player_width // 2
player_y = 250
player_ges = 3

# Gegner Basis
enemy_hight = 25
enemy_width = 25
enemy_ges = 3

# Gegner 1
enemy1_x = 400
enemy1_y = 100
enemy1_direct = -1

# Gegner 2
enemy2_x = 300
enemy2_y = 220
enemy2_direct = 1

# Gegner 3
enemy3_x = 1
enemy3_y = 400
enemy3_direct = 1

# Gravitation
grav = 0.3

# Springen
player_vert_ges = 0.0
jump_power = -10

# Blöcke
block_gr_x = 250
block_gr_y = 10
block_UL = pygame.Rect(100, 450, block_gr_x, block_gr_y)
block_UR = pygame.Rect(450, 450, block_gr_x, block_gr_y)
block_MM = pygame.Rect(275, 300, block_gr_x, block_gr_y)
block_MR = pygame.Rect(650, 300, block_gr_x, block_gr_y)
block_ML = pygame.Rect(-100, 300, block_gr_x, block_gr_y)
block_OL = pygame.Rect(100, 150, block_gr_x, block_gr_y)
block_OR = pygame.Rect(450, 150, block_gr_x, block_gr_y)

blöcke = [block_UL, block_UR, block_MM, block_MR, block_ML, block_OL, block_OR]

# Bodenblöcke
floor_block_hight = 50
floor_block_y = window_hight - 40
floor_block_width = window_width // 3  # ein Drittel des Fensters
floor_block_rect1 = pygame.Rect(0, floor_block_y, floor_block_width, floor_block_hight)
floor_block_rect2 = pygame.Rect(window_width - floor_block_width, floor_block_y, floor_block_width,
                              floor_block_hight)

floor_blöcke = [floor_block_rect1, floor_block_rect2]

# Auf Boden oder Block
player_on_floor_or_block = False

# Game Over Zustand
game_over = False

# Münzen
coin_size = 20
coins = []
coinImg = pygame.image.load('gold-coin.png')

# Funktion zum Erzeugen von Münzen
def create_coins():
    new_coins = []
    for _ in range(5):  # 5 Münzen
        while True:
            coin_x = random.randint(0, window_width - coin_size)
            coin_y = random.randint(0, 400)  # Münzen nur im oberen Bereich generieren
            coin = pygame.Rect(coin_x, coin_y, coin_size, coin_size)
            coin.center = (coin_x + coin_size // 2, coin_y + coin_size // 2)
            # Überprüfe, ob die Münze mit einem Block kollidiert
            colide_with_block = False
            for block in blöcke + floor_blöcke:
                if coin.colliderect(block):
                    colide_with_block = True
                    break
            if not colide_with_block:
                new_coins.append(coin)
                break
    return new_coins

# Initialisiere Münzen
coins = create_coins()

coin_collect = 0
score = 0

# Spiel-Zustand hinzufügen
game_state = "start"  # Mögliche Zustände: "start", "playing"

# Spielschleife
game_aktiv = True
while game_aktiv:
    # Ereignisse verarbeiten
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_aktiv = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                if game_state == "start" or game_over:  # Neustart mit R-Taste
                    game_state = "playing"
                    game_over = False
                    score = 0
                    highscore = load_highscore()
                    player_x = window_width // 2 - player_width // 2
                    player_y = 250
                    player_vert_ges = 0
                    coins = create_coins()  # Erzeuge neue Münzen

    # Fensterhintergrund löschen
    window.fill((0, 0, 0))  # Schwarz

    if game_state == "start":
        # Startbildschirm anzeigen
        font = pygame.font.Font(None, 74)
        title = start.render("Pixel Bros.", True, RED)
        highscore = load_highscore()
        highscorescreen = str(highscore)
        startscore = score_font.render("Current Highscore: " + highscorescreen, True, YELLOW)
        start_text = score_font.render("Drücke 'R' zum Starten", True, YELLOW)  # Score Font verwenden
        window.blit(title, (window_width // 2 - title.get_width() // 2, 250))
        window.blit(startscore, (window_width // 2 - startscore.get_width() // 2, 150))
        window.blit(start_text, (window_width // 2 - start_text.get_width() // 2, 350))
    elif not game_over:  # Nur spielen, wenn nicht Game Over und im Spielzustand "playing"
        # Tastensteuerung
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT]:
            player_x -= player_ges
        if key[pygame.K_RIGHT]:
            player_x += player_ges

        # Schwerkraft anwenden
        player_vert_ges += grav
        player_y += player_vert_ges

        # Gegner bewegen
        enemy1_x += enemy_ges * enemy1_direct
        if enemy1_x <= 0:
            enemy1_direct = 1
        elif enemy1_x >= window_width - enemy_width:
            enemy1_direct = -1

        # Gegner bewegen
        enemy2_x += enemy_ges * enemy2_direct
        if enemy2_x <= 0:
            enemy2_direct = 1
        elif enemy2_x >= window_width - enemy_width:
            enemy2_direct = -1

        # Gegner bewegen
        enemy3_x += enemy_ges * enemy3_direct
        if enemy3_x <= 0:
            enemy3_direct = 1
        elif enemy3_x >= window_width - enemy_width:
            enemy3_direct = -1

        # Kollision
        player_rect = pygame.Rect(player_x, player_y, player_width, player_hight)
        enemy1_rect = pygame.Rect(enemy1_x, enemy1_y, enemy_width, enemy_hight)
        enemy2_rect = pygame.Rect(enemy2_x, enemy2_y, enemy_width, enemy_hight)
        enemy3_rect = pygame.Rect(enemy3_x, enemy3_y, enemy_width, enemy_hight)

        # Kollisionsprüfung mit Gegnern
        if player_rect.colliderect(enemy1_rect) or \
                player_rect.colliderect(enemy2_rect) or \
                player_rect.colliderect(enemy3_rect):
            game_over = True
            if game_over:
                if score > highscore:
                    highscore = score
                    save_highscore(highscore)
            


            

        # Kollisionsbehandlung
        if player_rect.colliderect(block_UL):
            # Kollisionsbehandlung (playerposition anpassen)
            if player_rect.bottom >= block_UL.top and player_vert_ges >= 0:
                player_y = block_UL.top - player_hight
                player_vert_ges = 0
                player_on_floor_or_block = True
            elif player_rect.top <= block_UL.bottom and player_vert_ges <= 0:
                player_y = block_UL.bottom
                player_vert_ges = 0
            elif player_rect.right >= block_UL.left and player_ges >= 0:
                player_x = block_UL.left - player_width
            elif player_rect.left <= block_UL.right and player_ges <= 0:
                player_x = block_UL.right

        elif player_rect.colliderect(block_UR):
            # Kollisionsbehandlung (playerposition anpassen)
            if player_rect.bottom >= block_UR.top and player_vert_ges >= 0:
                player_y = block_UR.top - player_hight
                player_vert_ges = 0
                player_on_floor_or_block = True
            elif player_rect.top <= block_UR.bottom and player_vert_ges <= 0:
                player_y = block_UR.bottom
                player_vert_ges = 0
            elif player_rect.right >= block_UR.left and player_ges >= 0:
                player_x = block_UR.left - player_width
            elif player_rect.left <= block_UR.right and player_ges <= 0:
                player_x = block_UR.right

        elif player_rect.colliderect(block_MM):
            # Kollisionsbehandlung (playerposition anpassen)
            if player_rect.bottom >= block_MM.top and player_vert_ges >= 0:
                player_y = block_MM.top - player_hight
                player_vert_ges = 0
                player_on_floor_or_block = True
            elif player_rect.top <= block_MM.bottom and player_vert_ges <= 0:
                player_y = block_MM.bottom
                player_vert_ges = 0
            elif player_rect.right >= block_MM.left and player_ges >= 0:
                player_x = block_MM.left - player_width
            elif player_rect.left <= block_MM.right and player_ges <= 0:
                player_x = block_MM.right

        elif player_rect.colliderect(block_MR):
            # Kollisionsbehandlung (playerposition anpassen)
            if player_rect.bottom >= block_MR.top and player_vert_ges >= 0:
                player_y = block_MR.top - player_hight
                player_vert_ges = 0
                player_on_floor_or_block = True
            elif player_rect.top <= block_MR.bottom and player_vert_ges <= 0:
                player_y = block_MR.bottom
                player_vert_ges = 0
            elif player_rect.right >= block_MR.left and player_ges >= 0:
                player_x = block_MR.left - player_width
            elif player_rect.left <= block_MR.right and player_ges <= 0:
                player_x = block_MR.right

        elif player_rect.colliderect(block_ML):
            # Kollisionsbehandlung (playerposition anpassen)
            if player_rect.bottom >= block_ML.top and player_vert_ges >= 0:
                player_y = block_ML.top - player_hight
                player_vert_ges = 0
                player_on_floor_or_block = True
            elif player_rect.top <= block_ML.bottom and player_vert_ges <= 0:
                player_y = block_ML.bottom
                player_vert_ges = 0
            elif player_rect.right >= block_ML.left and player_ges >= 0:
                player_x = block_ML.left - player_width
            elif player_rect.left <= block_ML.right and player_ges <= 0:
                player_x = block_ML.right

        elif player_rect.colliderect(block_OL):
            # Kollisionsbehandlung (playerposition anpassen)
            if player_rect.bottom >= block_OL.top and player_vert_ges >= 0:
                player_y = block_OL.top - player_hight
                player_vert_ges = 0
                player_on_floor_or_block = True
            elif player_rect.top <= block_OL.bottom and player_vert_ges <= 0:
                player_y = block_OL.bottom
                player_vert_ges = 0
            elif player_rect.right >= block_OL.left and player_ges >= 0:
                player_x = block_OL.left - player_width
            elif player_rect.left <= block_OL.right and player_ges <= 0:
                player_x = block_OL.right

        elif player_rect.colliderect(block_OR):
            # Kollisionsbehandlung (playerposition anpassen)
            if player_rect.bottom >= block_OR.top and player_vert_ges >= 0:
                player_y = block_OR.top - player_hight
                player_vert_ges = 0
                player_on_floor_or_block = True
            elif player_rect.top <= block_OR.bottom and player_vert_ges <= 0:
                player_y = block_OR.bottom
                player_vert_ges = 0
            elif player_rect.right >= block_OR.left and player_ges >= 0:
                player_x = block_OR.left - player_width
            elif player_rect.left <= block_OR.right and player_ges <= 0:
                player_x = block_OR.right

        elif player_rect.colliderect(floor_block_rect1) or player_rect.colliderect(floor_block_rect2):
            player_y = floor_block_y - player_hight
            player_vert_ges = 0
            player_on_floor_or_block = True

        else:
            if player_on_floor_or_block:
                player_on_floor_or_block = False

        # Münzen einsammeln
        for coin in coins:
            if player_rect.colliderect(coin):
                coins.remove(coin)
                score += 1

        # Nach dem Einsammeln prüfen:
        if len(coins) == 0:
            coins = create_coins()

        # Springen
        if key[pygame.K_SPACE] and player_on_floor_or_block:
            player_vert_ges = jump_power

        # Spielfigur innerhalb des Fensters halten
        player_x = max(0, min(player_x, window_width - player_width))

        # Game Over Bedingung
        if player_y > window_hight:
            game_over = True
            new_score = False
            if game_over:
                if score > highscore:
                    new_score = True
                    highscore = score
                    save_highscore(highscore)
            
        elif player_y > floor_block_y and (
                player_x < floor_block_width or player_x > window_width - floor_block_width - player_width
        ):
            game_over = True
            if game_over:
                if score > highscore:
                    highscore = score
                    save_highscore(highscore)
            

        # Spielfigur zeichnen
        pygame.draw.rect(window, (255, 0, 0), (player_x, player_y, player_width, player_hight))  # Rot

        # Gegner zeichnen
        pygame.draw.rect(window, (64, 64, 255), (enemy1_x, enemy1_y, enemy_width, enemy_hight))
        pygame.draw.rect(window, (64, 64, 255), (enemy2_x, enemy2_y, enemy_width, enemy_hight))
        pygame.draw.rect(window, (64, 64, 255), (enemy3_x, enemy3_y, enemy_width, enemy_hight))

        # Blöcke zeichnen
        pygame.draw.rect(window, (42, 255, 255), (450, 450, block_gr_x, block_gr_y))  # Block UR
        pygame.draw.rect(window, (42, 255, 255), (100, 450, block_gr_x, block_gr_y))  # Block UL
        pygame.draw.rect(window, (42, 255, 255), (275, 300, block_gr_x, block_gr_y))  # Block MM
        pygame.draw.rect(window, (42, 255, 255), (650, 300, block_gr_x, block_gr_y))  # Block MR
        pygame.draw.rect(window, (42, 255, 255), (-100, 300, block_gr_x, block_gr_y))  # Block ML
        pygame.draw.rect(window, (42, 255, 255), (100, 150, block_gr_x, block_gr_y))  # Block OL
        pygame.draw.rect(window, (42, 255, 255), (450, 150, block_gr_x, block_gr_y))  # Block OR

        pygame.draw.rect(window, (165, 42, 42),
                         (0, floor_block_y, floor_block_width, floor_block_hight))  # Bodenblock Braun

        pygame.draw.rect(window, (165, 42, 42), (window_width - floor_block_width, floor_block_y,
                                                    floor_block_width,
                                                    floor_block_hight, ))  # Bodenblock Braun
        # Münzen zeichnen
        for coin in coins:
            window.blit(coinImg, coin)  

        if score <= highscore:
            score_text = score_font.render(f"Score: {score}", True, WHITE)
        else:
            score_text = score_font.render(f"Score: {score}", True, GREEN)
        highscore_text = score_font.render(f"Highscore: {highscore}", True, WHITE)
        window.blit(score_text, (10, 10))
        window.blit(highscore_text, (10, 40))

    else:
        # Game Over Bildschirm anzeigen
        font = pygame.font.Font(None, 74)
        font2 = pygame.font.Font(None, 40)
        coin_collect = 0
        gameover = font.render("Game Over", 1, (255, 0, 0))
        gameover_score = font2.render('Your score is ' + str(score) + " Coins!", 2, (255, 255, 0))
        restart = font2.render("Press 'R' to Restart!", 1, (255, 0, 0))
        gameover_rect = gameover.get_rect(center=(window_width // 2, window_hight // 2))
        restart_rect = restart.get_rect(center=(window_width // 2, window_hight // 1.2))
        gameover_score_rect = gameover_score.get_rect(center=(window_width // 2, window_hight // 5))
        window.blit(gameover, gameover_rect)
        window.blit(restart, restart_rect)
        window.blit(gameover_score, gameover_score_rect)

    # Fenster aktualisieren
    pygame.display.flip()

    # Framerate begrenzen
    clock.tick(120)

# Pygame beenden
pygame.quit()
