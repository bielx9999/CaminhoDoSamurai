import pygame
import random


class Inimigo(pygame.sprite.Sprite):
    def __init__(self, *groups):
        super().__init__(*groups)

        img_original = pygame.image.load('Personagem/goblin.png')
        img_redimensionada = pygame.transform.scale(img_original, [110, 80])

        self.image_right = img_redimensionada
        self.image_left = pygame.transform.flip(img_redimensionada, True, False)

        lado = random.choice(["esquerda", "direita"])

        self.speed = 1 + random.random() * 2

        if lado == "direita":
            self.image = self.image_left
            self.direcao = "esquerda"
            self.rect = self.image.get_rect()
            self.rect.x = random.randint(900, 1500)
            self.speed_x = -self.speed
        else:
            self.image = self.image_right
            self.direcao = "direita"
            self.rect = self.image.get_rect()
            self.rect.x = random.randint(-600, -100)
            self.speed_x = self.speed

        self.rect.bottom = 480

        self.mask = pygame.mask.from_surface(self.image)

    def update(self, *args):
        self.rect.x += self.speed_x

        if self.rect.right < -800 or self.rect.left > 1800:
            self.kill()