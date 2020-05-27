"""
Programa projeto final de Design de Software - Engenharia Insper - 1 semestre
Autores:
Filippo Ferraro
Gustavo Guedes
Tiago Seixas
"""

#Importando Bibliotecas necessárias para o jogo
import pygame
from random import randint
from os import path
from math import *
import time 
import sys
from pygame import mixer


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

def tela_final(texto1,texto2, cor_da_letra, tamanho_do_titulo, cor_fundo):
    tela_fim = pygame.display.set_mode(tamanho)
    tela_fim.fill(cor_fundo)
    fonte_fim = pygame.font.SysFont(None, tamanho_do_titulo)
    superficie1 = fonte_fim.render(texto1, True, cor_da_letra)
    tela_fim.blit(superficie1, (250, 100))
    fonte_fim2 = pygame.font.SysFont(None, tamanho_do_titulo)
    superficie2 = fonte_fim2.render(texto2, True, cor_da_letra)
    tela_fim.blit(superficie2, (150, 300))



#Criando as classes do jogo
class Fundo_intro(pygame.sprite.Sprite):
    def __init__(self,texto1,texto2,texto3,texto4,texto5,texto6,texto7,texto8, cor_da_letra, tamanho_do_titulo,tamanho_da_instrucao, cor_fundo):
        tela_jogo2 = pygame.display.set_mode(tamanho)
        tela_jogo2.fill(cor_fundo)
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
        tela_jogo2.blit(self.superficie6, ((tela_jogo2.get_width()-self.superficie6.get_width())/2, 420))
        self.fonte_texto7 = pygame.font.SysFont(None, tamanho_da_instrucao)
        self.superficie7 = self.fonte_texto7.render(texto7, True, cor_da_letra)
        tela_jogo2.blit(self.superficie7, ((tela_jogo2.get_width()-self.superficie7.get_width())/2, 480))
        self.fonte_texto8 = pygame.font.SysFont(None, tamanho_da_instrucao)
        self.superficie8 = self.fonte_texto8.render(texto8, True, cor_da_letra)
        tela_jogo2.blit(self.superficie8, ((tela_jogo2.get_width()-self.superficie8.get_width())/2, 540))
        pygame.display.update()


class Fundo(pygame.sprite.Sprite):
    def __init__(self,velocidade_fundo,pontos_iniciais):
        pygame.sprite.Sprite.__init__(self)
        try: #tenta ler os arquivos
            self.image = pygame.image.load(path.join(img_dir,'grama.png'))
        except pygame.error: #Se der errado
            print("Erro ao tentar ler a imagem do fundo") #Avisa se der errado
            sys.exit() #Sai pela rotina do sistema
        self.image = pygame.transform.scale(self.image, (tamanho)).convert()
        self.rect = self.image.get_rect()
        self.speedx = velocidade_fundo
        self.pontos = pontos_iniciais

    def update(self):
        self.speedx -= 3
        self.pontos += 3
        self.rel_x = self.speedx % self.rect.width
        self.tela_jogoblit = tela_jogo.blit(self.image,(self.rel_x-self.rect.width ,0))
        if self.rel_x < 800:
            self.tela_jogoblit = tela_jogo.blit(self.image,(self.rel_x,0))

    def go_fundo(self):
        self.update()


class Personagem(pygame.sprite.Sprite):
    def __init__ (self, velocidade_personagem, tempo_pulo, PULANDO, negativo, posX_personagem, posY_personagem):
        pygame.sprite.Sprite.__init__(self)
        try: #tenta ler os arquivos
            self.image = pygame.image.load(path.join(img_dir,'mariogro.png'))
        except pygame.error: #Se der errado
            print("Erro ao tentar ler a imagem do personagem") #Avisa se der errado
            sys.exit() #Sai pela rotina do sistema
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

class Rosado(pygame.sprite.Sprite):
    def __init__(self,velocidade_rosado,posX_rosado,posY_rosado):
        pygame.sprite.Sprite.__init__(self)

        self.speedx = velocidade_rosado
        try: #tenta ler os arquivos
            self.image = pygame.image.load(path.join(img_dir,'skeleton-idle_00.png')).convert_alpha()
        except pygame.error: #Se der errado
            print("Erro ao tentar ler a imagem do rosado") #Avisa se der errado
            sys.exit() #Sai pela rotina do sistema
        self.image = pygame.transform.scale(self.image,(90,90))
        self.rect = self.image.get_rect()

        self.rect.x = posX_rosado
        self.rect.y = posY_rosado

    
    def update(self):
        
        self.rect.x -= self.speedx

        if self.rect.x < 0:
            self.rect.x += 1200
            self.speedx = randint(5,8)
    
        tela_jogo.blit(self.image, (self.rect.x,self.rect.y))

    def go_obstaculo(self):
        self.update()

