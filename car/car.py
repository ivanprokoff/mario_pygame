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
vertical_borders = pygame.sprite.Group()


class Border(pygame.sprite.Sprite):
    # строго вертикальный или строго горизонтальный отрезок
    def __init__(self, x1, y1, x2, y2):
        super().__init__(all_sprites)
        if x1 == x2:  # вертикальная стенка
            self.add(vertical_borders)
            self.image = pygame.Surface([1, y2 - y1])
            self.rect = pygame.Rect(x1, y1, 1, y2 - y1)


class Car(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(all_sprites)
        self.pos_x = 1
        self.pos_y = 0
        self.image = car_image
        self.rect = self.image.get_rect().move(
            self.pos_x, self.pos_y)
        self.left = False
        self.n = 2

    def update(self):
        if self.left:
            self.pos_x -= V * clock.tick() / 1000
        elif not self.left:
            self.pos_x += V * clock.tick() / 1000
        self.rect = self.image.get_rect().move(
            self.pos_x, self.pos_y)
        if pygame.sprite.spritecollideany(self, vertical_borders):
            self.image = pygame.transform.flip(
                self.image, True, False)
            if self.n % 2 == 0:
                self.left = True
            else:
                self.left = False
            self.n += 1


car_image = load_image('car.png')

V = 50

pygame.init()
pygame.display.set_caption('Машинка')
size = 600, 95
screen = pygame.display.set_mode(size)
screen.fill(pygame.Color('white'))
clock = pygame.time.Clock()
running = True

Border(0, 0, 0, 95)
Border(600, 0, 600, 95)
car = Car()
all_sprites.add(car)

while running:  # главный игровой цикл
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill(pygame.Color('white'))
    all_sprites.update()
    all_sprites.draw(screen)
    pygame.display.flip()  # смена кадра
