import pygame

class Shuriken(pygame.sprite.Sprite):
    def __init__(self, x, y, direcao, *groups):
        super().__init__(*groups)

        img_original = pygame.image.load('Personagem/Shuriken.png')
        self.image_right = pygame.transform.scale(img_original, [20, 20])
        self.image_left = pygame.transform.flip(self.image_right, True, False)

        if direcao == "esquerda":
            self.image = self.image_left
            self.speed = -10
        else: # direita
            self.image = self.image_right
            self.speed = 10
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y

    def update(self, *args):
        # Move a shuriken
        self.rect.x += self.speed

        if self.rect.left > 900 or self.rect.right < 0:
            self.kill()