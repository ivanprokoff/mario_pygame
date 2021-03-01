import pygame
import os


def load_image(name, color_key=None):
    # Функция загрузки изображения
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print('Невозможно загрузить изображение:', name)
        raise SystemExit(message)
    if color_key is not None:
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    return image


pygame.init()
pygame.display.set_caption('Game over')
background = load_image('gameover.png')
size = 600, 300
V = 200
screen = pygame.display.set_mode(size)
screen.fill(pygame.Color('blue'))
clock = pygame.time.Clock()
running = True
x = -500
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.blit(background, (x, 0))
    x += V * clock.tick() / 1000
    pygame.display.flip()
    if int(x) == 0:
        running = False
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
                running = False
    screen.blit(background, (10, 0))
