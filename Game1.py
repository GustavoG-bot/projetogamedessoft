<<<<<<< HEAD
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
pygame.mixer.init()

#Váriavel para velocidade
clock = pygame.time.Clock()

#Gerando Tela do Jogo Principal 
LARGURA = 800
COMPRIMENTO = 600
tela_jogo = pygame.display.set_mode((LARGURA,COMPRIMENTO))
pygame.display.set_caption('Super Marioigi Run!')
FPS = 65
pontos = 0



# Iniciar assets: 
rosado_largura = 90
rosado_comprimento = 90
azulado_largura = 105
azulado_comprimento = 105
personagem_largura = 90
personagem_comprimento = 90
bala_largura = 50
bala_comprimento = 50

assets = {}

assets['personagem_img'] = pygame.image.load(path.join(img_dir,'mariogro.png')).convert_alpha()
assets['personagem_img'] = pygame.transform.scale(assets['personagem_img'], (personagem_largura, personagem_comprimento))

assets['rosado_img'] = pygame.image.load(path.join(img_dir,'skeleton-idle_00.png')).convert_alpha()
assets['rosado_img'] = pygame.transform.scale(assets['rosado_img'], (rosado_largura, rosado_comprimento))

assets['azulado_img'] = pygame.image.load(path.join(img_dir, 'skeleton-fly_00.png')).convert_alpha()
assets['azulado_img'] = pygame.transform.scale(assets['azulado_img'], (azulado_largura, azulado_comprimento))

assets['bullet_img'] = pygame.image.load(path.join(img_dir,'bola_de_fogo.png')).convert_alpha()
assets['bullet_img'] = pygame.transform.scale(assets['bullet_img'], (bala_largura, bala_comprimento))

assets['background_img'] = pygame.image.load(path.join(img_dir,'deserto.png')).convert()
assets['background_img'] = pygame.transform.scale(assets['background_img'], (LARGURA, COMPRIMENTO))


# Carregando sons do jogo: 
pygame.mixer.music.load(path.join(som_dir, "MusicaFundo.oga"))
pygame.mixer.music.set_volume(0.3)
assets['bullet_sound'] = pygame.mixer.Sound(path.join(som_dir,"bullet.oga"))
#assets['pew_sound'] = pygame.mixer.Sound('assets/snd/pew.wav')

#Criando as classes do jogo
class Fundo_intro(pygame.sprite.Sprite):
    def __init__(self,texto1,texto2,texto3,texto4,texto5,texto6,texto7,texto8, cor_da_letra, tamanho_do_titulo,tamanho_da_instrucao, cor_fundo):
        tela_jogo2 = pygame.display.set_mode((LARGURA,COMPRIMENTO))
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
        tela_jogo2.blit(self.superficie6, ((tela_jogo2.get_width()-self.superficie6.get_width())/2, 480))
        self.fonte_texto7 = pygame.font.SysFont(None, tamanho_da_instrucao)
        self.superficie7 = self.fonte_texto7.render(texto7, True, cor_da_letra)
        tela_jogo2.blit(self.superficie7, ((tela_jogo2.get_width()-self.superficie7.get_width())/2, 420))
        self.fonte_texto8 = pygame.font.SysFont(None, tamanho_da_instrucao)
        self.superficie8 = self.fonte_texto8.render(texto8, True, cor_da_letra)
        tela_jogo2.blit(self.superficie8, ((tela_jogo2.get_width()-self.superficie8.get_width())/2, 540))
        pygame.display.update()


class Fundo(pygame.sprite.Sprite):
    def __init__(self, assets):
        pygame.sprite.Sprite.__init__(self)
        self.image = assets['background_img']
        self.rect = self.image.get_rect()
        self.x_mov = 0

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

class Rosado(pygame.sprite.Sprite):
    def __init__(self, assets):
        pygame.sprite.Sprite.__init__(self)
        
        self.image = assets['rosado_img']
        self.rect = self.image.get_rect()

        self.rect.x = randint(LARGURA,850)
        self.rect.y = 395

        self.speedx = randint(4,6)

    def update(self):
        self.rect.x -= self.speedx
        # Se o rosado passar do final da tela, volta para a esquerda e sorteia novas posições e velocidades.
        if self.rect.right < 0:
            self.rect.x = randint(LARGURA, 850)
            self.speedx = randint(4,6)
    

