"""Classes do jogo"""

#Importando bibliotecas necessárias
import pygame
from random import randint
from os import path
from math import *
import time 
import sys
from pygame import mixer

#Gerando Tela do Jogo Principal 
LARGURA = 800
COMPRIMENTO = 600
tela_jogo = pygame.display.set_mode((LARGURA,COMPRIMENTO))
pygame.display.set_caption('Super Marioigi Run!')
FPS = 65
cor_intro=(255, 200, 70)
#Criando as classes do jogo

#Classe da tela de entrada
class Fundo_intro(pygame.sprite.Sprite):
    def __init__(self,texto1,texto2,texto3,texto4,texto5,texto6,texto7,texto8, cor_da_letra, tamanho_do_titulo,tamanho_da_instrucao, cor_fundo):
        tela_jogo2 = pygame.display.set_mode((LARGURA,COMPRIMENTO))
        tela_jogo2.fill(cor_intro)
        self.fonte_texto1 = pygame.font.SysFont(None, tamanho_do_titulo)
        self.superficie1 = self.fonte_texto1.render(texto1, True, cor_da_letra)
        tela_jogo2.blit(self.superficie1, ((tela_jogo2.get_width()-self.superficie1.get_width())/2, 60))
        self.fonte_texto2 = pygame.font.SysFont(None, tamanho_do_titulo)
        self.superficie2 = self.fonte_texto2.render(texto2, True, cor_da_letra)
        tela_jogo2.blit(self.superficie2, ((tela_jogo2.get_width()-self.superficie2.get_width())/2, 120))
        self.fonte_texto3 = pygame.font.SysFont(None, tamanho_do_titulo)
        self.superficie3 = self.fonte_texto3.render(texto3, True, cor_da_letra)
        tela_jogo2.blit(self.superficie3, ((tela_jogo2.get_width()-self.superficie3.get_width())/2, 180))
        self.fonte_texto4 = pygame.font.SysFont(None, tamanho_da_instrucao)
        self.superficie4 = self.fonte_texto4.render(texto4, True, cor_da_letra)
        tela_jogo2.blit(self.superficie4, ((tela_jogo2.get_width()-self.superficie4.get_width())/2, 300))
        self.fonte_texto5 = pygame.font.SysFont(None, tamanho_da_instrucao)
        self.superficie5 = self.fonte_texto5.render(texto5, True, cor_da_letra)
        tela_jogo2.blit(self.superficie5, ((tela_jogo2.get_width()-self.superficie5.get_width())/2, 360))
        self.fonte_texto6 = pygame.font.SysFont(None, tamanho_da_instrucao)
        self.superficie6 = self.fonte_texto6.render(texto6, True, cor_da_letra)
        tela_jogo2.blit(self.superficie6, ((tela_jogo2.get_width()-self.superficie6.get_width())/2, 480))
        self.fonte_texto7 = pygame.font.SysFont(None, tamanho_da_instrucao)
        self.superficie7 = self.fonte_texto7.render(texto7, True, cor_da_letra)
        tela_jogo2.blit(self.superficie7, ((tela_jogo2.get_width()-self.superficie7.get_width())/2, 420))
        self.fonte_texto8 = pygame.font.SysFont(None, tamanho_da_instrucao)
        self.superficie8 = self.fonte_texto8.render(texto8, True, cor_da_letra)
        tela_jogo2.blit(self.superficie8, ((tela_jogo2.get_width()-self.superficie8.get_width())/2, 540))
        pygame.display.update()

#Classe da tela de fundo do jogo
class Fundo(pygame.sprite.Sprite):
    def __init__(self, assets):
        pygame.sprite.Sprite.__init__(self)
        self.image = assets['background_img']
        self.rect = self.image.get_rect()
        self.x_mov = 0

#Classe do personagem do jogador
class Personagem(pygame.sprite.Sprite):
    def __init__ (self, groups, assets):
        pygame.sprite.Sprite.__init__(self)

        self.image = assets['personagem_img']
        self.rect = self.image.get_rect()

        self.rect.x = 200
        self.rect.y = 400

        self.speedx = -3

        self.groups = groups
        self.assets = assets
    
    def update(self):
        self.rect.x += self.speedx

        # Mantem o personagem dentro da tela
        if self.rect.right > LARGURA:
            self.rect.right = LARGURA
        if self.rect.left < 0:
            self.rect.left = 0

    def shoot(self):
        # A nova bala vai ser criada no mesmo Y do personagem e no centro VERTICAL do personagem:
        nova_bala = Bullet(self.assets, self.rect.y, self.rect.centerx)
        self.groups['all_sprites'].add(nova_bala)
        self.groups['all_bullets'].add(nova_bala)
        self.assets['bullet_sound'].play()

#Classe de um obstáculo
class Rosado(pygame.sprite.Sprite):
    def __init__(self, assets):
        pygame.sprite.Sprite.__init__(self)
        
        self.image = assets['rosado_img']
        self.rect = self.image.get_rect()

        self.rect.x = randint(LARGURA,850)
        self.rect.y = 395

        self.speedx = randint(5,9)

    def update(self):
        self.rect.x -= self.speedx
        # Se o rosado passar do final da tela, volta para a esquerda e sorteia novas posições e velocidades.
        if self.rect.right < 0:
            self.rect.x = randint(LARGURA, 850)
            self.speedx = randint(5,9)
    
#Classe de outro obstáculo
class Azulado(pygame.sprite.Sprite):
    def __init__(self, assets):
        pygame.sprite.Sprite.__init__(self)

        self.image = assets['azulado_img']
        self.rect = self.image.get_rect()

        self.rect.x = randint(LARGURA, 850)
        self.rect.y = 295

        self.speedx = randint(5, 9)

    def update(self):
        self.rect.x -= self.speedx
        # Se o rosado passar do final da tela, volta para a esquerda e sorteia novas posições e velocidades.
        if self.rect.right < 0:
            self.rect.x = randint(LARGURA,850)
            self.speedx = randint(5, 9)
            
 
#Classe da bola de fogo
class Bullet(pygame.sprite.Sprite):
    def __init__(self, assets, posY_personagem, centerx):
        pygame.sprite.Sprite.__init__(self)

        #Velocidade fixa, para a direita 
        self.speedx = -20 

        self.image = assets['bullet_img']
        self.rect = self.image.get_rect()

        self.rect.centerx = centerx
        self.rect.y = posY_personagem

    def update(self): 
        self.rect.x -= self.speedx

        # Se o tiro passar do fim da tela, morre.
        if self.rect.y > LARGURA:
            self.kill()

#Classe da tela final
class Fundo_Fim(pygame.sprite.Sprite):
            def __init__(self, texto1, texto2, cor_da_letra, tamanho_do_titulo, cor_fundo):
                tela_fim = pygame.display.set_mode((LARGURA,COMPRIMENTO))
                tela_fim.fill(cor_fundo)
                self.fonte_fim = pygame.font.SysFont(None, tamanho_do_titulo)
                self.superficie1 = self.fonte_fim.render(texto1, True, cor_da_letra)
                tela_fim.blit(self.superficie1, ((tela_fim.get_width()-self.superficie1.get_width())/2, 100))
                self.fonte_fim2 = pygame.font.SysFont(None, tamanho_do_titulo)
                self.superficie2 = self.fonte_fim2.render(texto2, True, cor_da_letra)
                tela_fim.blit(self.superficie2, ((tela_fim.get_width()-self.superficie2.get_width())/2, 300))
                pygame.display.update()



