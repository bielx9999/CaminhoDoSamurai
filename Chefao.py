import pygame
import random


class Chefao(pygame.sprite.Sprite):
    def __init__(self, samurai, *groups):
        super().__init__(*groups)

        img_original = pygame.image.load('Personagem/chefao.PNG')
        img_redimensionada = pygame.transform.scale(img_original, [160, 130])

        self.image_right = img_redimensionada
        self.image_left = pygame.transform.flip(img_redimensionada, True, False)

        self.samurai = samurai

        self.speed = 1.9

        lado = random.choice(["esquerda", "direita"])
        if lado == "direita":
            self.image = self.image_left
            self.rect = self.image.get_rect()
            self.rect.x = 950
        else:
            self.image = self.image_right
            self.rect = self.image.get_rect()
            self.rect.x = -200

        self.rect.bottom = 480

        self.vida = 10

        self.mask = pygame.mask.from_surface(self.image)

    def update(self, *args):
        if self.samurai.rect.centerx > self.rect.centerx:
            self.rect.x += self.speed
            self.image = self.image_right
        else:
            self.rect.x -= self.speed
            self.image = self.image_left

        self.mask = pygame.mask.from_surface(self.image)

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > 900:
            self.rect.right = 900