class Azulado(pygame.sprite.Sprite):
    def __init__(self, assets):
        pygame.sprite.Sprite.__init__(self)

        self.image = assets['azulado_img']
        self.rect = self.image.get_rect()

        self.rect.x = randint(LARGURA, 850)
        self.rect.y = 295

        self.speedx = randint(4, 6)

    def update(self):
        self.rect.x -= self.speedx
        # Se o rosado passar do final da tela, volta para a esquerda e sorteia novas posições e velocidades.
        if self.rect.right < 0:
            self.rect.x = randint(LARGURA,850)
            self.speedx = randint(4, 6)
            
 

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



# Criando grupos 
all_sprites = pygame.sprite.Group()
all_rosados = pygame.sprite.Group()
all_azulados = pygame.sprite.Group()
all_bullets = pygame.sprite.Group()

groups = {}
groups['all_sprites'] = all_sprites
groups['all_rosados'] = all_rosados
groups['all_azulados'] = all_azulados
groups['all_bullets'] = all_bullets

#Criando fundo, personagem, bala, monstros
fundo = Fundo(assets)
mariogro = Personagem(groups, assets)
rosado = Rosado(assets)
azulado = Azulado(assets)

#Adicionando no all_sprites e all_rosados e all_azulados
all_sprites.add(mariogro)
all_sprites.add(rosado)
all_sprites.add(azulado)

all_rosados.add(rosado)
all_azulados.add(azulado)


#Palavras introdutórias do tutorial e algumas variáveis para a movimentação do personagem
intro = Fundo_intro("Bem Vindo","ao","Supermariogro","Pressione SPACE para atirar","Pressione CIMA para pular","Pressione DIREITA ou ESQUERDA para mover o ogro","Caso encoste em um obstáculo, o jogo para","Pressione ENTER para continuar", (255,255,255), 80,30, (34,139,34))
PULANDO = False
tempo_pulo = 10
world_speed = -3



#Rodando musica de fundo
pygame.mixer.music.play(loops=-1)



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
    # Ajusta a velocidade do jogo.
    clock.tick(FPS)
    keys = pygame.key.get_pressed()

    # Processa os eventos (mouse, teclado, botão, etc).
    for event in pygame.event.get():

        # Verifica se apertou alguma tecla.
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                mariogro.speedx += 8
            if event.key == pygame.K_LEFT:
                mariogro.speedx -= 8
            if event.key == pygame.K_SPACE:
                mariogro.shoot()   
                      
        # Verifica se soltou alguma tecla.
        if event.type == pygame.KEYUP:
            # Dependendo da tecla, altera a velocidade.
            if event.key == pygame.K_LEFT:
                mariogro.speedx += 8
            if event.key == pygame.K_RIGHT:
                mariogro.speedx -= 8

    #Evento exclusivo para o Pulo do personagem!
        
    if not PULANDO:
        if keys[pygame.K_UP]:
            PULANDO = True
    else:
        if tempo_pulo >= -10:
            negativo = 1
            if tempo_pulo < 0:
                negativo = -1
            mariogro.rect.y -= int(tempo_pulo**2 * 0.50 * negativo) 
            #mariogro.speedx += 4
            tempo_pulo -= 1
        else:
            PULANDO = False
            tempo_pulo = 10 

    # Verifica se foi fechado.
    if event.type == pygame.QUIT:
        pygame.quit()
        sys.exit()

    all_sprites.update()
    
    # Verifica se houve colisão entre tiro e rosado 
    hits = pygame.sprite.groupcollide(all_rosados, all_bullets, True, True)
        
    # Verifica se houve colisão entre tiro e azulado
    hits2 = pygame.sprite.groupcollide(all_azulados, all_bullets, True, True)

    #Contagem de pontos
    if hits or hits2:
        pontos += 100

    #Recriando novos rosados e azulados
    for rosados in hits: 
        novo_rosado = Rosado(assets)
        all_sprites.add(novo_rosado)
        all_rosados.add(novo_rosado)
    
    for azulados in hits2: 
        novo_azulado = Azulado(assets)
        all_sprites.add(novo_azulado)
        all_azulados.add(novo_azulado)
        
    # Verifica se houve colisão entre personagem e rosados, azulados 
    hits_persona = pygame.sprite.spritecollide(mariogro, all_rosados, True)
    hits_persona2 = pygame.sprite.spritecollide(mariogro, all_azulados, True)

    if len(hits_persona) > 0 or len(hits_persona2) > 0: 
        mixer.music.pause()
        #Classe para tela final
        class Fundo_Fim(pygame.sprite.Sprite):
            def __init__(self, texto1, texto2, cor_da_letra, tamanho_do_titulo, cor_fundo):
                tela_fim = pygame.display.set_mode((LARGURA,COMPRIMENTO))
                tela_fim.fill(cor_fundo)
                self.fonte_fim = pygame.font.SysFont(None, tamanho_do_titulo)
                self.superficie1 = self.fonte_fim.render(texto1, True, cor_da_letra)
                tela_fim.blit(self.superficie1, (250, 100))
                self.fonte_fim2 = pygame.font.SysFont(None, tamanho_do_titulo)
                self.superficie2 = self.fonte_fim2.render(texto2, True, cor_da_letra)
                tela_fim.blit(self.superficie2, (150, 300))
                pygame.display.update()
        tela_fim = Fundo_Fim("Fim de jogo", "Você fez {0} pontos".format(pontos),(255,255,255),80,(0,0,0))      
        tela_fim.__init__
        JOGANDO = False
        contador = 0
        while contador < 1e100:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    pygame.quit()
                    sys.exit()
                else:
                    contador += 1
                
            

  
        # assets['boom_sound'].play()

    #Movimentação do fundo

    tela_jogo.fill((0, 0, 0))
    fundo.rect.x += world_speed
    if fundo.rect.right<0:
        fundo.rect.x += fundo.rect.width
    tela_jogo.blit(fundo.image, fundo.rect)

    fundo.rect2 = fundo.rect.copy()
    fundo.rect2.x += fundo.rect2.width

    tela_jogo.blit(fundo.image, fundo.rect2)

    all_sprites.draw(tela_jogo)
    pygame.display.flip()
