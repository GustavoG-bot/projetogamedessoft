#Importar Bibliotecas necessárias para o jogo
import pygame
from random import randint
from os import path

#Pasta que contêm os arquivos: 
img_dir = path.join(path.dirname(__file__), 'img')
som_dir = path.join(path.dirname(__file__), 'sons')
font_dir = path.join(path.dirname(__file__), 'font')

#Inicializando o pygame
pygame.init()

#Váriavel para velocidade
clock = pygame.time.Clock()


#Gerando Tela do Jogo
tamanho = (800,600)
tela_jogo = pygame.display.set_mode(tamanho)
pygame.display.set_caption('Super Marioigi Run!')
FPS = 100

#Imagem
fundo_arquivo = pygame.image.load(path.join(img_dir,'grama.png')).convert()
fundo = pygame.transform.scale(fundo_arquivo, (tamanho))
fundo_rect = fundo.get_rect()

#Personagens
tamanho_personagem = (90,90)
personagem_arquivo = pygame.image.load(path.join(img_dir,'mariogro.png')).convert_alpha()
personagem = pygame.transform.scale(personagem_arquivo,(tamanho_personagem))
personagem_rect = personagem.get_rect()

#Obstáculos
tamanho_arvore = (90,90)
arvore_arquivo = pygame.image.load(path.join(img_dir,'arvorezuada.png')).convert_alpha()
arvore = pygame.transform.scale(arvore_arquivo,(tamanho_arvore))
arvore_rect = personagem.get_rect()


#Atributos do personagem
posX_personagem = 40
posY_personagem = 397
tempo_pulo = 10
velocidade_personagem = 5
vidas = 3

PULANDO = False

#Sistema de Pontos e Vidas


JOGANDO = True 

velocidade_fundo = 0
velocidade_arvore = 0
while JOGANDO and vidas > 0:

    # Ajusta a velocidade do jogo.
    clock.tick(FPS)

    rel_x = velocidade_fundo % fundo.get_rect().width
    tela_jogo.blit(fundo,(rel_x-fundo.get_rect().width ,0))
    tela_jogo.blit(personagem,(posX_personagem,posY_personagem))

    a = 50

    if rel_x < 800 :
        tela_jogo.blit(fundo, (rel_x,0))
        tela_jogo.blit(personagem,(posX_personagem,posY_personagem))
        tela_jogo.blit(arvore, (rel_x+a,397))
    
    velocidade_fundo -= 2
    velocidade_arvore -= 2
    posX_personagem -= 2
  
    # Processa os eventos (mouse, teclado, botão, etc).
    for event in pygame.event.get():

        # Verifica se foi fechado.
        if event.type == pygame.QUIT:
            JOGANDO = False
      
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

    if posX_personagem == 0:
        vidas -= 1
        if vidas <= 0:
            continue


    #Tela Games
    pygame.display.flip()
    pygame.display.update()
