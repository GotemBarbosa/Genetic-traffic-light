import pygame
import random


CAR_GENERATION_PROBABILITY = 0.008
CAR_VELOCITY = 0.5
TRAFIC_LIGHT_TIMER = 2000
DISTANCE_TRAFIC_LIGHT = 25


# Iniciando o pygame
pygame.init()

largura = 800
altura = 600
# Configuraçao da janela
tela = pygame.display.set_mode((largura, altura)) # Tamanho da janela
pygame.display.set_caption("Simulaçao Semáforos") # Nome da janela

branco = (255, 255, 255)
cinza = (200, 200, 200)
verde = (51, 204, 51)

interconexoes_area = []

class Rua:
    def __init__(self, x, y, largura, altura, orientacao, interseccao=None):
        self.x = x
        self.y = y
        self.largura = largura
        self.altura = altura
        self.orientacao = orientacao
        
        self.carros_esperando = 0
        self.carros_transitando = 0
        self.semaforos = [] #Semaforos que serao adicionados pela classe interconexao
        self.carros = [] #Carros que serao adicionados pela classe carro

        self.interseccao = interseccao  # Ponto de interseção (x, y) se houver
        

    def desenhar_rua(self):
        # Define as cores
        cor_rua = (50, 50, 50)          # Cinza para a rua
        cor_borda = (255, 255, 255)    # Branco para a borda
        cor_linha = (255, 255, 255)    # Branco para as linhas de trânsito
        
        # Desenha a rua principal
        pygame.draw.rect(tela, cor_rua, (self.x, self.y, self.largura, self.altura))
        
        # Desenha a borda branca ao redor da rua
        pygame.draw.rect(tela, cor_borda, (self.x, self.y, self.largura, self.altura), 2)
        
        # Desenhar linhas brancas na rua
        if self.orientacao == 'horizontal':
            for i in range(self.x, self.x + self.largura, 70):
                linha = pygame.Rect(i, self.y + self.altura // 2 - 1, 20, 2)
                # Verifica se a linha está dentro de alguma interconexão ou interseção
                pular_linha = False
                if self.interseccao:
                    ix, iy = self.interseccao
                    if ix - self.largura // 2 <= i <= ix + self.largura // 2:
                        pular_linha = True
                if any(inter_area.colliderect(linha) for inter_area in interconexoes_area):
                    pular_linha = True
                if not pular_linha:
                    pygame.draw.line(tela, cor_linha,
                                    (i, self.y + self.altura // 2),
                                    (i + 20, self.y + self.altura // 2), 2)
        elif self.orientacao == 'vertical':
            for i in range(self.y, self.y + self.altura, 40):
                linha = pygame.Rect(self.x + self.largura // 2 - 1, i, 2, 20)
                # Verifica se a linha está dentro de alguma interconexão ou interseção
                pular_linha = False
                if self.interseccao:
                    ix, iy = self.interseccao
                    if iy - self.altura // 2 <= i <= iy + self.altura // 2:
                        pular_linha = True
                if any(inter_area.colliderect(linha) for inter_area in interconexoes_area):
                    pular_linha = True
                if not pular_linha:
                    pygame.draw.line(tela, cor_linha,
                                    (self.x + self.largura // 2, i),
                                    (self.x + self.largura // 2, i + 20), 2)
    
    def atualizar_estatisticas(self):
        self.carros_esperando = 0
        for semaforo in self.semaforos:
            self.carros_esperando += semaforo.carros_esperando

class Semaforo:
    def __init__(self, x, y, rua, estado=0):
        self.estado = 0 # 0 = vermelho, 1 = verde
        self.x = x
        self.y = y
        self.rua = rua
        self.estado = estado
        self.timer = TRAFIC_LIGHT_TIMER
        self.carros_esperando = 0
        self.rate_carros = 0

    def desenhar_semaforo(self):
        # Cores
        cor_corpo = (50, 50, 50)         # Corpo do semáforo (cinza escuro)
        cor_borda = (0, 0, 0)            # Borda das luzes (preto)
        cor_luz_desligada = (30, 30, 30) # Luz desligada (cinza mais escuro)

        # Dimensões do semáforo
        largura_corpo = 20
        altura_corpo = 40
        raio_luz = 8
        espaco_entre_luzes = 2

        # Posição do corpo do semáforo
        corpo_x = self.x - largura_corpo // 2
        corpo_y = self.y - altura_corpo // 2

        # Desenha o corpo do semáforo
        pygame.draw.rect(tela, cor_corpo, (corpo_x, corpo_y, largura_corpo, altura_corpo), border_radius=5)

        # Posições das luzes
        luzes_y = [
            corpo_y + espaco_entre_luzes + raio_luz,                              # Luz vermelha
            corpo_y + altura_corpo - espaco_entre_luzes - raio_luz                # Luz verde
        ]
        luz_x = self.x

        # Estados das luzes
        if self.estado == 0:  # Vermelho
            cor_vermelho = (255, 0, 0)
            cor_verde = cor_luz_desligada
        elif self.estado == 1:  # Verde
            cor_vermelho = cor_luz_desligada
            cor_verde = (0, 255, 0)
        else:  # Todas apagadas
            cor_vermelho = cor_luz_desligada
            cor_verde = cor_luz_desligada

        # Desenha as luzes
        # Luz vermelha
        pygame.draw.circle(tela, cor_vermelho, (luz_x, luzes_y[0]), raio_luz)
        pygame.draw.circle(tela, cor_borda, (luz_x, luzes_y[0]), raio_luz, 1)
        # Luz verde
        pygame.draw.circle(tela, cor_verde, (luz_x, luzes_y[1]), raio_luz)
        pygame.draw.circle(tela, cor_borda, (luz_x, luzes_y[1]), raio_luz, 1)
    
    def atualizar_semaforo(self):
        self.rua.atualizar_estatisticas()
        self.timer -= 1
        if self.timer == 0:
            self.estado = 1 - self.estado
            self.timer = TRAFIC_LIGHT_TIMER
        

class Carro:
    def __init__(self, rua):
        # Variaveis proprias
        self.tempoParado = 0
        self.velocidade = random.uniform(CAR_VELOCITY - 0.1, CAR_VELOCITY + 0.1)
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
        altura_carro = 20
        largura_carro = 30

        if(self.orientacao == 'horizontal'):

            pygame.draw.rect(tela, self.cor, (self.x, self.y, largura_carro, altura_carro))
            #rodas retangulares
            pygame.draw.rect(tela, (0, 0, 0), (self.x + 2, self.y - 1, 10, 2))
            pygame.draw.rect(tela, (0, 0, 0), (self.x + 2, self.y + 19, 10, 2))
            pygame.draw.rect(tela, (0, 0, 0), (self.x + 18, self.y - 1, 10, 2))
            pygame.draw.rect(tela, (0, 0, 0), (self.x + 18, self.y + 19, 10, 2))

            #janela retangular
            pygame.draw.rect(tela, (255, 255, 255), (self.x + 15, self.y + 2, 5, 16))
        else:
            pygame.draw.rect(tela, self.cor, (self.x, self.y, altura_carro, largura_carro))
            #rodas retangulares
            pygame.draw.rect(tela, (0, 0, 0), (self.x - 1, self.y + 2, 2, 10))
            pygame.draw.rect(tela, (0, 0, 0), (self.x + 19, self.y + 2, 2, 10))
            pygame.draw.rect(tela, (0, 0, 0), (self.x - 1, self.y + 18, 2, 10))
            pygame.draw.rect(tela, (0, 0, 0), (self.x + 19, self.y + 18, 2, 10))

            #janela retangular
            pygame.draw.rect(tela, (255, 255, 255), (self.x + 2, self.y + 15, 16, 5))

    def verificar_semaforos(self):
        for semaforo in self.rua.semaforos:  
            if self.orientacao == 'horizontal':
                # Verifica se o carro está na posição correta para contar como esperando
                if semaforo.estado == 0 and (semaforo.x - DISTANCE_TRAFIC_LIGHT <= self.x + 20 <= semaforo.x):
                    if self.tempoParado == 0:
                        semaforo.carros_esperando += 1
                    self.tempoParado += 1
                    return False
            if self.orientacao == 'vertical':
                # Verifica se o carro está na posição correta para contar como esperando
                if semaforo.estado == 0 and (semaforo.y - DISTANCE_TRAFIC_LIGHT <= self.y + 20 <= semaforo.y):
                    if self.tempoParado == 0:
                        semaforo.carros_esperando += 1
                    self.tempoParado += 1
                    return False
        if self.tempoParado > 0:
            for semaforo in self.rua.semaforos:
                if self.orientacao == 'horizontal' and (semaforo.x - DISTANCE_TRAFIC_LIGHT <= self.x + 20 <= semaforo.x):
                    semaforo.carros_esperando -= 1
                if self.orientacao == 'vertical' and (semaforo.y - DISTANCE_TRAFIC_LIGHT <= self.y + 20 <= semaforo.y):
                    semaforo.carros_esperando -= 1
            self.tempoParado = 0
        return True


    def mover_carro(self):
        if self.verificar_semaforos():
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

        # Define o tamanho da área da interconexão
        self.largura_area = 60  # Ajuste conforme necessário
        self.altura_area = 60    # Ajuste conforme necessário

        # Adiciona a área da interconexão à lista global
        interconexoes_area.append(pygame.Rect(
            self.x - self.largura_area // 2 + 12,
            self.y - self.altura_area // 2 + 12,
            self.largura_area,
            self.altura_area
        ))

        # apendSemaforosRua - fazer com que o semaforo seja adicionado a rua ou alguma forma da rua ter conhecimento das suas interconexoes
        if(self.rua1.orientacao == 'horizontal'):
            self.semaforo = Semaforo(self.x-30, self.y+75, self.rua1)
        else:
            self.semaforo = Semaforo(self.x+65, self.y-50, self.rua1, 1)
        
        #adiciona semaforo a rua         
        self.rua1.semaforos.append(self.semaforo)

    def desenhar_interconexao(self):
        # Desenha o retângulo da interconexão sobrepondo as ruas
        cor_interconexao = (50, 50, 50)  # Mesma cor da rua
        pygame.draw.rect(tela, cor_interconexao, self.area_interconexao)
        # Desenha a borda branca
        pygame.draw.rect(tela, (255, 255, 255), self.area_interconexao, 2)


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
ruas = [rua1, rua2, rua3]
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
    tela.fill(verde)

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
        intercon.semaforo.atualizar_semaforo()
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