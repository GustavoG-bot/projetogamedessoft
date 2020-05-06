#Importar Bibliotecas necessárias para o jogo
import pygame
from random import randint
#Inicializando o pygame
pygame.init()
#Gerando Tela do Jogo
tela_jogo = pygame.display.set_mode((800,800))
pygame.display.set_caption('Nome do Jogo!')
rodando = True 
while rodando:
    # Ajusta a velocidade do jogo.
  
    # Processa os eventos (mouse, teclado, botão, etc).
    for event in pygame.event.get():
        
        # Verifica se foi fechado.
        if event.type == pygame.QUIT:
            rodando = False