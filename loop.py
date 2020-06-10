"""Loop da tela inicial do jogo"""

#Importando as classes necessárias para o jogo
import pygame
from classes import *

def loop_intro():
    Intro = True
    #Palavras introdutórias do tutorial e algumas variáveis para a movimentação do personagem
    intro = Fundo_intro("Bem Vindo","ao","Supermariogro","Pressione SPACE para atirar","Pressione CIMA para pular","Pressione DIREITA ou ESQUERDA para mover o ogro","Caso encoste em um obstáculo, o jogo para","Pressione ENTER para continuar", (255,255,255), 80,30, (34,139,34))
    while Intro:
        pygame.init()
        intro.__init__
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if keys[pygame.K_RETURN]:
                Intro = False
            elif event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()