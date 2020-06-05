"""Loop principal do jogo"""

#Importando bibliotecas necessárias
import pygame
from classes import *
from assets import *
from loop import *

def loop_jogo():
    #Variáveis iniciais
    pontos = 0
    JOGANDO = True
    PULANDO = False
    tempo_pulo = 10
    world_speed = -3
    while JOGANDO:
        # Ajusta a velocidade do jogo.
        clock.tick(FPS)
        keys = pygame.key.get_pressed()

        # Processa os eventos (mouse, teclado, botão, etc).
        for event in pygame.event.get():

            # Verifica se apertou alguma tecla.
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    mariogro.speedx += 8
                if event.key == pygame.K_LEFT:
                    mariogro.speedx -= 8
                if event.key == pygame.K_SPACE:
                    mariogro.shoot()   
                        
            # Verifica se soltou alguma tecla.
            if event.type == pygame.KEYUP:
                # Dependendo da tecla, altera a velocidade.
                if event.key == pygame.K_LEFT:
                    mariogro.speedx += 8
                if event.key == pygame.K_RIGHT:
                    mariogro.speedx -= 8

            # Verifica se foi fechado.
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()


        #Evento exclusivo para o Pulo do personagem!
        
        if not PULANDO:
            if keys[pygame.K_UP]:
                assets['jump_sound'].play()
                PULANDO = True
        else:
            if tempo_pulo >= -10:
                negativo = 1
                if tempo_pulo < 0:
                    negativo = -1
                mariogro.rect.y -= int(tempo_pulo**2 * 0.50 * negativo) 
                mariogro.rect.x += 4
                tempo_pulo -= 1
            else:
                PULANDO = False
                tempo_pulo = 10 

        all_sprites.update()
        
        # Verifica se houve colisão entre tiro e rosado 
        hits = pygame.sprite.groupcollide(all_rosados, all_bullets, True, True)
            
        # Verifica se houve colisão entre tiro e azulado
        hits2 = pygame.sprite.groupcollide(all_azulados, all_bullets, True, True)

        #Contagem de pontos
        if hits or hits2:
            pontos += 100

        #Recriando novos rosados e azulados
        for rosados in hits:
            assets['hit_sound'].play()
            novo_rosado = Rosado(assets)
            all_sprites.add(novo_rosado)
            all_rosados.add(novo_rosado)
        
        for azulados in hits2:
            assets['hit_sound'].play()
            novo_azulado = Azulado(assets)
            all_sprites.add(novo_azulado)
            all_azulados.add(novo_azulado)
            
        # Verifica se houve colisão entre personagem e rosados, azulados 
        hits_persona = pygame.sprite.spritecollide(mariogro, all_rosados, True)
        hits_persona2 = pygame.sprite.spritecollide(mariogro, all_azulados, True)

        if len(hits_persona) > 0 or len(hits_persona2) > 0: 
            mixer.music.pause()
            tela_fim = Fundo_Fim("Fim de jogo", "Você fez {0} pontos".format(pontos),(255,255,255),80,(0,0,0))      
            tela_fim.__init__
            JOGANDO = False
            assets['gameover_sound'].play()
            contador = 0
            while contador < 1e100:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                        pygame.quit()
                        sys.exit()
                    else:
                        contador += 1
                    
        #Movimentação do fundo

        tela_jogo.fill((0, 0, 0))
        fundo.rect.x += world_speed
        if fundo.rect.right<0:
            fundo.rect.x += fundo.rect.width
        tela_jogo.blit(fundo.image, fundo.rect)

        fundo.rect2 = fundo.rect.copy()
        fundo.rect2.x += fundo.rect2.width

        tela_jogo.blit(fundo.image, fundo.rect2)

        all_sprites.draw(tela_jogo)
        pygame.display.flip()