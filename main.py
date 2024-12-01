import pygame
import random


CAR_GENERATION_PROBABILITY = 0.008
CAR_VELOCITY = 0.2


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
        self.semaforos = [] #Semaforos que serao adicionados pela classe interconexao
        self.carros = [] #Carros que serao adicionados pela classe carro
        

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
    def __init__(self, rua):
        # Variaveis proprias
        self.tempoParado = 0
        self.velocidade = CAR_VELOCITY
        cor_carro =  (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)) # Cor aleatória
        self.cor = cor_carro

        # Associando o carro a uma rua
        self.rua = rua
        self.rua.carros.append(self)
        self.rua.carros_transitando += 1


        self.orientacao = self.rua.orientacao
        if self.orientacao == 'horizontal':
            self.x = rua.x
            self.y = random.randint(rua.y, rua.y + 25)
        if self.orientacao == 'vertical':
            self.x = random.randint(rua.x, rua.x + 25)
            self.y = rua.y
    
    def remover_carro(self):
        if self in self.rua.carros:
            self.rua.carros.remove(self)
            self.rua.carros_transitando -= 1

    def desenhar_carro(self):
        pygame.draw.rect(tela, self.cor, (self.x, self.y, 20, 20))

    def mover_carro(self):
        if self.orientacao == 'horizontal':
            self.x += self.velocidade
        if self.orientacao == 'vertical':
            self.y += self.velocidade
    


class interConexao:
    def __init__(self, rua1, rua2):
        self.rua1 = rua1
        self.rua2 = rua2

        #localizaçao da interconexão
        if rua1.orientacao == 'horizontal' and rua2.orientacao == 'vertical':
            self.x = rua2.x
            self.y = rua1.y
        if rua1.orientacao == 'vertical' and rua2.orientacao == 'horizontal':
            self.x = rua1.x
            self.y = rua2.y

        # apendSemaforosRua - fazer com que o semaforo seja adicionado a rua ou alguma forma da rua ter conhecimento das suas interconexoes
        if(self.rua1.orientacao == 'horizontal'):
            self.semaforo = Semafaro(self.x-30, self.y+65, self.rua1)
        else:
            self.semaforo = Semafaro(self.x+65, self.y-30, self.rua2, 1)
        
        #adiciona semaforo a rua
        self.rua1.semaforos.append(self.semaforo)

# Classe para exibir estatísticas
class displayEstatisticas:
    def __init__(self, ruas, largura_tela=800):
        self.ruas = ruas
        self.largura_tela = largura
        self.fonte = pygame.font.Font(None, 20)
    
    def desenhar_estatisticas(self):
        y = 10
        for index, rua in enumerate(self.ruas):
            titulo = self.fonte.render(f'RUA {index + 1} - {rua.orientacao}', True, (255, 255, 255))
            texto = self.fonte.render(f'Carros: {rua.carros_transitando}', True, (255, 255, 255))
            texto2 = self.fonte.render(f'Carros esperando: {rua.carros_esperando}', True, (255, 255, 255))

            tela.blit(titulo, (self.largura_tela - titulo.get_width() - 10, y))
            tela.blit(texto, (self.largura_tela - texto.get_width() - 10, y + 15))
            tela.blit(texto2, (self.largura_tela - texto2.get_width() - 10, y + 30))
            y += 50

# Classe para exibir gráfico
class Grafico:
    def __init__(self, ruas, largura_tela=800, altura_tela=600):
        self.ruas = ruas
        self.largura_tela = largura_tela
        self.altura_tela = altura_tela
        self.dados = {rua: [] for rua in ruas}
        self.cores = {rua: (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)) for rua in ruas}
        self.max_dados = 100
        self.iteracao = 0
        self.intervalo_atualizacao = 10  # Atualiza a cada 10 iterações

    def adicionar_dados(self):
        self.iteracao += 1
        if self.iteracao % self.intervalo_atualizacao == 0:
            for rua in self.ruas:
                self.dados[rua].append(rua.carros_transitando)
                if len(self.dados[rua]) > self.max_dados:
                    self.dados[rua].pop(0)

    def desenhar_grafico(self):
        for rua in self.ruas:
            cor = self.cores[rua]
            for i in range(1, len(self.dados[rua])):
                pygame.draw.line(tela, cor, (self.largura_tela - self.max_dados + i - 1, self.altura_tela - self.dados[rua][i - 1] * 5),
                                 (self.largura_tela - self.max_dados + i, self.altura_tela - self.dados[rua][i] * 5))
        
# Loop principal
running = True

# gerando duas ruas (classe)
rua1 = Rua(0, 200, largura, 50, 'horizontal')

rua2 = Rua(200, 0, 50, altura, 'vertical')
rua3 = Rua(400, 0, 50, altura, 'vertical')
rua4 = Rua(0, 400, largura, 50, 'horizontal')


carros = []
ruas = [rua1, rua2, rua3, rua4]
interconexoes = []

# Calcula com base em todas as ruas onde tem conexao entre elas e salva em uma classe conexao
def verificarInterconexoesRuas():
    for rua in ruas:
        for rua2 in ruas:
            #verifica se as ruas são diferentes e se são perpendiculares
            if (rua != rua2) and ((rua.orientacao == 'horizontal' and rua2.orientacao == 'vertical') or(rua.orientacao == 'vertical' and rua2.orientacao == 'horizontal')):
                print('Conexao encontrada')
                interconexoes.append(interConexao(rua, rua2))                   
                

verificarInterconexoesRuas()
displayEstatisticas = displayEstatisticas(ruas)
grafico = Grafico([rua1, rua2], largura, altura)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Preenche tela com preto
    tela.fill((0, 0, 0))

    # Desenha as ruas
    for rua in ruas:
        rua.desenhar_rua()

    #gerando carros aleatoriamente
    if random.random() < CAR_GENERATION_PROBABILITY:
        numRuas = len(ruas)
        ruaOrigem = ruas[random.randint(0, numRuas-1)]
        carros.append(Carro(ruaOrigem))

    #desenhando semaforos das interconexoes
    for intercon in interconexoes:
        intercon.semaforo.desenhar_semaforo()


    #desenhando carros
    for carro in carros:
        carro.desenhar_carro()
        carro.mover_carro()
        if carro.orientacao == 'horizontal':
            if carro.x > largura:
                carro.remover_carro()
        if carro.orientacao == 'vertical':
            if carro.y > altura:
                carro.remover_carro()

    #desenhando estatisticas
    displayEstatisticas.desenhar_estatisticas()

    # grafico
    grafico.adicionar_dados()
    grafico.desenhar_grafico()

    # Atualiza a tela
    pygame.display.update()

# Finaliza o pygame
pygame.quit()