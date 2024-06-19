import pygame
import random
from assets.configs.config import MIRA, DISPARO, LARGURA, ALTURA
from alvo import Alvo

class Mira(pygame.sprite.Sprite):
    def __init__(self, pontuacao):
        super().__init__()
        self.image = pygame.image.load(MIRA).convert_alpha()
        self.image = pygame.transform.scale(self.image, (50,50))
        self.rect = self.image.get_rect()
        self.sound = pygame.mixer.Sound(DISPARO)
        self.pontuacao = pontuacao
    
    def update(self):   #predefinido pela Sprite
        self.rect.center = pygame.mouse.get_pos()
    
    def shoot(self, grupo_de_alvos):
        self.sound.play()
        
        colisions = pygame.sprite.spritecollide(self, grupo_de_alvos, False)
        for colision in colisions:
            self.pontuacao.adicionar_ponto()
            
            colision.kill()
            while len(grupo_de_alvos) < 6:  # Garante que sempre haja 6 alvos na tela
                novo_alvo = Alvo(random.randrange(0, LARGURA), random.randrange(0, ALTURA)) #só pode desenhar em grupos (conjunto)
                grupo_de_alvos.add(novo_alvo)