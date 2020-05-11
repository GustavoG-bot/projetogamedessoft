#Importar Bibliotecas necessárias para o jogo
import pygame
from random import randint
from os import path

#Pasta que contêm os arquivos: 
img_dir = path.join(path.dirname(__file__), 'img')
som_dir = img_dir = path.join(path.dirname(__file__), 'sons')

#Inicializando o pygame
pygame.init()

#Váriavel para velocidade
clock = pygame.time.Clock()


#Gerando Tela do Jogo
tamanho = (800,600)
tela_jogo = pygame.display.set_mode(tamanho)
pygame.display.set_caption('Super Marioigi Run!')
superficie = pygame.display.set_mode(tamanho)
FPS = 30

JOGANDO = True 

class teladefundo():
    def __init__(self):
        #Renderizando as imagens e adicionando-as ao fundo
        self.imagemfundo = pygame.image.load(path.join(img_dir,'mariotime.png'))
        self.rectimagemfundo = self.imagemfundo.get.rect()
        self.imagemfundo = pygame.transform.scale(self.imagemfundo, (800,600))
        self.rectIMfundo = self.imagemfundo.get.rect()

        #Alterando as posições e definido elas inicialmente 
        self.fundoY1 = 0
        self.fundoX1 = 0

        self.fundoY2 = self.rectIMfundo.height 
        self.fundoX2 = 0 

        #Velocidade do fundo
        self.movendovelocidade = 5

    #Função pra colocar como as posições vão ser alteradas
    def update(self):
        self.fundoY1 -= self.movendovelocidade
        self.fundoY2 -= self.movendovelocidade
        if self.fundoX1 <= - self.rectIMfundo.height:
            self.fundoX1 = self.rectIMfundo.height
        if self.fundoX2 <= - self.rectIMfundo.height:
            self.fundoX2 = self.rectIMfundo.height

    #Renderizar imagens 
    def renderizando (self):
        superficie.blit(self.imagemfundo, (self.fundoX1,self.fundoY1))
        superficie.blit(self.imagemfundo, (self.fundoX2,self.fundoY2))
#class Jogadores():




while JOGANDO:
    # Ajusta a velocidade do jogo.
    clock.tick(FPS)
  
    # Processa os eventos (mouse, teclado, botão, etc).
    for event in pygame.event.get():

        # Verifica se foi fechado.
        if event.type == pygame.QUIT:
            JOGANDO = False
        
        #if event.type == pygame.KEYUP:

        #if event.type == pygame.
            
    #Preenche com cor
    tela_jogo = teladefundo()
    pygame.display.update()