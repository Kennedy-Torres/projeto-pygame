import pygame
import random
import sys
from assets.configs.config import LARGURA, ALTURA, BG, BG_TELA_INICIAL, FONTE, FONTE_MENU, TIMER, SOUND_MENU, FINALIZAR, GAME_PAUSED 
from alvo import Alvo
from mira import Mira
from pontuacao import Pontuacao

pygame.init()

screen = pygame.display.set_mode((LARGURA, ALTURA)) # definição da tela

bg = pygame.image.load(BG).convert() #convert ajuda na adqueção da imagem
bg = pygame.transform.scale(bg, (LARGURA, ALTURA))

bg_tela_inicial = pygame.image.load(BG_TELA_INICIAL).convert()
bg_tela_inicial = pygame.transform.scale(bg_tela_inicial, (LARGURA, ALTURA))

clock = pygame.time.Clock() # Clock irá auxiliar com a atualização de imagens 

font = pygame.font.Font(FONTE, 30)
font_menu = pygame.font.Font(FONTE_MENU, 60)

pygame.display.set_caption('Tiro ao alvo')

# Definir o cursor padrão e o cursor interagindo com objeto
cursor_default = pygame.cursors.arrow
cursor_hand = pygame.cursors.broken_x

def menu():
    sound_menu = pygame.mixer.Sound(SOUND_MENU)
    sound_menu.play()
    
    pygame.mouse.set_cursor(*cursor_default)
    
    while True:
        screen.fill((0, 0, 0))
        screen.blit(bg_tela_inicial, (0, 0))
        
        title = font_menu.render('Tiro ao Alvo', True, (0, 0, 0))
        start_button = font_menu.render('Start', True, (0, 0, 0))
        
        title_rect = title.get_rect(center=(LARGURA / 2, ALTURA / 2 - 100))
        start_button_rect = start_button.get_rect(center=(LARGURA / 2, ALTURA / 2))
        
        screen.blit(title, title_rect)
        screen.blit(start_button, start_button_rect)
        
        mouse_pos = pygame.mouse.get_pos()
        if start_button_rect.collidepoint(mouse_pos):
            pygame.mouse.set_cursor(*cursor_hand)
        else:
            pygame.mouse.set_cursor(*cursor_default)
        
        
        for event in pygame.event.get(): # pega a leitura dos eventos
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if start_button_rect.collidepoint(event.pos):
                        sound_menu.stop()
                        return  # Sai do menu e inicia o jogo

        pygame.display.flip() # flip ... atualiza a img
        clock.tick(60) # nº de quadros passados por seg


def mini_game(pontuacao):
    global TIMER, GAME_PAUSED, FINALIZAR
    pygame.mouse.set_cursor(*cursor_default)
    
    grupo_de_alvos = pygame.sprite.Group()
    
    # Inicia o jogo com exatamente 6 alvos
    for i in range(6):
        alvo = Alvo(random.randrange(0, LARGURA), random.randrange(0, ALTURA)) # gera um grupo de 6 alvos
        grupo_de_alvos.add(alvo)


    # Transforma o cursor em uma mira
    mira = Mira(pontuacao)
    mira_group = pygame.sprite.Group()
    mira_group.add(mira)

    
    while not FINALIZAR:
        
        # USADO NA TELA DE PAUSE
        pause = font.render("PRESSIONE ESC PARA SAIR DO PAUSE", True, (255, 255, 255)) # render... trabalhando com o texto
        points = font.render(f"RECORDE: {pontuacao.recorde}", True, (255, 255, 255))
        last_score = font.render(f"PONTOS NA PARTIDA: {pontuacao.pontos}", True, (255, 255, 255))
        voltar_ao_menu = font.render("VOLTAR AO MENU", True, (255, 255, 255))
        
        pause_rect = pause.get_rect(center=(LARGURA / 2, ALTURA / 2)) #get_rect... trabalhando com o espaço ocupado pelo texto
        points_rect = points.get_rect(center=(LARGURA / 2, ALTURA / 2 - 50))
        last_score_rect = last_score.get_rect(center=(LARGURA / 2, ALTURA / 2 - 100))
        voltar_ao_menu_rect = voltar_ao_menu.get_rect(center=(LARGURA / 2, ALTURA / 2 + 120))
    
        
        if not GAME_PAUSED:
            pygame.mouse.set_visible(False)
            
            #looping para detecção de eventos
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE: # esc
                        GAME_PAUSED = not GAME_PAUSED
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        
                        # Se acertar o alvo incrementa tempo extra no tempo total, se errar decrementa
                        hit_target = mira.shoot(grupo_de_alvos)
                        if hit_target:
                            TIMER += 30 # 30/60 = 0,5seg Adicionados ao relógio
                        else:
                            TIMER -= 120 # 120/60 = 2seg retirados do relógio
            
            screen.blit(bg, (0, 0))
            grupo_de_alvos.draw(screen) # desenha na tela o conjunto de alvos
            mira_group.draw(screen) # desenha na tela a mira 
            mira_group.update() # atualiza a posição da mira
            
            score = font.render(f' Pontos: {int(pontuacao.pontos)} ', True, (0, 0, 0))
            screen.blit(score, (50, 50))
            
            tempo = font.render(f'Tempo: {TIMER / 60:.1f} s', True, (0, 0, 0))
            screen.blit(tempo, (50, 100))
        
            
            
            TIMER -= 1
            
            if TIMER < 0:
                GAME_PAUSED = True
                TIMER = 600
                pontuacao.atualizar_recorde()
                
                
        # TELA DE PAUSE
        else:
            screen.fill((252, 132, 3)) # preenche a tela em laranja
            pygame.mouse.set_visible(True)
            
            # Verificar a posição do mouse
            mouse_pos = pygame.mouse.get_pos()
            if voltar_ao_menu_rect.collidepoint(mouse_pos):
                pygame.mouse.set_cursor(*cursor_hand)
            else:
                pygame.mouse.set_cursor(*cursor_default)
                            
                            
            #looping para detecção de eventos                
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE: # tecla esc
                        GAME_PAUSED = False # retira o pause
                        
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        
                        
                        if voltar_ao_menu_rect.collidepoint(event.pos):
                            pontuacao.resetar_pontos()
                            TIMER = 600
                            GAME_PAUSED = False
                            return  # Sai do jogo e volta ao menu
                        
                        
                        

                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
        
            
            screen.blit(pause, pause_rect)
            screen.blit(points, points_rect)
            screen.blit(last_score, last_score_rect)
            screen.blit(voltar_ao_menu, voltar_ao_menu_rect)
        
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    pontuacao = Pontuacao()
    while True:
        menu()
        mini_game(pontuacao)