=======
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
pygame.mixer.init()

#Váriavel para velocidade
clock = pygame.time.Clock()

#Gerando Tela do Jogo Principal 
LARGURA = 800
COMPRIMENTO = 600
tela_jogo = pygame.display.set_mode((LARGURA,COMPRIMENTO))
pygame.display.set_caption('Super Marioigi Run!')
FPS = 65
pontos = 0



# Iniciar assets: 
rosado_largura = 90
rosado_comprimento = 90
azulado_largura = 105
azulado_comprimento = 105
personagem_largura = 90
personagem_comprimento = 90
bala_largura = 50
bala_comprimento = 50

assets = {}

assets['personagem_img'] = pygame.image.load(path.join(img_dir,'mariogro.png')).convert_alpha()
assets['personagem_img'] = pygame.transform.scale(assets['personagem_img'], (personagem_largura, personagem_comprimento))

assets['rosado_img'] = pygame.image.load(path.join(img_dir,'skeleton-idle_00.png')).convert_alpha()
assets['rosado_img'] = pygame.transform.scale(assets['rosado_img'], (rosado_largura, rosado_comprimento))

assets['azulado_img'] = pygame.image.load(path.join(img_dir, 'skeleton-fly_00.png')).convert_alpha()
assets['azulado_img'] = pygame.transform.scale(assets['azulado_img'], (azulado_largura, azulado_comprimento))

assets['bullet_img'] = pygame.image.load(path.join(img_dir,'bola_de_fogo.png')).convert_alpha()
assets['bullet_img'] = pygame.transform.scale(assets['bullet_img'], (bala_largura, bala_comprimento))

assets['background_img'] = pygame.image.load(path.join(img_dir,'deserto.png')).convert()
assets['background_img'] = pygame.transform.scale(assets['background_img'], (LARGURA, COMPRIMENTO))


# Carregando sons do jogo: 
pygame.mixer.music.load(path.join(som_dir, "MusicaFundo.oga"))
pygame.mixer.music.set_volume(0.3)
assets['bullet_sound'] = pygame.mixer.Sound(path.join(som_dir,"bullet.oga"))
#assets['pew_sound'] = pygame.mixer.Sound('assets/snd/pew.wav')

