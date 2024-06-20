import pygame
import random
import sys 
from assets.configs.config import LARGURA, ALTURA, BG, FONTE, TIMER, GAME_PAUSED, FINALIZAR
from alvo import Alvo
from mira import Mira
from pontuacao import Pontuacao


pygame.init()

screen = pygame.display.set_mode((LARGURA,ALTURA))

bg =  pygame.image.load(BG).convert() #convert ajuda na adqueção da imagem
bg = pygame.transform.scale(bg, (LARGURA,ALTURA))

clock = pygame.time.Clock()

font = pygame.font.Font(FONTE, 30)

pygame.display.set_caption('Tiro ao alvo')

def menu():
    while True:
        screen.fill((0, 0, 0))
        
        title = font.render('Tiro ao Alvo', True, (255, 255, 255))
        start_button = font.render('Start', True, (255, 255, 255))
        
        title_rect = title.get_rect(center=(LARGURA / 2, ALTURA / 2 - 100))
        start_button_rect = start_button.get_rect(center=(LARGURA / 2, ALTURA / 2))
        
        screen.blit(title, title_rect)
        screen.blit(start_button, start_button_rect)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button_rect.collidepoint(event.pos):
                    return  # Sai do menu e inicia o jogo

        pygame.display.flip()
        clock.tick(60)

def mini_game():
    global GAME_PAUSED, FINALIZAR, TIMER
     
    grupo_de_alvos = pygame.sprite.Group()

    # Inicia o jogo com exatamente 6 alvos
    for i in range(6):
        alvo = Alvo(random.randrange(0,LARGURA),random.randrange(0,ALTURA)) #só pode desenhar em grupos (conjunto)
        grupo_de_alvos.add(alvo)

    pontuacao = Pontuacao()    
    mira = Mira(pontuacao)
    mira_group = pygame.sprite.Group()
    mira_group.add(mira)


    while not FINALIZAR:
        
        
        if not GAME_PAUSED:
            
            pygame.mouse.set_visible(False)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                    
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE: #esc
                        GAME_PAUSED = not GAME_PAUSED
                    
                # se acertar o alvo incrementa tempo extra no tempo total, se errar decrementa
                if event.type == pygame.MOUSEBUTTONDOWN:
                    hit_target = mira.shoot(grupo_de_alvos)
                    if hit_target:
                        TIMER += 30  # Adiciona 0.5 segundos ao TIMER (0.5s * 60 frames)
                    else:
                        TIMER -= 30  # Remove 0.5 segundos do TIMER (0.5s * 60 frames)
                    
            screen.blit(bg, (0,0))
            grupo_de_alvos.draw(screen)
                
            mira_group.draw(screen)
            mira_group.update()
                
            score = font.render(f' Pontos: {int(pontuacao.pontos)} ', True, (0,0,0))
            screen.blit(score, (50,50))
                
            tempo = font.render(f'Tempo: {TIMER/60:.1f} s',True, (0,0,0))
            screen.blit(tempo, (50,100))
                
            TIMER -=1
                
            if TIMER < 0:
                TIMER = 600
                
                pontuacao.atualizar_recorde()
                #pontuacao.resetar_pontos()
                #GAME_PAUSED = not GAME_PAUSED
                GAME_PAUSED = True
                
        else:
            screen.fill((252, 132, 3))
            pygame.mouse.set_visible(True)
            for event in pygame.event.get():
        
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE: #esc
                        pontuacao.resetar_pontos()
                        TIMER = 600
                        GAME_PAUSED = False
                        #GAME_PAUSED = not GAME_PAUSED

                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                    
            pause = font.render(f"PRESSIONE ESC PARA INICIAR   ",True, (255,255,255))
            points = font.render(f"RECORDE: {pontuacao.recorde} ",True, (255,255,255))
            last_score = font.render(f"PONTOS NA PARTIDA: {pontuacao.pontos} ", True, (255, 255, 255))
            
            pause_rect = pause.get_rect(center = (LARGURA/2, ALTURA/2))
            points_rect = points.get_rect(center = (LARGURA/2, ALTURA/2-50))
            last_score_rect = last_score.get_rect(center=(LARGURA / 2, ALTURA / 2 - 100))
            
            screen.blit(pause, pause_rect)
            screen.blit(points,points_rect)
            screen.blit(last_score, last_score_rect)

                
        pygame.display.flip()
        clock.tick(60)
        
if __name__ == "__main__":
    menu()
    mini_game()