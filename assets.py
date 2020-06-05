"""Arquivos, parâmetros, assets e sprites do jogo"""

#Importando bibliotecas necessárias
import pygame
from os import path
from pygame import mixer
from classes import *

#Pasta que contêm os arquivos:
img_dir = path.join(path.dirname(__file__), 'img')
som_dir = path.join(path.dirname(__file__), 'sons')
font_dir = path.join(path.dirname(__file__), 'font')

#Gerando Tela do Jogo Principal 
LARGURA = 800
COMPRIMENTO = 600
tela_jogo = pygame.display.set_mode((LARGURA,COMPRIMENTO))
pygame.display.set_caption('Super Marioigi Run!')
FPS = 65
pontos = 0

#Váriavel para velocidade
clock = pygame.time.Clock()

#Inicializando som
pygame.mixer.init()

#Parâmetros 
rosado_largura = 90
rosado_comprimento = 90
azulado_largura = 105
azulado_comprimento = 105
personagem_largura = 90
personagem_comprimento = 90
bala_largura = 50
bala_comprimento = 50

# Iniciar assets:
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
assets['gameover_sound'] = mixer.Sound(path.join(som_dir, "gameover.oga"))
mixer.Sound.set_volume(assets['gameover_sound'] ,0.3)

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