#Criando as classes do jogo
class Fundo_intro(pygame.sprite.Sprite):
    def __init__(self,texto1,texto2,texto3,texto4,texto5,texto6,texto7,texto8, cor_da_letra, tamanho_do_titulo,tamanho_da_instrucao, cor_fundo):
        tela_jogo2 = pygame.display.set_mode((LARGURA,COMPRIMENTO))
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
        tela_jogo2.blit(self.superficie6, ((tela_jogo2.get_width()-self.superficie6.get_width())/2, 480))
        self.fonte_texto7 = pygame.font.SysFont(None, tamanho_da_instrucao)
        self.superficie7 = self.fonte_texto7.render(texto7, True, cor_da_letra)
        tela_jogo2.blit(self.superficie7, ((tela_jogo2.get_width()-self.superficie7.get_width())/2, 420))
        self.fonte_texto8 = pygame.font.SysFont(None, tamanho_da_instrucao)
        self.superficie8 = self.fonte_texto8.render(texto8, True, cor_da_letra)
        tela_jogo2.blit(self.superficie8, ((tela_jogo2.get_width()-self.superficie8.get_width())/2, 540))
        pygame.display.update()


class Fundo(pygame.sprite.Sprite):
    def __init__(self, assets):
        pygame.sprite.Sprite.__init__(self)
        self.image = assets['background_img']
        self.rect = self.image.get_rect()
        self.x_mov = 0

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

class Rosado(pygame.sprite.Sprite):
    def __init__(self, assets):
        pygame.sprite.Sprite.__init__(self)
        
        self.image = assets['rosado_img']
        self.rect = self.image.get_rect()

        self.rect.x = randint(LARGURA,850)
        self.rect.y = 395

        self.speedx = randint(4,6)

    def update(self):
        self.rect.x -= self.speedx
        # Se o rosado passar do final da tela, volta para a esquerda e sorteia novas posições e velocidades.
        if self.rect.right < 0:
            self.rect.x = randint(LARGURA, 850)
            self.speedx = randint(4,6)
    

class Azulado(pygame.sprite.Sprite):
    def __init__(self, assets):
        pygame.sprite.Sprite.__init__(self)

        self.image = assets['azulado_img']
        self.rect = self.image.get_rect()

        self.rect.x = randint(LARGURA, 850)
        self.rect.y = 295

        self.speedx = randint(4, 6)

    def update(self):
        self.rect.x -= self.speedx
        # Se o rosado passar do final da tela, volta para a esquerda e sorteia novas posições e velocidades.
        if self.rect.right < 0:
            self.rect.x = randint(LARGURA,850)
            self.speedx = randint(4, 6)
            
 

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



# Criando grupos 
all_sprites = pygame.sprite.Group()
all_rosados = pygame.sprite.Group()
all_azulados = pygame.sprite.Group()
all_bullets = pygame.sprite.Group()

groups = {}
groups['all_sprites'] = all_sprites
groups['all_rosados'] = all_rosados
groups['all_azulados'] = all_azulados
groups['all_bullets'] = all_bullets

#Criando fundo, personagem, bala, monstros
fundo = Fundo(assets)
mariogro = Personagem(groups, assets)
rosado = Rosado(assets)
azulado = Azulado(assets)

#Adicionando no all_sprites e all_rosados e all_azulados
all_sprites.add(mariogro)
all_sprites.add(rosado)
all_sprites.add(azulado)

all_rosados.add(rosado)
all_azulados.add(azulado)


#Palavras introdutórias do tutorial e algumas variáveis para a movimentação do personagem
intro = Fundo_intro("Bem Vindo","ao","Supermariogro","Pressione SPACE para atirar","Pressione CIMA para pular","Pressione DIREITA ou ESQUERDA para mover o ogro","Caso encoste em um obstáculo, o jogo para","Pressione ENTER para continuar", (255,255,255), 80,30, (34,139,34))
PULANDO = False
tempo_pulo = 10
world_speed = -3



