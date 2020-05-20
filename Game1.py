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
FPS = 65

class Fundo_intro(pygame.sprite.Sprite):
    def __init__(self,texto1,texto2,texto3,texto4, cor_da_letra, tamanho_do_titulo,tamanho_da_instrucao, cor_fundo):
        tamanho_certo = (800,800)
        tela_jogo2 = pygame.display.set_mode(tamanho)
        tela_jogo2.fill(cor_fundo)
        self.fonte_texto1 = pygame.font.SysFont(None, tamanho_do_titulo)
        self.superficie1 = self.fonte_texto1.render(texto1, True, cor_da_letra)
        tela_jogo.blit(self.superficie1, (240, 100))
        self.fonte_texto2 = pygame.font.SysFont(None, tamanho_do_titulo)
        self.superficie2 = self.fonte_texto2.render(texto2, True, cor_da_letra)
        tela_jogo.blit(self.superficie2, (380, 160))
        self.fonte_texto3 = pygame.font.SysFont(None, tamanho_do_titulo)
        self.superficie3 = self.fonte_texto3.render(texto3, True, cor_da_letra)
        tela_jogo.blit(self.superficie3, (170, 220))
        self.fonte_texto4 = pygame.font.SysFont(None, tamanho_da_instrucao)
        self.superficie4 = self.fonte_texto4.render(texto4, True, cor_da_letra)
        tela_jogo.blit(self.superficie4, (250, 500))
        pygame.display.update()

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


        self.speedx = velocidade_personagem
    
    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.x > self.speedx:
            self.rect.x -= self.speedx
        if keys[pygame.K_RIGHT] and self.rect.x < 601:
            self.rect.x += self.speedx

        if not self.PULANDO:
            if keys[pygame.K_UP]:
                self.PULANDO = True
        
        else: 
            if self.tempo_pulo >= -10:
                self.negativo = 1
                if self.tempo_pulo < 0:
                    self.negativo = -1
                self.rect.y -= int(self.tempo_pulo**2 * 0.65 * self.negativo) 
                self.rect.x +=4
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
        self.image = pygame.image.load(path.join(img_dir,'skeleton-idle_00.png')).convert_alpha()
        self.image = pygame.transform.scale(self.image,(90,90))
        self.rect = self.image.get_rect()

        self.rect.x = posX_arvore
        self.rect.y = posY_arvore

    
    def update(self):
        
        self.rect.x -= self.speedx

        if self.rect.x < 0:
            self.rect.x = randint(800,850)
            self.speedx = randint(5,8)
    
        tela_jogo.blit(self.image, (self.rect.x,self.rect.y))

    def go_obstaculo(self):
        self.update()

class Rocha(Arvore):
    def __init__(self,velocidade_rocha,posX_rocha,posY_rocha):

        self.speedx = velocidade_rocha
        self.image = pygame.image.load(path.join(img_dir,'skeleton-fly_00.png')).convert_alpha()
        self.image = pygame.transform.scale(self.image,(105,105))
        self.rect = self.image.get_rect()
        self.rect.x = posX_rocha
        self.rect.y = posY_rocha

    
    def update(self):
        self.rect.x -= self.speedx
        if self.rect.x < 0:
            self.rect.x = randint(870,900)
            self.speedx = randint(5,6)
        tela_jogo.blit(self.image, (self.rect.x,self.rect.y))


class Bullet(pygame.sprite.Sprite):
    def __init__(self,velocidade_bala):
        pygame.sprite.Sprite.__init__(self)

        self.speedx = velocidade_bala
        self.image = pygame.image.load(path.join(img_dir,'bola_de_fogo.png')).convert_alpha()
        self.image = pygame.transform.scale(self.image,(70,70 ))

        self.rect = self.image.get_rect()
        self.rect.x = personagem.rect.centerx
        self.rect.y = personagem.rect.y

    def update(self): 
        global fire_state
        fire_state = 'FIRE'
        tela_jogo.blit(self.image, (self.rect.x,self.rect.y))


fire_state = 'ready'

personagem = Personagem(5,10,False,1,200,397) #Altera Velocidade

bullet = Bullet(-6)

intro = Fundo_intro("Bem Vindo","ao","Supermariogro","pressione ENTER para continuar", (255,255,255), 100,30, (34,139,34))

fundo = Fundo(0) # Altera Velocidade do Fundo

arvore = Arvore(5,600,400) # Altera velocidade da árvore

rocha = Rocha(5,850,260) # Altera velocidade da rocha 

Intro = True

while Intro:
    keys = pygame.key.get_pressed()
    intro.__init__
    for event in pygame.event.get():
        if keys[pygame.K_RETURN]:
            Intro = False
        elif event.type == pygame.QUIT:
            pygame.quit()

JOGANDO = True 

while JOGANDO:
    keys = pygame.key.get_pressed()
    # Ajusta a velocidade do jogo.
    clock.tick(FPS)

    # Chamando as funções para rodar.
    fundo.go_fundo()
    personagem.go()
    arvore.go_obstaculo()
    rocha.go_obstaculo()
    
    if bullet.rect.x > 1368:
        bullet.rect.x = personagem.rect.centerx
        if personagem.PULANDO == False:
            bullet.rect.y = personagem.rect.y
        elif personagem.PULANDO == True:
            bullet.rect.y = rocha.rect.y
        fire_state = 'ready'

    if fire_state == 'FIRE':
        bullet.update()
        bullet.rect.x -= bullet.speedx

    hits = pygame.sprite.collide_rect(personagem, arvore)
    hits2 = pygame.sprite.collide_rect(personagem, rocha)

    hits_do_bem = pygame.sprite.collide_rect(arvore,bullet)
    hits_do_bem2 = pygame.sprite.collide_rect(rocha,bullet)

    #if hits or hits2:
    
    if hits_do_bem:
        arvore.rect.x = randint(800,850)
        arvore.speedx = randint(6,8)
    elif hits_do_bem2:
        rocha.rect.x = randint(850,900)
        rocha.speedx = randint(6,8)

    # Processa os eventos (mouse, teclado, botão, etc).
    for event in pygame.event.get():

        if keys[pygame.K_SPACE]:
            bullet.update()
        # Verifica se foi fechado.
        if event.type == pygame.QUIT:
            JOGANDO = False

    #Tela Games
    pygame.display.flip()
    pygame.display.update()
