#Importar Bibliotecas necessárias para o jogo
import pygame
from random import randint
from os import path
from math import *
import time 

#Pasta que contêm os arquivos: 
img_dir = path.join(path.dirname(__file__), 'img')
som_dir = path.join(path.dirname(__file__), 'sons')
font_dir = path.join(path.dirname(__file__), 'font')

#Inicializando o pygame
pygame.init()

#Váriavel para velocidade
clock = pygame.time.Clock()

#Gerando Tela do Jogo Principal 
tamanho = (800,600)
tela_jogo = pygame.display.set_mode(tamanho)
pygame.display.set_caption('Super Marioigi Run!')
FPS = 100


class Fundo(pygame.sprite.Sprite):
    def __init__(self,velocidade_fundo):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(path.join(img_dir,'grama.png'))
        self.image = pygame.transform.scale(self.image, (tamanho)).convert()
        self.rect = self.image.get_rect()
        self.speedx = velocidade_fundo

    def update(self):
        self.speedx -= 3
        self.rel_x = self.speedx % self.rect.width
        self.tela_jogoblit = tela_jogo.blit(self.image,(self.rel_x-self.rect.width ,0))
        if self.rel_x < 800:
            self.tela_jogoblit = tela_jogo.blit(self.image,(self.rel_x,0))

    def go_fundo(self):
        self.update()


class Personagem(pygame.sprite.Sprite):
    def __init__ (self, velocidade_personagem, tempo_pulo, PULANDO, negativo, posX_personagem, posY_personagem):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(path.join(img_dir,'mariogro.png'))
        self.image = pygame.transform.scale(self.image,(90,90)).convert_alpha()
        self.rect = self.image.get_rect()

        self.tempo_pulo = tempo_pulo
        self.PULANDO = PULANDO
        self.negativo = negativo

        self.rect.x = posX_personagem
        self.rect.y = posY_personagem

        #self.hitbox = (10,4,65,85)
        #pygame.draw.rect(self.image, (255,0,0), self.hitbox, 2)

        self.speedx = velocidade_personagem


    def update(self):
        self.rect.x -= 3
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.x > self.speedx:
            self.rect.x -= self.speedx
        if keys[pygame.K_RIGHT] and self.rect.x < 601:
            self.rect.x += self.speedx
    
        if not self.PULANDO:
            if keys[pygame.K_SPACE]:
                self.PULANDO = True
        
        else: 
            if self.tempo_pulo >= -10:
                self.negativo = 1
                if self.tempo_pulo < 0:
                    self.negativo = -1
                self.rect.y -= int(self.tempo_pulo**2 /2 * self.negativo) 
                self.tempo_pulo -= 1
            else:
                self.PULANDO = False
                self.tempo_pulo = 10
        tela_jogo.blit(self.image,(self.rect.x,self.rect.y))
        

    def go(self):
        self.update()

class Arvore(pygame.sprite.Sprite):
    def __init__(self,velocidade_arvore,posX_arvore,posY_arvore):
        pygame.sprite.Sprite.__init__(self)


        self.speedx = velocidade_arvore
        self.image = pygame.image.load(path.join(img_dir,'Arvore desenho.png')).convert_alpha()
        self.image = pygame.transform.scale(self.image,(120,120))
        self.rect = self.image.get_rect()

        self.rect.x = posX_arvore
        self.rect.y = posY_arvore

        self.hitbox = (7,4,100,110)

        #pygame.draw.rect(self.image, (0,255,0), self.hitbox, 2)

    def update(self):
        self.rect.x -= self.speedx

        if self.rect.x < 0:
            self.rect.x = randint(800,850)
            self.speedx = randint(5,8)

        tela_jogo.blit(self.image, (round(self.rect.x),round(self.rect.y)))

    #def colisao(self, rect):
        #if rect[0] + rect[2] > self.hitbox[0] and rect[0] < self.hitbox[0] + self.hitbox[2]:
            #if rect[1] + rect[3] > self.hitbox[3]:
                #return True
            #else:
                #return False

    def go_obstaculo(self):
        self.update()

class Rocha(Arvore):
    def __init__(self,velocidade_rocha,posX_rocha,posY_rocha):

        self.speedx = velocidade_rocha
        self.image = pygame.image.load(path.join(img_dir,'Rocha desenho.png')).convert_alpha()
        self.image = pygame.transform.scale(self.image,(120,120))
        self.rect = self.image.get_rect()
        self.rect.x = posX_rocha
        self.rect.y = posY_rocha

        self.hitbox = (20,4,80,110)

        #pygame.draw.rect(self.image, (0,255,0), self.hitbox, 2)
    
    def update(self):
        self.rect.x -= self.speedx
        if self.rect.x < 0:
            self.rect.x = randint(850,900)
            self.speedx = randint(5,9)
        tela_jogo.blit(self.image, (self.rect.x,self.rect.y))
    
    #def colisao_rocha(self,rect):
        #if rect[0] + rect[2] > self.hitboxrocha[0] and rect[0] < self.hitboxrocha[0] + self.hitboxrocha[2]:
            #if rect[1] + rect[3] > self.hitboxrocha[3]:
                #return True
        #return False


personagem = Personagem(5,10,False,1,200,397) #Altera Velocidade

fundo = Fundo(0) # Altera Velocidade do Fundo

arvore = Arvore(5,600,375) # Altera velocidade da árvore

rocha = Rocha(5,850,375) # Altera velocidade da rocha 



JOGANDO = True 

while JOGANDO:

    # Ajusta a velocidade do jogo.
    clock.tick(FPS)

    # Chamando as funções para rodar.
    fundo.go_fundo()
    personagem.go()
    arvore.go_obstaculo()
    rocha.go_obstaculo()
    
    hits = pygame.sprite.collide_rect(personagem, arvore)
    if hits:
        print ('colidiu')

    #if arvore.colisao(personagem.hitbox_personagem) or rocha.colisao_rocha(personagem.hitbox_personagem):
        #print ("oi")
      
    # Processa os eventos (mouse, teclado, botão, etc).
    for event in pygame.event.get():

        # Verifica se foi fechado.
        if event.type == pygame.QUIT:
            JOGANDO = False

    #Tela Games
    pygame.display.flip()
    pygame.display.update()
