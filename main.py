import pygame

# Iniciando o pygame
pygame.init()

# Configuraçao da janela
largura = 800
altura = 600
tela = pygame.display.set_mode((largura, altura)) # Tamanho da janela
pygame.display.set_caption("Simulaçao Semáforos") # Nome da janela

branco = (255, 255, 255)


class Rua:
    def __init__(self):
        self.carros_esperando = 0
        self.carros_transitando = 0

    def desenhar_rua(self, x, y, largura, altura, orientacao):
        if orientacao == 'horizontal':
            pygame.draw.rect(tela, branco, (x, y, largura, 50))
        if orientacao == 'vertical':
            pygame.draw.rect(tela, branco, (x, y, 50, altura))

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
    def __init__(self, x, y, rua, orientacao):
        self.tempoParado = 0
        self.x = x
        self.y = y
        self.rua = rua
        self.orientacao = orientacao
    
    def desenhar_carro(self):
        pygame.draw.rect(tela, (255, 0, 0), (self.x, self.y, 20, 20))


# Loop principal
running = True

# gerando duas ruas (classe)
rua1 = Rua()
rua2 = Rua()
semaforo1 = Semafaro(180, 180, rua1)
semaforo2 = Semafaro(270, 270, rua2, 1)
Carro1 = Carro(0, 200, rua1, 'horizontal')
Carro2 = Carro(200, 0, rua2, 'vertical')

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Preenche tela com preto
    tela.fill((0, 0, 0))

    # Desenha as ruas
    rua1.desenhar_rua(0, 200, largura, 50, 'horizontal')
    rua2.desenhar_rua(200, 0, 50, altura, 'vertical')


    # Desenha os carros
    Carro1.desenhar_carro()
    Carro2.desenhar_carro()

    #desenhando semaforos
    semaforo1.desenhar_semaforo()
    semaforo2.desenhar_semaforo()


    # Atualiza a tela
    pygame.display.update()

# Finaliza o pygame
pygame.quit()