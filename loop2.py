"""Loop principal do jogo"""

#Importando bibliotecas necessárias
import pygame
from classes import *
from assets import *
from loop import *
import os

def loop_jogo():

    # Criando grupos de sprites
    all_sprites = pygame.sprite.Group()
    all_rosados = pygame.sprite.Group()
    all_azulados = pygame.sprite.Group()
    all_bullets = pygame.sprite.Group()

    groups = {}
    groups['all_sprites'] = all_sprites
    groups['all_rosados'] = all_rosados
    groups['all_azulados'] = all_azulados
    groups['all_bullets'] = all_bullets


    #Criando fundo, personagem, bala, monstros
    fundo = Fundo(assets)
    mariogro = Personagem(groups, assets)
    rosado = Rosado(assets)
    azulado = Azulado(assets)

    #Adicionando sprites nos grupos
    all_sprites.add(mariogro)
    all_sprites.add(rosado)
    all_sprites.add(azulado)

    all_rosados.add(rosado)
    all_azulados.add(azulado)
    #Variáveis iniciais
    pontos = 0
    JOGANDO = True
    PULANDO = False
    tempo_pulo = 10
    world_speed = -3
    #Placar de pontos
    font = pygame.font.SysFont("arial black", 25)
    texto = font.render("Pontos: ", True, (255,255,255), (0, 0, 0))
    pos_texto = texto.get_rect()
    pos_texto.center = (55, 15)
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
        hits = pygame.sprite.groupcollide(all_rosados, all_bullets, True, True, pygame.sprite.collide_mask)
            
        # Verifica se houve colisão entre tiro e azulado
        hits2 = pygame.sprite.groupcollide(all_azulados, all_bullets, True, True, pygame.sprite.collide_mask)

        #Contagem de pontos matando Rosado
        if hits:
            pontos += 100
            texto = font.render("Pontos: "+str(pontos), True, (255,255,255), (0, 0, 0))

        #Contagem de pontos matando Azulado
        if hits2:
            pontos += 300
            texto = font.render("Pontos: "+str(pontos), True, (255,255,255), (0, 0, 0))
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
        hits_persona = pygame.sprite.spritecollide(mariogro, all_rosados, True, pygame.sprite.collide_mask)
        hits_persona2 = pygame.sprite.spritecollide(mariogro, all_azulados, True, pygame.sprite.collide_mask)

        if len(hits_persona) > 0 or len(hits_persona2) > 0: 
            mixer.music.pause()
            tela_fim = Fundo_Fim("Fim de jogo", "Você fez {0} pontos".format(pontos), "Aperte r para tentar novamente!", (255,255,255), 80, 50, (0,0,0))      
            tela_fim.__init__
            JOGANDO = False
            assets['gameover_sound'].play()
            contador = 0
            while contador < 1e100:
                for event in pygame.event.get():
                    keys = pygame.key.get_pressed()
                    
                    if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                        pygame.quit()
                        sys.exit()

                    elif keys[pygame.K_r]:
                        """pygame.quit()
                        pygame.init()"""
                        #reiniciando o jogo (no Vscode pode não reiniciar)
                        """os.system('python Game1.py')
                        exit()"""
                        return True

                    else:
                        contador += 1
                    
        #Movimentação do fundo (cenário)

        tela_jogo.fill((0, 0, 0))
        fundo.rect.x += world_speed
        if fundo.rect.right<0:
            fundo.rect.x += fundo.rect.width
        tela_jogo.blit(fundo.image, fundo.rect)

        fundo.rect2 = fundo.rect.copy()
        fundo.rect2.x += fundo.rect2.width

        tela_jogo.blit(fundo.image, fundo.rect2)

        all_sprites.draw(tela_jogo)
        tela_jogo.blit(texto, pos_texto)
        pygame.display.flip()