class Azulado(Rosado):
    def __init__(self,velocidade_azulado,posX_azulado,posY_azulado):

        self.speedx = velocidade_azulado
        try: #tenta ler os arquivos
            self.image = pygame.image.load(path.join(img_dir,'skeleton-fly_00.png')).convert_alpha()
        except pygame.error: #Se der errado
            print("Erro ao tentar ler a imagem do azulado") #Avisa se der errado
            sys.exit() #Sai pela rotina do sistema
        self.image = pygame.transform.scale(self.image,(105,105))
        self.rect = self.image.get_rect()
        self.rect.x = posX_azulado
        self.rect.y = posY_azulado

    
    def update(self):
        self.rect.x -= self.speedx
        if self.rect.x < 0:
            self.rect.x += 1700
            self.speedx = randint(5,6)
        tela_jogo.blit(self.image, (self.rect.x,self.rect.y))


class Bullet(pygame.sprite.Sprite):
    def __init__(self,velocidade_bala):
        pygame.sprite.Sprite.__init__(self)

        self.speedx = velocidade_bala
        try: #tenta ler os arquivos
            self.image = pygame.image.load(path.join(img_dir,'bola_de_fogo.png')).convert_alpha()
        except pygame.error: #Se der errado
            print("Erro ao tentar ler a imagem da bola de fogo") #Avisa se der errado
            sys.exit() #Sai pela rotina do sistema
        self.image = pygame.transform.scale(self.image,(70,70 ))

        self.rect = self.image.get_rect()
        self.rect.x = mariogro.rect.centerx
        self.rect.y = mariogro.rect.y

    def update(self): 
        global fire_state
        fire_state = 'FIRE'
        tela_jogo.blit(self.image, (self.rect.x,self.rect.y))
        
fire_state = 'ready'

mariogro = Personagem(5,10,False,1,200,397) #Altera Velocidade

bullet = Bullet(-30)

intro = Fundo_intro("Bem Vindo","ao","Supermariogro","Pressione SPACE para atirar","Pressione CIMA para pular","Pressione DIREITA ou ESQUERDA para mover o ogro","Caso encoste em um obstáculo, o jogo para","Pressione ENTER para continuar", (255,255,255), 80,30, (34,139,34))

fundo = Fundo(0,0) # Altera Velocidade do Fundo

rosado = Rosado(5,600,400) # Altera velocidade do monstro rosado 

azulado = Azulado(5,850,260) # Altera velocidade do monstro azulado


#Implementando Música de fundo
musica=path.join("sons", "MusicaFundo.oga")
mixer.music.set_volume(0.2)
mixer.music.load(musica)
mixer.music.play(-1)

#Implementando som do tiro
#bullet_sound=path.join("sons", "bullet.oga")
#mixer.music.load(bullet_sound)


#Loop da tela inicial
loop = True

while loop:
    Intro = True
    while Intro:
        intro.__init__
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if keys[pygame.K_RETURN]:
                Intro = False
            elif event.type == pygame.QUIT:
                pygame.quit()

    #Loop principal do jogo
    JOGANDO = True
    while JOGANDO:
        keys = pygame.key.get_pressed()
        # Ajusta a velocidade do jogo.
        clock.tick(FPS)

        # Chamando as funções para rodar.
        fundo.go_fundo()
        mariogro.go()
        rosado.go_obstaculo()
        azulado.go_obstaculo()

        
        if bullet.rect.x > 4000:
            bullet.rect.x = mariogro.rect.centerx
            if mariogro.PULANDO == False:
                bullet.rect.y = mariogro.rect.y
            elif mariogro.PULANDO == True:
                bullet.rect.y = azulado.rect.y
            fire_state = 'ready'

        if fire_state == 'FIRE':
            #bullet_sound.play()
            bullet.update()
            bullet.rect.x -= bullet.speedx
        
        hits = pygame.sprite.collide_rect(mariogro, rosado)
        hits2 = pygame.sprite.collide_rect(mariogro, azulado)

        hits_do_bem = pygame.sprite.collide_rect(rosado,bullet)
        hits_do_bem2 = pygame.sprite.collide_rect(azulado,bullet)

        if hits or hits2:
            JOGANDO = False
            mixer.music.pause()
            placar = fundo.pontos
            tela_final("Fim de jogo", "Você fez {0} pontos".format(placar),(255,255,255),80,(0,0,0))
            pygame.display.update()

            
        if hits_do_bem:
            rosado.rect.x = randint(800,850)
            rosado.speedx = randint(6,8)
        elif hits_do_bem2:
            azulado.rect.x = randint(850,900)
            azulado.speedx = randint(6,8)

        # Processa os eventos (mouse, teclado, botão, etc).
        for event in pygame.event.get():

            if keys[pygame.K_SPACE]:
                bullet.update()
            # Verifica se foi fechado.
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()
            

        #Tela Games
        pygame.display.flip()
        pygame.display.update()
