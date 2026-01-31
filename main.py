import pygame
import sys
import random

pygame.init()

# --------------------
# TELA
# --------------------
WIDTH, HEIGHT = 800, 450
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dino Clone")

clock = pygame.time.Clock()
FPS = 60

# --------------------
# CONSTANTES
# --------------------
GROUND_Y = 360
font = pygame.font.SysFont(None, 36)

# --------------------
# IMAGENS
# --------------------
background = pygame.image.load("assets/background.png").convert()
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

menu_img = pygame.image.load("assets/TELA INICIAL.png").convert()
menu_img = pygame.transform.scale(menu_img, (WIDTH, HEIGHT))

gameover_img = pygame.image.load("assets/TELA FINAL.png").convert()
gameover_img = pygame.transform.scale(gameover_img, (WIDTH, HEIGHT))

player_img = pygame.image.load("assets/correndo 1.png").convert_alpha()
player_img = pygame.transform.scale(player_img, (80, 80))

obs_pequeno_img = pygame.image.load("assets/sacos de lixo.png").convert_alpha()
obs_pequeno_img = pygame.transform.scale(obs_pequeno_img, (50, 50))

item_img = pygame.image.load("assets/sublinha parte 2.png").convert_alpha()
item_img = pygame.transform.scale(item_img, (35, 35))

# --------------------
# PLAYER
# --------------------
player = pygame.Rect(100, GROUND_Y - 80, 80, 80)
vel_y = 0
gravity = 1
jump_force = -18
on_ground = True

# --------------------
# OBSTÁCULOS
# --------------------
obstaculos = []
spawn_timer = 0

def spawn_obstaculo():
    tipo = random.choice(["pequeno", "grande"])

    if tipo == "pequeno":
        rect = pygame.Rect(WIDTH + 50, GROUND_Y - 50, 50, 50)
    else:
        rect = pygame.Rect(WIDTH + 50, GROUND_Y - 110, 60, 110)

    obstaculos.append((tipo, rect))

# --------------------
# ITEM COLETÁVEL
# --------------------
item = pygame.Rect(WIDTH + 400, GROUND_Y - 45, 35, 35)
itens_coletados = 0

# --------------------
# VARIÁVEIS DE JOGO
# --------------------
speed = 6
estado = "menu"

# --------------------
# RESET
# --------------------
def resetar_jogo():
    global vel_y, on_ground, speed, itens_coletados, obstaculos, spawn_timer

    player.x = 100
    player.bottom = GROUND_Y

    vel_y = 0
    on_ground = True

    obstaculos.clear()
    spawn_timer = 0

    item.x = WIDTH + random.randint(400, 700)
    item.bottom = GROUND_Y - 10

    speed = 6
    itens_coletados = 0

# --------------------
# LOOP PRINCIPAL
# --------------------
rodando = True
while rodando:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            rodando = False

    # ====================
    # MENU
    # ====================
    if estado == "menu":
        screen.blit(menu_img, (0, 0))

        txt = font.render("Pressione ESPAÇO para começar", True, (255, 255, 255))
        screen.blit(txt, (WIDTH//2 - txt.get_width()//2, 360))

        pygame.display.flip()

        if pygame.key.get_pressed()[pygame.K_SPACE]:
            resetar_jogo()
            estado = "jogando"
        continue

    # ====================
    # GAME OVER
    # ====================
    if estado == "game_over":
        screen.blit(gameover_img, (0, 0))

        t1 = font.render(f"Itens coletados: {itens_coletados}", True, (255, 255, 255))
        t2 = font.render("Pressione R para reiniciar", True, (255, 255, 255))

        screen.blit(t1, (WIDTH//2 - t1.get_width()//2, 300))
        screen.blit(t2, (WIDTH//2 - t2.get_width()//2, 340))

        pygame.display.flip()

        if pygame.key.get_pressed()[pygame.K_r]:
            resetar_jogo()
            estado = "jogando"
        continue

    # ====================
    # JOGANDO
    # ====================
    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE] and on_ground:
        vel_y = jump_force
        on_ground = False

    # FÍSICA
    vel_y += gravity
    player.y += vel_y

    if player.bottom >= GROUND_Y:
        player.bottom = GROUND_Y
        vel_y = 0
        on_ground = True

    # OBSTÁCULOS
    spawn_timer += 1
    if spawn_timer > 90:
        spawn_obstaculo()
        spawn_timer = 0

    for obs in obstaculos[:]:
        obs[1].x -= speed

        if obs[1].right < 0:
            obstaculos.remove(obs)

        if player.colliderect(obs[1]):
            estado = "game_over"

    # ITEM
    item.x -= speed
    if item.right < 0:
        item.x = WIDTH + random.randint(400, 700)
        item.bottom = GROUND_Y - 10

    if player.colliderect(item):
        itens_coletados += 1
        item.x = WIDTH + random.randint(400, 700)
        item.bottom = GROUND_Y - 10

    speed = 6 + itens_coletados // 5

    # DESENHO
    screen.blit(background, (0, 0))
    screen.blit(player_img, player)

    for tipo, rect in obstaculos:
        if tipo == "pequeno":
            screen.blit(obs_pequeno_img, rect)
    
    screen.blit(item_img, item)

    hud = font.render(f"Itens: {itens_coletados}", True, (255, 255, 255))
    screen.blit(hud, (10, 10))

    pygame.display.flip()

pygame.quit()
sys.exit()
