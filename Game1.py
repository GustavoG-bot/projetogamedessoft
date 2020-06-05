""" Programa projeto final de Design de Software
Autores: Filippo Ferraro, Gustavo Guedes e Tiago Seixas - Engenharia Insper - 1 semestreb - Turma A """
#Importando Bibliotecas necessárias para o jogo
import pygame
from assets import *
from loop import *
from loop2 import *

#Pasta que contêm os arquivos:
img_dir = path.join(path.dirname(__file__), 'img')
som_dir = path.join(path.dirname(__file__), 'sons')

#Inicializando o pygame
pygame.init()
pygame.mixer.init()

#Rodando musica de fundo
pygame.mixer.music.play(loops=-1)

#Rodando o loop de entrada
loop_intro()

#Rodando o loop principal do jogo
loop_jogo()