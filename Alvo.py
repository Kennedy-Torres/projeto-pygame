import pygame
from assets.configs.config import ALVO

class Alvo(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__()
        self.image = pygame.image.load(ALVO).convert_alpha()
        self.image = pygame.transform.scale(self.image, (100,100))
        self.rect = self.image.get_rect()
        self.rect.center = [pos_x, pos_y]