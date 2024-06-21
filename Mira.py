import pygame
import random
from assets.configs.config import MIRA, DISPARO, LARGURA, ALTURA
from alvo import Alvo

class Mira(pygame.sprite.Sprite): # sprite irá permitir combinar audio e animação 
    def __init__(self, pontuacao):
        super().__init__()
        self.image = pygame.image.load(MIRA).convert_alpha()
        self.image = pygame.transform.scale(self.image, (50,50))
        self.rect = self.image.get_rect() # O retângulo delimitador da mira.
        self.sound = pygame.mixer.Sound(DISPARO)
        self.pontuacao = pontuacao
    
    # atualiza a posição da mira
    def update(self):   #predefinido pela Sprite
        self.rect.center = pygame.mouse.get_pos()
    
    # Retorna um booleano indicando se o "disparo" acertou um alvo.
    def shoot(self, grupo_de_alvos):
        self.sound.play()
        
        # armazenando o grupo_de_alvos que estão colidindo com a mira
        colisions = pygame.sprite.spritecollide(self, grupo_de_alvos, False)
        if colisions:
            self.pontuacao.adicionar_ponto()
            for colision in colisions:
                colision.kill()
                
                while len(grupo_de_alvos) < 6:  # Garante que sempre haja 6 alvos na tela
                    novo_alvo = Alvo(random.randrange(0, LARGURA), random.randrange(0, ALTURA)) #só pode desenhar em grupos (conjunto)
                    grupo_de_alvos.add(novo_alvo)
            return True # se conseguiu armazenar....Retornando True se colidiu com o alvo 
        return False  # se não conseguiu armazenar....Retornando False pois não teve colisão
        