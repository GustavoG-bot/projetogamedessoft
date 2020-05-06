#Importar Bibliotecas necessárias para o jogo
import pygame
from random import randint
#Inicializando o pygame
pygame.init()

#Gerando Tela do Jogo
tela_jogo = pygame.display.set_mode((800,600))
pygame.display.set_caption('jogo a definir')
rodando = True 

while rodando:
    # Ajusta a velocidade do jogo.
  
    # Processa os eventos (mouse, teclado, botão, etc).
    for event in pygame.event.get():
        
        # Verifica se foi fechado.
        if event.type == pygame.QUIT:
            rodando = False
    #Preenche com cor
    tela_jogo.fill((255,0,0))
    pygame.display.update()