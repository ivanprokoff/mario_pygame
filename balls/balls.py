import pygame
import random


all_sprites = pygame.sprite.Group()
vertical_borders = pygame.sprite.Group()
horizontal_borders = pygame.sprite.Group()


class Border(pygame.sprite.Sprite):
    # строго вертикальный или строго горизонтальный отрезок
    def __init__(self, x1, y1, x2, y2):
        super().__init__(all_sprites)
        if x1 == x2:  # вертикальная стенка
            self.add(vertical_borders)
            self.image = pygame.Surface([1, y2 - y1])
            self.rect = pygame.Rect(x1, y1, 1, y2 - y1)
        else:  # горизонтальная стенка
            self.add(horizontal_borders)
            self.image = pygame.Surface([x2 - x1, 1])
            self.rect = pygame.Rect(x1, y1, x2 - x1, 1)


class Ball(pygame.sprite.Sprite):
    def __init__(self, radius, pos):
        super().__init__(all_sprites)
        self.radius = radius
        self.x = pos[0]
        self.y = pos[1]
        self.image = pygame.Surface((2 * radius, 2 * radius),
                                    pygame.SRCALPHA, 32)
        pygame.draw.circle(self.image, pygame.Color("white"),
                           (radius, radius), radius)
        self.rect = pygame.Rect(self.x, self.y, 2 * radius, 2 * radius)
        self.vx = -5
        self.vy = -5

    def update(self):
        self.rect = self.rect.move(self.vx, self.vy)
        if pygame.sprite.spritecollideany(self, horizontal_borders):
            self.vy = -self.vy
        if pygame.sprite.spritecollideany(self, vertical_borders):
            self.vx = -self.vx


pygame.init()
pygame.display.set_caption('Шарики')
size = 600, 500
V = 100
screen = pygame.display.set_mode(size)
screen.fill(pygame.Color('black'))
clock = pygame.time.Clock()
running = True
Border(0, 0, 600, 0)
Border(0, 500, 600, 500)
Border(0, 0, 0, 500)
Border(600, 0, 600, 500)
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = event.pos
            ball = Ball(10, pos)
            all_sprites.add(ball)
    all_sprites.update()
    screen.fill(pygame.Color('black'))
    all_sprites.draw(screen)
    pygame.display.flip()
    clock.tick(V)
