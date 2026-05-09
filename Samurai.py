import pygame

class Samurai(pygame.sprite.Sprite):
    def __init__(self, *groups):
        super().__init__(*groups)

        img_original = pygame.image.load('Personagem/Samurai/1x/attack_4.png')
        img_redimensionada = pygame.transform.scale(img_original, [120, 110])

        self.image_right = img_redimensionada
        self.image_left = pygame.transform.flip(img_redimensionada, True, False)

        self.image = self.image_right
        self.direcao = "direita"

        self.vidas = 3

        self.rect = pygame.Rect(50, 370, 120, 110)

        self.mask = pygame.mask.from_surface(self.image)

        self.speed_x = 0.4
        self.acceleration = 0.5

        self.speed_y = 0
        self.gravity = 1
        self.jump_force = -20
        self.on_ground = False

    def update(self, *args):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]:
            self.speed_x -= self.acceleration
            self.image = self.image_left
            self.direcao = "esquerda"

        elif keys[pygame.K_d]:
            self.speed_x += self.acceleration
            self.image = self.image_right
            self.direcao = "direita"

        else:
            self.speed_x *= 0.9

        self.rect.x += self.speed_x

        if keys[pygame.K_w] and self.on_ground:
            self.speed_y = self.jump_force
            self.on_ground = False

        self.speed_y += self.gravity
        self.rect.y += self.speed_y

        self.mask = pygame.mask.from_surface(self.image)

        if self.rect.left < 0:
            self.rect.left = 0
            self.speed_x = 0

        if self.rect.right > 900:
            self.rect.right = 900
            self.speed_x = 0

        if self.rect.top < 0:
            self.rect.top = 0
            self.speed_y = 0

        if self.rect.bottom > 480:
            self.rect.bottom = 480
            self.speed_y = 0
            self.on_ground = True