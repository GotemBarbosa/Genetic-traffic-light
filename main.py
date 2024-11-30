import pygame
import random

# Iniciando o pygame
pygame.init()

# Configuraçao da janela
largura = 800
altura = 600
tela = pygame.display.set_mode((largura, altura)) # Tamanho da janela
pygame.display.set_caption("Simulaçao Semáforos") # Nome da janela

branco = (255, 255, 255)


class Rua:
    def __init__(self, x, y, largura, altura, orientacao):
        self.x = x
        self.y = y
        self.largura = largura
        self.altura = altura
        self.orientacao = orientacao
        
        self.carros_esperando = 0
        self.carros_transitando = 0
        

    def desenhar_rua(self):
        if self.orientacao == 'horizontal':
            pygame.draw.rect(tela, branco, (self.x, self.y, self.largura, 50))
        if self.orientacao == 'vertical':
            pygame.draw.rect(tela, branco, (self.x, self.y, 50, self.altura))

class Semafaro:
    def __init__(self, x, y, rua, estado=0):
        self.estado = 0 # 0 = vermelho, 1 = verde
        self.x = x
        self.y = y
        self.rua = rua
        self.estado = estado

    def desenhar_semaforo(self):
        if self.estado == 0:
            pygame.draw.circle(tela, (255, 0, 0), (self.x, self.y), 10)
        else:
            pygame.draw.circle(tela, (0, 255, 0), (self.x, self.y), 10)
        

class Carro:
    def __init__(self, x, y, rua):
        self.tempoParado = 0

        self.rua = rua
        self.orientacao = self.rua.orientacao
        self.velocidade = 0.5
        cor_carro =  (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)) # Cor aleatória
        self.cor = cor_carro

        if self.orientacao == 'horizontal':
            self.x = rua.x
            self.y = random.randint(rua.y, rua.y + 25)
        if self.orientacao == 'vertical':
            self.x = random.randint(rua.x, rua.x + 25)
            self.y = rua.y
    
    def desenhar_carro(self):

        pygame.draw.rect(tela, self.cor, (self.x, self.y, 20, 20))

    def mover_carro(self):
        if self.orientacao == 'horizontal':
            self.x += self.velocidade
        if self.orientacao == 'vertical':
            self.y += self.velocidade

# Loop principal
running = True

# gerando duas ruas (classe)
rua1 = Rua(0, 200, largura, 50, 'horizontal')

rua2 = Rua(200, 0, 50, altura, 'vertical')




semaforo1 = Semafaro(180, 180, rua1)
semaforo2 = Semafaro(270, 270, rua2, 1)

carros = []
ruas = [rua1, rua2]

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Preenche tela com preto
    tela.fill((0, 0, 0))

    # Desenha as ruas
    for rua in ruas:
        rua.desenhar_rua()

    #desenhando semaforos
    semaforo1.desenhar_semaforo()
    semaforo2.desenhar_semaforo()

    #gerando carros aleatoriamente
    if random.random() < 0.01:
        numRuas = len(ruas)
        ruaOrigem = ruas[random.randint(0, numRuas-1)]

        if random.random() < 0.5:
            carros.append(Carro(0, 200, ruaOrigem))
        else:
            carros.append(Carro(0, 200, ruaOrigem))

    #desenhando carros
    for carro in carros:
        carro.desenhar_carro()
        carro.mover_carro()
        if carro.orientacao == 'horizontal':
            if carro.x > largura:
                carros.remove(carro)
        if carro.orientacao == 'vertical':
            if carro.y > altura:
                carros.remove(carro)

    # Atualiza a tela
    pygame.display.update()

# Finaliza o pygame
pygame.quit()