import sys
import os

import pygame

FPS = 50
WIDTH = 500
HEIGHT = 500


def terminate():
    pygame.quit()
    sys.exit()


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


def start_screen():
    intro_text = ["Перемещение героя", "",
                  "Дополнительные уровни", 'Введите название', 'желаемого уровня в',
                                           'стандартный поток ввода']

    fon = pygame.transform.scale(load_image('fon.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return  # начинаем игру
        pygame.display.flip()
        clock.tick(FPS)


def load_level(filename):
    global running
    filename = "data/" + filename
    try:
        # читаем уровень, убирая символы перевода строки
        with open(filename, 'r') as mapFile:
            level_map = [line.strip() for line in mapFile]

        # и подсчитываем максимальную длину
        max_width = max(map(len, level_map))

        # дополняем каждую строку пустыми клетками ('.')
        return list(map(lambda x: x.ljust(max_width, '.'), level_map))
    except Exception:
        print('Неверный формат ввода или такого файла не существует.')
        print('Перезапустите игру и попробуйте еще раз')


# основной персонаж
player = None

# группы спрайтов
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
wall_tiles = pygame.sprite.Group()


def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y)
            elif level[y][x] == '#':
                BoxTile('wall', x, y)
            elif level[y][x] == '@':
                Tile('empty', x, y)
                new_player = Player(x, y)
    # вернем игрока, а также размер поля в клетках
    return new_player, x, y


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class BoxTile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(wall_tiles, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)
        self.mask = pygame.mask.from_surface(self.image)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.pos_x = pos_x * tile_width + 15
        self.pos_y = pos_y * tile_height + 5
        self.image = player_image
        self.rect = self.image.get_rect().move(
            self.pos_x, self.pos_y)
        self.mask = pygame.mask.from_surface(self.image)

    def update(self, pos):
        if pos == 'left':
            self.pos_x -= 50
            self.rect = self.image.get_rect().move(
                self.pos_x, self.pos_y)
            if pygame.sprite.spritecollideany(self, wall_tiles):
                self.pos_x += 50
                self.rect = self.image.get_rect().move(
                    self.pos_x, self.pos_y)
        if pos == 'right':
            self.pos_x += 50
            self.rect = self.image.get_rect().move(
                self.pos_x, self.pos_y)
            if pygame.sprite.spritecollideany(self, wall_tiles):
                self.pos_x -= 50
                self.rect = self.image.get_rect().move(
                    self.pos_x, self.pos_y)
        if pos == 'up':
            self.pos_y -= 50
            self.rect = self.image.get_rect().move(
                self.pos_x, self.pos_y)
            if pygame.sprite.spritecollideany(self, wall_tiles):
                self.pos_y += 50
                self.rect = self.image.get_rect().move(
                    self.pos_x, self.pos_y)
        if pos == 'down':
            self.pos_y += 50
            self.rect = self.image.get_rect().move(
                self.pos_x, self.pos_y)
            if pygame.sprite.spritecollideany(self, wall_tiles):
                self.pos_y -= 50
                self.rect = self.image.get_rect().move(
                    self.pos_x, self.pos_y)


tile_images = {
    'wall': load_image('box.png'),
    'empty': load_image('grass.png')
}
player_image = load_image('mar.png')

tile_width = tile_height = 50

pygame.init()
pygame.display.set_caption('Перемещение героя. Дополнительные уровни')
size = WIDTH, HEIGHT
screen = pygame.display.set_mode(size)
fps = 10  # количество кадров в секунду
clock = pygame.time.Clock()
running = True
pos = None
size = 1
first = True
success = True

while running:  # главный игровой цикл
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if first:
            start_screen()
            first = False
            level = load_level(input('Введите название уровня (в формате name.txt): '))
            if level:
                player, level_x, level_y = generate_level(level)
            else:
                screen.fill(pygame.Color('Black'))
                run = True
                intro_text = ["Произошла ошибка", "Перезапустите игру и попробуйте еще раз"]

                font = pygame.font.Font(None, 30)
                text_coord = 50
                for line in intro_text:
                    string_rendered = font.render(line, 1, pygame.Color('white'))
                    intro_rect = string_rendered.get_rect()
                    text_coord += 10
                    intro_rect.top = text_coord
                    intro_rect.x = 10
                    text_coord += intro_rect.height
                    screen.blit(string_rendered, intro_rect)

                while run:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            run = False
                    pygame.display.flip()
                    clock.tick(FPS)
        all_sprites.draw(screen)
        tiles_group.draw(screen)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player_group.update('left')
            if event.key == pygame.K_RIGHT:
                player_group.update('right')
            if event.key == pygame.K_UP:
                player_group.update('up')
            if event.key == pygame.K_DOWN:
                player_group.update('down')
        all_sprites.draw(screen)
        tiles_group.draw(screen)
        player_group.draw(screen)
    pygame.display.flip()  # смена кадра
    clock.tick(fps)
