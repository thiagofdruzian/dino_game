import pygame
import os

pygame.init()

WIDTH, HEIGHT = 800, 400
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Jogo Dino")

FONT = pygame.font.SysFont('comicsans', 20)

def load_image(name, size):
    base_path = os.path.dirname(__file__)
    full_path = os.path.join(base_path, name)
    image = pygame.image.load(full_path).convert_alpha()
    return pygame.transform.scale(image, size)

# Imagens
DINO_RUN = [
    load_image("dino1.png", (60, 60)),
    load_image("dino2.png", (60, 60))
]
CACTUS = load_image("cactus.png", (40, 60))

GROUND_HEIGHT = 40

class Dino:
    def __init__(self):
        self.run_count = 0
        self.image = DINO_RUN[0]
        self.rect = self.image.get_rect()
        self.rect.x = 50
        self.rect.y = HEIGHT - GROUND_HEIGHT - self.rect.height
        self.is_jumping = False
        self.jump_vel = 8.5
        self.vel_y = self.jump_vel

    def update(self):
        if self.is_jumping:
            self.rect.y -= self.vel_y * 4
            self.vel_y -= 0.8
            if self.vel_y < -self.jump_vel:
                self.is_jumping = False
                self.vel_y = self.jump_vel
        else:
            # Corrige a posição para alinhar com o chão
            self.rect.y = HEIGHT - GROUND_HEIGHT - self.rect.height

            self.run_count += 1
            if self.run_count >= len(DINO_RUN) * 5:
                self.run_count = 0
            self.image = DINO_RUN[self.run_count // 5]

    def jump(self):
        if not self.is_jumping:
            self.is_jumping = True

    def draw(self, win):
        win.blit(self.image, (self.rect.x, self.rect.y))

class Cactus:
    def __init__(self):
        self.image = CACTUS
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH
        self.rect.y = HEIGHT - GROUND_HEIGHT - self.rect.height
        self.vel = 7

    def update(self):
        self.rect.x -= self.vel
        if self.rect.right < 0:
            self.rect.x = WIDTH  # Reseta a posição para direita

    def draw(self, win):
        win.blit(self.image, (self.rect.x, self.rect.y))

def draw_ground(win, night_mode):
    color = (83, 83, 83) if not night_mode else (200, 200, 200)
    pygame.draw.rect(win, color, (0, HEIGHT - GROUND_HEIGHT, WIDTH, GROUND_HEIGHT))

def draw_score(win, score, night_mode):
    color = (0, 0, 0) if not night_mode else (255, 255, 255)
    text = FONT.render(f"Score: {score}", True, color)
    win.blit(text, (WIDTH - 150, 20))

def main():
    clock = pygame.time.Clock()
    dino = Dino()
    cactus = Cactus()
    run = True
    score = 0
    night_mode = False
    night_trigger = 1000  # Pontuação para ativar o modo noite

    while run:
        clock.tick(30)

        # Ativa modo noite após atingir pontuação
        if score >= night_trigger:
            night_mode = True

        # Cor do fundo conforme modo dia/noite
        if night_mode:
            WIN.fill((20, 20, 40))
        else:
            WIN.fill((255, 255, 255))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            dino.jump()

        dino.update()
        cactus.update()

        score += 1

        draw_ground(WIN, night_mode)
        dino.draw(WIN)
        cactus.draw(WIN)
        draw_score(WIN, score, night_mode)

        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()
