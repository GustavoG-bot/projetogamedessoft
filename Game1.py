"""
Programa projeto final de Design de Software - Engenharia Insper - 1 semestre
Autores:
Filippo Ferraro
Gustavo Guedes
Tiago Seixas
"""
#Importando Bibliotecas necessárias para o jogo
import pygame
from random import randint
from os import path
from math import *
import time 
import sys
from pygame import mixer
from classes import *

#Pasta que contêm os arquivos:
img_dir = path.join(path.dirname(__file__), 'img')
som_dir = path.join(path.dirname(__file__), 'sons')
font_dir = path.join(path.dirname(__file__), 'font')

#Inicializando o pygame
pygame.init()
pygame.mixer.init()

#Váriavel para velocidade
clock = pygame.time.Clock()

#Gerando Tela do Jogo Principal 
LARGURA = 800
COMPRIMENTO = 600
tela_jogo = pygame.display.set_mode((LARGURA,COMPRIMENTO))
pygame.display.set_caption('Super Marioigi Run!')
FPS = 65
pontos = 0



# Iniciar assets: 
rosado_largura = 90
rosado_comprimento = 90
azulado_largura = 105
azulado_comprimento = 105
personagem_largura = 90
personagem_comprimento = 90
bala_largura = 50
bala_comprimento = 50

assets = {}

assets['personagem_img'] = pygame.image.load(path.join(img_dir,'mariogro.png')).convert_alpha()
assets['personagem_img'] = pygame.transform.scale(assets['personagem_img'], (personagem_largura, personagem_comprimento))

assets['rosado_img'] = pygame.image.load(path.join(img_dir,'skeleton-idle_00.png')).convert_alpha()
assets['rosado_img'] = pygame.transform.scale(assets['rosado_img'], (rosado_largura, rosado_comprimento))

assets['azulado_img'] = pygame.image.load(path.join(img_dir, 'skeleton-fly_00.png')).convert_alpha()
assets['azulado_img'] = pygame.transform.scale(assets['azulado_img'], (azulado_largura, azulado_comprimento))

assets['bullet_img'] = pygame.image.load(path.join(img_dir,'bola_de_fogo.png')).convert_alpha()
assets['bullet_img'] = pygame.transform.scale(assets['bullet_img'], (bala_largura, bala_comprimento))

assets['background_img'] = pygame.image.load(path.join(img_dir,'deserto.png')).convert()
assets['background_img'] = pygame.transform.scale(assets['background_img'], (LARGURA, COMPRIMENTO))


# Carregando sons do jogo: 
mixer.music.load(path.join(som_dir, "MusicaFundo.oga"))
mixer.music.set_volume(0.3)
assets['bullet_sound'] = pygame.mixer.Sound(path.join(som_dir,"bullet.oga"))
mixer.Sound.set_volume(assets['bullet_sound'] ,0.1)
assets['hit_sound'] = mixer.Sound(path.join(som_dir, "hit.oga"))
mixer.Sound.set_volume(assets['hit_sound'] ,0.1)
assets['jump_sound'] = mixer.Sound(path.join(som_dir, "jump.oga"))
mixer.Sound.set_volume(assets['jump_sound'] ,0.1)


# Criando grupos 
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

#Adicionando no all_sprites e all_rosados e all_azulados
all_sprites.add(mariogro)
all_sprites.add(rosado)
all_sprites.add(azulado)

all_rosados.add(rosado)
all_azulados.add(azulado)


#Palavras introdutórias do tutorial e algumas variáveis para a movimentação do personagem
intro = Fundo_intro("Bem Vindo","ao","Supermariogro","Pressione SPACE para atirar","Pressione CIMA para pular","Pressione DIREITA ou ESQUERDA para mover o ogro","Caso encoste em um obstáculo, o jogo para","Pressione ENTER para continuar", (255,255,255), 80,30, (34,139,34))
PULANDO = False
tempo_pulo = 10
world_speed = -3



#Rodando musica de fundo
pygame.mixer.music.play(loops=-1)



Intro = True
while Intro:
    intro.__init__
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if keys[pygame.K_RETURN]:
            Intro = False
        elif event.type == pygame.QUIT:
            pygame.quit()

#Loop principal do jogo
JOGANDO = True
    
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

    # Verifica se foi fechado.
    if event.type == pygame.QUIT:
        pygame.quit()
        sys.exit()

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

