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

'''
#Imagem
fundo_arquivo = pygame.image.load(path.join(img_dir,'grama.png')).convert()
fundo = pygame.transform.scale(fundo_arquivo, (tamanho))
fundo_rect = fundo.get_rect()
'''

obstaculos = []

class Fundo(pygame.sprite.Sprite):
    def __init__(self,velocidade_fundo):
        pygame.sprite.Sprite.__init__(self)
        self.velocidade_fundo = velocidade_fundo

    def imagem_fundo(self):
        self.fundo_arquivo = pygame.image.load(path.join(img_dir,'grama.png')).convert()
        self.fundo = pygame.transform.scale(self.fundo_arquivo, (tamanho))
        self.fundo_rect = self.fundo.get_rect()

    def movimento_fundo(self):
        self.rel_x = self.velocidade_fundo % self.fundo_rect.width
        self.tela_jogoblit = tela_jogo.blit(self.fundo,(self.rel_x-self.fundo_rect.width ,0))
        if self.rel_x < 800:
            self.tela_jogoblit = tela_jogo.blit(self.fundo,(self.rel_x,0))
        self.velocidade_fundo -= 5

    def go_fundo(self):
        self.imagem_fundo()
        self.movimento_fundo()


#Personagem
class Personagem(pygame.sprite.Sprite):
    def __init__ (self, velocidade_personagem, tempo_pulo, PULANDO, negativo):
        pygame.sprite.Sprite.__init__(self)
        self.velocidade_personagem = velocidade_personagem
        self.tempo_pulo = tempo_pulo
        self.PULANDO = PULANDO
        self.negativo = negativo
        self.hitbox_personagem = (10,4,65,85)

    def localizacao (self,posX_personagem,posY_personagem):
        self.posX_personagem = posX_personagem
        self.posY_personagem = posY_personagem

    def imagens(self):
        self.personagem = pygame.image.load(path.join(img_dir,'mariogro.png')).convert_alpha()
        self.personagem_oficial = pygame.transform.scale(self.personagem,(90,90))
        self.personagem_rect = self.personagem_oficial.get_rect()
        pygame.draw.rect(self.personagem_oficial, (255,0,0), self.hitbox_personagem, 2)
        tela_jogo.blit(self.personagem_oficial,(round(self.posX_personagem),round(self.posY_personagem)))

    def botoes(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.posX_personagem > self.velocidade_personagem:
            self.posX_personagem -= self.velocidade_personagem
        if keys[pygame.K_RIGHT] and self.posX_personagem < 601:
            self.posX_personagem += self.velocidade_personagem

        if not self.PULANDO:
            if keys[pygame.K_SPACE]:
                self.PULANDO = True

        else: 
            #Pulo chegando ao ápice 
            if self.tempo_pulo >= -10:
                self.negativo = 1
            #Se o tempo for negativo, agora o boneco desce
                if self.tempo_pulo < 0:
                    self.negativo = -1
            #Repare que enquanto tempo for positivo, o boneco sobe. Assim que ficar negativo, a posição desce!
                self.posY_personagem -= self.tempo_pulo**2 /2 * self.negativo
                self.tempo_pulo -= 1
        #Quando acabar o pulo, volta ao tempo inicial!
            else:
                self.PULANDO = False
                self.tempo_pulo = 10
        self.posX_personagem -= 5

    def go(self):
        self.imagens()
        self.botoes()

class Arvore():
    def __init__(self,velocidade_arvore):
        self.velocidade_arvore = velocidade_arvore

    def localizacao_arvore(self,posX_arvore,posY_arvore):
        self.posX_arvore = posX_arvore
        self.posY_arvore = posY_arvore

    def imagem_arvore(self):
        self.arvore = pygame.image.load(path.join(img_dir,'Arvore desenho.png')).convert_alpha()
        self.arvore_oficial = pygame.transform.scale(self.arvore,(120,120))
        self.arvore_rect = self.arvore_oficial.get_rect()
        self.hitbox = (7,4,100,110)
        pygame.draw.rect(self.arvore_oficial, (0,255,0), self.hitbox, 2)
        tela_jogo.blit(self.arvore_oficial, (round(self.posX_arvore),round(self.posY_arvore)))
        self.posX_arvore -= self.velocidade_arvore
        if self.posX_arvore < 0:
            self.posX_arvore = randint(800,850)
            self.velocidade_arvore = randint(5,15)

    def colisao(self,rect):
        if rect[0] + rect[2] > self.hitbox[0] and rect[0] < self.hitbox[0] + self.hitbox[2]:
            if rect[1] + rect[3] > self.hitbox[3]:
                return True
        return False


    def go_obstaculo(self):
        self.imagem_arvore()

class Rocha(Arvore):
    def __init__(self,velocidade_rocha):
        self.velocidade_rocha = velocidade_rocha
    
    def imagem_arvore(self):
        self.rocha = pygame.image.load(path.join(img_dir,'Rocha desenho.png')).convert_alpha()
        self.rocha_oficial = pygame.transform.scale(self.rocha,(120,120))
        self.rocha_rect = self.rocha_oficial.get_rect()
        self.hitboxrocha = (20,4,80,110)
        pygame.draw.rect(self.rocha_oficial, (0,255,0), self.hitboxrocha, 2)
        self.blit = tela_jogo.blit(self.rocha_oficial, (self.posX_arvore,self.posY_arvore))
        self.posX_arvore -= self.velocidade_rocha

        if self.posX_arvore < 0:
            self.posX_arvore = randint(850,900)
            self.velocidade_rocha = randint(5,15)
    
    def colisao_rocha(self,rect):
        if rect[0] + rect[2] > self.hitboxrocha[0] and rect[0] < self.hitboxrocha[0] + self.hitboxrocha[2]:
            if rect[1] + rect[3] > self.hitboxrocha[3]:
                return True
        return False




personagem = Personagem(10,10,False,1) #Altera Velocidade
personagem.localizacao(200,397) #Altera localização

fundo = Fundo(0) # Altera Velocidade do Fundo

arvore = Arvore(5) # Altera velocidade da árvore
arvore.localizacao_arvore(600,375) # Altera posição da árvore

rocha = Rocha(5) # Altera velocidade da rocha 
rocha.localizacao_arvore(850,375) # Altera posição da rocha 

'''
tamanho_personagem = (90,90)
personagem_arquivo = pygame.image.load(path.join(img_dir,'mariogro.png')).convert_alpha()
personagem = pygame.transform.scale(personagem_arquivo,(tamanho_personagem))
personagem_mascara = pygame.mask.from_surface(personagem)
personagem_rect = personagem.get_rect()

posX_personagem = 200
posY_personagem = 397
tempo_pulo = 10
velocidade_personagem = 5
vidas = 3

#Obstáculos
tamanho_arvore = (100,100)
arvore_arquivo = pygame.image.load(path.join(img_dir,'Arvore desenho.png')).convert_alpha()
arvore = pygame.transform.scale(arvore_arquivo,(tamanho_arvore))
arvore_mascara = pygame.mask.from_surface(arvore)
arvore_rect = arvore.get_rect()
posX_arvore = randint(100,600)
posY_arvore = 397


#Sistema de Pontos e Vidas
'''

JOGANDO = True 

'''
velocidade_fundo = 0
velocidade_arvore = 0
'''
while JOGANDO:

    # Ajusta a velocidade do jogo.
    clock.tick(FPS)
    '''
    rel_x = velocidade_fundo % fundo.get_rect().width
    tela_jogo.blit(fundo,(rel_x-fundo.get_rect().width ,0))
    tela_jogo.blit(personagem,(posX_personagem,posY_personagem))
    
    a = 200
    '''
    fundo.go_fundo()
    personagem.go()
    arvore.go_obstaculo()
    rocha.go_obstaculo()
    

    if arvore.colisao(personagem.hitbox_personagem) or rocha.colisao_rocha(personagem.hitbox_personagem):
        print ("oi")
    
    '''
    if rel_x < 800:
        
        tela_jogo.blit(fundo, (rel_x,0))
        tela_jogo.blit(personagem,(posX_personagem,posY_personagem))
        tela_jogo.blit(arvore, (rel_x+a,395))
        '''
    '''
    velocidade_fundo -= 2
    velocidade_arvore -= 2
    posX_personagem -= 2
    '''        
    # Processa os eventos (mouse, teclado, botão, etc).
    for event in pygame.event.get():

        # Verifica se foi fechado.
        if event.type == pygame.QUIT:
            JOGANDO = False


    '''
    keys = pygame.key.get_pressed()

    #Controlando velocidades horizontais 
    if keys[pygame.K_LEFT] and posX_personagem > velocidade_personagem:
        posX_personagem -= velocidade_personagem
    if keys[pygame.K_RIGHT] and posX_personagem < 601:
        posX_personagem += velocidade_personagem

    #Controlando velocidades verticais: 
    #Se não estiver pulando, faz nada!
    if not PULANDO:
        if keys[pygame.K_SPACE]:
            PULANDO = True
    #Pulando
    else: 
        #Pulo chegando ao ápice 
        if tempo_pulo >= -10:
            negativo = 1
            #Se o tempo for negativo, agora o boneco desce
            if tempo_pulo < 0:
                negativo = -1
            #Repare que enquanto tempo for positivo, o boneco sobe. Assim que ficar negativo, a posição desce!
            posY_personagem -= tempo_pulo**2 /2 * negativo
            tempo_pulo-= 1
        #Quando acabar o pulo, volta ao tempo inicial!
        else:
            PULANDO = False
            tempo_pulo = 10

    #Verifica se o personagem bateu na parte de trás da tela
    
    if posX_personagem == 0:
        posX_personagem = 400
        vidas -= 1
        time.sleep(1)
        if vidas <= 0:
            continue
    '''

    #Tela Games
    pygame.display.flip()
    pygame.display.update()
