import pygame
import random
import os
import sys

pygame.init()

size = width, height = 865, 630
screen = pygame.display.set_mode(size)


def load_image(name, color_key=None):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname).convert()
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)

    if color_key is not None:
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    else:
        image = image.convert_alpha()
    return image


class Hero(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(all_sprites)
        self.hero_imagetl = load_image('Вверх влево.png', -1)
        self.hero_imagetr = load_image('Вверх вправо.png', -1)
        self.hero_imagebl = load_image('Вниз влево.png', -1)
        self.hero_imagebr = load_image('Вниз вправо.png', -1)
        self.image = self.hero_imagetl
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.move_ip(280, 290)
        self.top = True
        self.bottom = False

    def update(self):
        key = pygame.key.get_pressed()
        if key[pygame.K_DOWN]:
            self.top = False
            self.bottom = True
            if self.rect.left == 280:
                self.image = self.hero_imagebl
                self.mask = pygame.mask.from_surface(self.image)
            if self.rect.left == 470:
                self.image = self.hero_imagebr
                self.mask = pygame.mask.from_surface(self.image)
        elif key[pygame.K_UP]:
            self.top = True
            self.bottom = False
            if self.rect.left == 280:
                self.image = self.hero_imagetl
                self.mask = pygame.mask.from_surface(self.image)
            if self.rect.left == 470:
                self.image = self.hero_imagetr
                self.mask = pygame.mask.from_surface(self.image)
        if key[pygame.K_RIGHT]:
            if self.rect.left == 280:
                self.rect.move_ip(190, 0)
            if self.top:
                self.image = self.hero_imagetr
                self.mask = pygame.mask.from_surface(self.image)
            if self.bottom:
                self.image = self.hero_imagebr
                self.mask = pygame.mask.from_surface(self.image)
        elif key[pygame.K_LEFT]:
            if self.rect.left == 470:
                self.rect.move_ip(-190, 0)
            if self.top:
                self.image = self.hero_imagetl
                self.mask = pygame.mask.from_surface(self.image)
            if self.bottom:
                self.image = self.hero_imagebl
                self.mask = pygame.mask.from_surface(self.image)


class Shelves(pygame.sprite.Sprite):
    image = load_image("жердочки.png", -1)

    def __init__(self):
        super().__init__(all_sprites)
        self.image = Shelves.image
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.bottom = 500


class Earth(pygame.sprite.Sprite):
    image = load_image("фон новый.png", -1)

    def __init__(self):
        super().__init__(all_sprites)
        self.image = Earth.image
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.bottom = height


class Count():
    count = 0
    countrazb = 0


class Drop(pygame.sprite.Sprite):
    image = load_image("яйцо.png", -1)
    img1 = load_image("яйцо вправо.png", -1)
    img2 = load_image("яйцо вниз.png", -1)
    img3 = load_image("яйцо влево.png", -1)

    def __init__(self, pos):
        super().__init__(yaca)
        self.pos = pos
        self.image = Drop.image
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.cp = 0
        self.cl = 0
        self.spp = [Drop.image, Drop.img1, Drop.img2, Drop.img3]
        self.spl = [Drop.image, Drop.img3, Drop.img2, Drop.img1]
        self.razb = False

    def update(self):
        if not pygame.sprite.collide_mask(self, shelf):
            self.rect = self.rect.move(0, 1)
        if pygame.sprite.collide_mask(self, shelf) and self.pos[0] < 430:
            self.rect = self.rect.move(1, 0)
            self.cp += 1
            if self.cp == 40:
                self.cp = 0
            self.image = self.spp[self.cp // 10]
        if pygame.sprite.collide_mask(self, shelf) and self.pos[0] > 430:
            self.rect = self.rect.move(-1, 0)
            self.cl += 1
            if self.cl == 40:
                self.cl = 0
            self.image = self.spl[self.cl // 10]
        if pygame.sprite.collide_mask(self, earth):
            self.kill()
            Count.countrazb += 1
            print(f'Разбито яиц: {Count.countrazb}')
            self.razb = True
            self.rect = self.rect.move(0, -1)
        if pygame.sprite.collide_mask(self, hero) and not self.razb:
            self.kill()
            Count.count += 1
            print(f'поймано яиц: {Count.count}')


screen_size = (865, 630)
FPS = 50
clock = pygame.time.Clock()


def terminate():
    pygame.quit()
    sys.exit


def start_screen():
    intro_text = ["Управление героем производится стрелочками"]

    fon = pygame.transform.scale(load_image('img.png'), screen_size)
    screen.blit(fon, (0, 0))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()
        clock.tick(FPS)


start_screen()
all_sprites = pygame.sprite.Group()
yaca = pygame.sprite.Group()

shelf = Shelves()
earth = Earth()
hero = Hero()

yc = Drop((135, 210))
yaca.add(yc)
all_sprites.add(yc)

sps = 70
spawn = 0
running = True
coords = [(135, 210), (135, 310), (725, 215), (725, 315)]

dist = 10
count = 0

pygame.mixer.music.load('data/music.wav')
pygame.mixer.music.play(-1)

font = pygame.font.SysFont('Consolas', 35)

while running:
    if Count.countrazb == 3:
        running = False
    c = random.randint(0, 3)
    coord = coords[c]
    spawn += 1
    if spawn == 1500:
        sps = 50
    if spawn == 3500:
        sps = 40
    if spawn % sps == 0:
        yc = Drop(coord)
        all_sprites.add(yc)
        yaca.add(yc)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    hits = pygame.sprite.collide_mask(yc, hero)
    if hits:
        yc.kill()
        count += 1
        print(count)
    screen.fill(pygame.Color(0, 191, 255))
    screen.blit(font.render(str(Count.count), True, (22, 1, 238)), (690, 30))
    screen.blit(font.render(str(Count.countrazb), True, (238, 4, 28)), (690, 78))
    all_sprites.draw(screen)
    all_sprites.update()
    pygame.display.flip()
    clock.tick(50)
pygame.quit()
