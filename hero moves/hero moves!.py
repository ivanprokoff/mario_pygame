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


all_sprites = pygame.sprite.Group()


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(all_sprites)
        self.pos_x = 0
        self.pos_y = 0
        self.image = player_image
        self.rect = self.image.get_rect().move(
            self.pos_x, self.pos_y)

    def update(self, pos):
        if pos == 'left':
            self.pos_x -= 10
            self.rect = self.image.get_rect().move(
                self.pos_x, self.pos_y)
        if pos == 'right':
            self.pos_x += 10
            self.rect = self.image.get_rect().move(
                self.pos_x, self.pos_y)
        if pos == 'up':
            self.pos_y -= 10
            self.rect = self.image.get_rect().move(
                self.pos_x, self.pos_y)
        if pos == 'down':
            self.pos_y += 10
            self.rect = self.image.get_rect().move(
                self.pos_x, self.pos_y)


player_image = load_image('creature.png')

tile_width = tile_height = 50

pygame.init()
pygame.display.set_caption('Перемещение героя')
size = 300, 300
screen = pygame.display.set_mode(size)
screen.fill(pygame.Color('white'))
fps = 10  # количество кадров в секунду
clock = pygame.time.Clock()
running = True

player = Player()
all_sprites.add(player)

while running:  # главный игровой цикл
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                all_sprites.update('left')
            if event.key == pygame.K_RIGHT:
                all_sprites.update('right')
            if event.key == pygame.K_UP:
                all_sprites.update('up')
            if event.key == pygame.K_DOWN:
                all_sprites.update('down')
        screen.fill(pygame.Color('white'))
        all_sprites.draw(screen)
    pygame.display.flip()  # смена кадра
    # изменение игрового мира
    # ...
    # временная задержка
    clock.tick(fps)