#Rodando musica de fundo
pygame.mixer.music.play(loops=-1)



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
    # Ajusta a velocidade do jogo.
    clock.tick(FPS)
    keys = pygame.key.get_pressed()

    # Processa os eventos (mouse, teclado, botão, etc).
    for event in pygame.event.get():

        # Verifica se apertou alguma tecla.
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                mariogro.speedx += 8
            if event.key == pygame.K_LEFT:
                mariogro.speedx -= 8
            if event.key == pygame.K_SPACE:
                mariogro.shoot()   
                      
        # Verifica se soltou alguma tecla.
        if event.type == pygame.KEYUP:
            # Dependendo da tecla, altera a velocidade.
            if event.key == pygame.K_LEFT:
                mariogro.speedx += 8
            if event.key == pygame.K_RIGHT:
                mariogro.speedx -= 8

    #Evento exclusivo para o Pulo do personagem!
        
    if not PULANDO:
        if keys[pygame.K_UP]:
            PULANDO = True
    else:
        if tempo_pulo >= -10:
            negativo = 1
            if tempo_pulo < 0:
                negativo = -1
            mariogro.rect.y -= int(tempo_pulo**2 * 0.50 * negativo) 
            #mariogro.speedx += 4
            tempo_pulo -= 1
        else:
            PULANDO = False
            tempo_pulo = 10 

    # Verifica se foi fechado.
    if event.type == pygame.QUIT:
        pygame.quit()
        sys.exit()

    all_sprites.update()
    
    # Verifica se houve colisão entre tiro e rosado 
    hits = pygame.sprite.groupcollide(all_rosados, all_bullets, True, True)
        
    # Verifica se houve colisão entre tiro e azulado
    hits2 = pygame.sprite.groupcollide(all_azulados, all_bullets, True, True)

    #Contagem de pontos
    if hits or hits2:
        pontos += 100

    #Recriando novos rosados e azulados
    for rosados in hits: 
        novo_rosado = Rosado(assets)
        all_sprites.add(novo_rosado)
        all_rosados.add(novo_rosado)
    
    for azulados in hits2: 
        novo_azulado = Azulado(assets)
        all_sprites.add(novo_azulado)
        all_azulados.add(novo_azulado)
        
    # Verifica se houve colisão entre personagem e rosados, azulados 
    hits_persona = pygame.sprite.spritecollide(mariogro, all_rosados, True)
    hits_persona2 = pygame.sprite.spritecollide(mariogro, all_azulados, True)

    if len(hits_persona) > 0 or len(hits_persona2) > 0: 
        mixer.music.pause()
        #Classe para tela final
        class Fundo_Fim(pygame.sprite.Sprite):
            def __init__(self, texto1, texto2, cor_da_letra, tamanho_do_titulo, cor_fundo):
                tela_fim = pygame.display.set_mode((LARGURA,COMPRIMENTO))
                tela_fim.fill(cor_fundo)
                self.fonte_fim = pygame.font.SysFont(None, tamanho_do_titulo)
                self.superficie1 = self.fonte_fim.render(texto1, True, cor_da_letra)
                tela_fim.blit(self.superficie1, (250, 100))
                self.fonte_fim2 = pygame.font.SysFont(None, tamanho_do_titulo)
                self.superficie2 = self.fonte_fim2.render(texto2, True, cor_da_letra)
                tela_fim.blit(self.superficie2, (150, 300))
                pygame.display.update()
        tela_fim = Fundo_Fim("Fim de jogo", "Você fez {0} pontos".format(pontos),(255,255,255),80,(0,0,0))      
        tela_fim.__init__
        JOGANDO = False
        contador = 0
        while contador < 1e100:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    pygame.quit()
                    sys.exit()
                else:
                    contador += 1
                
            

  
        # assets['boom_sound'].play()

    #Movimentação do fundo

    tela_jogo.fill((0, 0, 0))
    fundo.rect.x += world_speed
    if fundo.rect.right<0:
        fundo.rect.x += fundo.rect.width
    tela_jogo.blit(fundo.image, fundo.rect)

    fundo.rect2 = fundo.rect.copy()
    fundo.rect2.x += fundo.rect2.width

    tela_jogo.blit(fundo.image, fundo.rect2)

    all_sprites.draw(tela_jogo)
    pygame.display.flip()
>>>>>>> 029caad9637c0369b2a406cfffc403038ea451eb
