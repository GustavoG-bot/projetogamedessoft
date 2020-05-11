#Importar Bibliotecas necessárias para o jogo
import pygame
from random import randint
from os import path

#Pasta que contêm os arquivos: 
img_dir = path.join(path.dirname(_file_), 'img')
som_dir = path.join(path.dirname(_file_), 'sons')
font_dir = path.join(path.dirname(_file_), 'font')

#Inicializando o pygame
pygame.init()

#Váriavel para velocidade
clock = pygame.time.Clock()


#Gerando Tela do Jogo
tamanho = (800,600)
tela_jogo = pygame.display.set_mode(tamanho)
pygame.display.set_caption('Super Marioigi Run!')
FPS = 100

fundo_arquivo = pygame.image.load(path.join(img_dir,'grama.png')).convert()
fundo = pygame.transform.scale(fundo_arquivo, (tamanho))
fundo_rect = fundo.get_rect()


JOGANDO = True 


#class Jogadores():
posição_fundo = 0
while JOGANDO:
    # Ajusta a velocidade do jogo.
    clock.tick(FPS)

    rel_posição_fundo = posição_fundo % fundo.get_rect().width
    tela_jogo.blit(fundo,(rel_posição_fundo-fundo.get_rect().width ,0))
    if rel_posição_fundo < 800 :
        tela_jogo.blit(fundo, (rel_posição_fundo,0))
    posição_fundo -= 2
  
    # Processa os eventos (mouse, teclado, botão, etc).
    for event in pygame.event.get():

        # Verifica se foi fechado.
        if event.type == pygame.QUIT:
            JOGANDO = False
        
        #if event.type == pygame.KEYUP:


        #if event.type == pygame.W

        
            
    #Tela game
    #tela_jogo = Teladefundo()
    pygame.display.flip()
    pygame.display.update()
