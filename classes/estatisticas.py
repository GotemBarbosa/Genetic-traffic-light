import pygame
import random
from classes.semaforo import Semaforo
from config import *
import pygame
import matplotlib.pyplot as plt
import numpy as np
import io
from PIL import Image

# Classe para exibir estatísticas
class DisplayEstatisticas:
    def __init__(self, ruas, largura_tela=800):
        self.ruas = ruas
        self.largura_tela = largura_tela
        self.altura_tela = ALTURA_TELA
        pygame.font.init()
        self.fonte_titulo = pygame.font.SysFont('Arial', 18, bold=True)
        self.fonte_texto = pygame.font.SysFont('Arial', 14)
        self.fonte_texto_pequeno = pygame.font.SysFont('Arial', 10)
        self.cor_fundo = (40, 40, 40)
        self.cor_texto = (255, 255, 255)
        self.cor_titulo = (255, 215, 0)
        self.cor_borda = (255, 255, 255)
        self.padding = 8

        self.melhor_fitness_geral = int(1e9)

    def desenhar_estatisticas(self, tela, geracao, individuo_evol, individuo_atual):
        largura_painel = 180  # Reduzir a largura do painel
        altura_painel = self.altura_tela
        x_painel = self.largura_tela - largura_painel
        y_painel = 0

        

        # Desenha o painel de fundo
        painel_rect = pygame.Rect(x_painel, y_painel, largura_painel, altura_painel)
        pygame.draw.rect(tela, self.cor_fundo, painel_rect)
        pygame.draw.rect(tela, self.cor_borda, painel_rect, 1)

        y_offset = y_painel + self.padding

        geracao = self.fonte_titulo.render(f'Geração: {geracao}', True, self.cor_titulo)
        tela.blit(geracao, (x_painel + self.padding, y_offset))
        y_offset += geracao.get_height() + self.padding

        fitness_melhor = individuo_evol.fitness_total
        fitness_melhor_texto = self.fonte_texto_pequeno.render(f'Melhor Fitness atual: {fitness_melhor:.2f}', True, self.cor_texto)
        tela.blit(fitness_melhor_texto, (x_painel + self.padding, y_offset))
        y_offset += fitness_melhor_texto.get_height() + self.padding

        if(fitness_melhor < self.melhor_fitness_geral):
            self.melhor_fitness_geral = fitness_melhor
        
        fitness_melhor_geral_texto = self.fonte_texto_pequeno.render(f'Melhor fitness encontrado: {self.melhor_fitness_geral:.2f}', True, self.cor_texto)
        tela.blit(fitness_melhor_geral_texto, (x_painel + self.padding, y_offset))
        y_offset += fitness_melhor_geral_texto.get_height() + self.padding

        for index, rua in enumerate(self.ruas):
            # Título da rua
            titulo_rua = self.fonte_texto.render(f'Rua {index + 1} - {rua.orientacao}', True, self.cor_titulo)
            tela.blit(titulo_rua, (x_painel + self.padding, y_offset))
            y_offset += titulo_rua.get_height() + 2

            # Carros transitando
            carros_transitando = self.fonte_texto.render(f'Transitando: {rua.carros_transitando}', True, self.cor_texto)
            tela.blit(carros_transitando, (x_painel + self.padding + 5, y_offset))
            y_offset += carros_transitando.get_height() + 2


            for key, semaforo in enumerate(individuo_atual.ruas[index].semaforos):
                estado_semaforo = self.fonte_texto.render(f'Semaforo {key} | estado: {semaforo.estado_inicial}', True, self.cor_texto)
                tela.blit(estado_semaforo, (x_painel + self.padding + 5, y_offset))
                y_offset += estado_semaforo.get_height() + 2

                carros_esperando = self.fonte_texto.render(f'Carros esperando: {semaforo.carros_esperando}', True, self.cor_texto)
                tela.blit(carros_esperando, (x_painel + self.padding + 5, y_offset))
                y_offset += carros_esperando.get_height() + 2

                tempo_aberto = self.fonte_texto.render(f'Tempo aberto: {semaforo.timer_clock}', True, self.cor_texto)
                tela.blit(tempo_aberto, (x_painel + self.padding + 5, y_offset))
                y_offset += tempo_aberto.get_height() + 2

            # Linha divisória entre ruas
            pygame.draw.line(tela, (100, 100, 100), (x_painel + self.padding, y_offset), (x_painel + largura_painel - self.padding, y_offset))
            y_offset += self.padding


        # Espaço para adicionar mais estatísticas futuramente

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

    def desenhar_grafico(self,tela):
        for rua in self.ruas:
            cor = self.cores[rua]
            for i in range(1, len(self.dados[rua])):
                pygame.draw.line(tela, cor, (self.largura_tela - self.max_dados + i - 1, self.altura_tela - self.dados[rua][i - 1] * 5),
                                 (self.largura_tela - self.max_dados + i, self.altura_tela - self.dados[rua][i] * 5))
                
class GraficoFitness:
    def __init__(self, largura_tela=800, altura_tela=600, largura_grafico=150, altura_grafico=100, posicao=(500, 400)):
        """
        Inicializa o gráfico de fitness.

        :param largura_tela: Largura total da tela.
        :param altura_tela: Altura total da tela.
        :param largura_grafico: Largura do gráfico.
        :param altura_grafico: Altura do gráfico.
        :param posicao: Tupla (x, y) representando a posição superior esquerda do gráfico.
        """
        self.largura_tela = largura_tela
        self.altura_tela = altura_tela
        self.largura_grafico = largura_grafico
        self.altura_grafico = altura_grafico
        self.posicao = posicao  # Posição (x, y) do canto superior esquerdo do gráfico
        self.dados = []
        self.max_dados = 100
        self.cor = (255, 0, 0)  # Vermelho para fitness
        self.padding = 50  # Espaço para margens e rótulos dentro do gráfico
        self.fonte = pygame.font.SysFont(None, 20)  # Fonte para rótulos

    def adicionar_dado(self, fitness):
        self.dados.append(fitness)
        if len(self.dados) > self.max_dados:
            self.dados.pop(0)

# class GraficoFitness:
#     def __init__(self, largura_tela=800, altura_tela=600, largura_grafico=150, altura_grafico=100, posicao=(500, 400)):
#         """
#         Inicializa o gráfico de fitness.

#         :param largura_tela: Largura total da tela.
#         :param altura_tela: Altura total da tela.
#         :param largura_grafico: Largura do gráfico.
#         :param altura_grafico: Altura do gráfico.
#         :param posicao: Tupla (x, y) representando a posição superior esquerda do gráfico.
#         """
#         self.largura_tela = largura_tela
#         self.altura_tela = altura_tela
#         self.largura_grafico = largura_grafico
#         self.altura_grafico = altura_grafico
#         self.posicao = posicao  # Posição (x, y) do canto superior esquerdo do gráfico
#         self.dados = []
#         self.max_dados = 100
#         self.cor = (255, 0, 0)  # Vermelho para fitness
#         self.padding = 50  # Espaço para margens e rótulos dentro do gráfico
#         self.fonte = pygame.font.SysFont(None, 20)  # Fonte para rótulos

#     def adicionar_dado(self, fitness):
#         self.dados.append(fitness)
#         if len(self.dados) > self.max_dados:
#             self.dados.pop(0)

#     def desenhar_grafico(self, tela):
#             if len(self.dados) < 2:
#                 return

#             # Definir área do gráfico
#             x_inicio, y_inicio = self.posicao
#             largura_area = self.largura_grafico
#             altura_area = self.altura_grafico

#             # Determina escala fixa de 0 a 1000
#             max_fitness = 1000
#             min_fitness = 0
#             range_fitness = max_fitness - min_fitness

#             # Desenhar fundo do gráfico
#             pygame.draw.rect(tela, (230, 230, 230), (x_inicio, y_inicio, largura_area, altura_area))

#             # Desenhar linhas de grade horizontais
#             num_linhas_grade = 5
#             for i in range(num_linhas_grade + 1):
#                 y = y_inicio + i * altura_area / num_linhas_grade
#                 pygame.draw.line(tela, (200, 200, 200), (x_inicio, y), (x_inicio + largura_area, y), 1)
#                 # Rótulos das linhas de grade
#                 fitness_label = self.fonte.render(f"{max_fitness - i * range_fitness / num_linhas_grade:.2f}", True, (0, 0, 0))
#                 tela.blit(fitness_label, (x_inicio - self.padding + 10, y - fitness_label.get_height() / 2))

#             # Desenhar linhas de grade verticais (menos frequentes para reduzir a "velocidade")
#             num_linhas_grade_vert = 10  # Aumentar o número de linhas verticais para mover mais devagar
#             for i in range(num_linhas_grade_vert + 1):
#                 x = x_inicio + i * largura_area / num_linhas_grade_vert
#                 pygame.draw.line(tela, (200, 200, 200), (x, y_inicio), (x, y_inicio + altura_area), 1)

#             # Desenhar eixos
#             pygame.draw.line(tela, (0, 0, 0), (x_inicio, y_inicio), (x_inicio, y_inicio + altura_area), 2)  # Eixo Y
#             pygame.draw.line(tela, (0, 0, 0), (x_inicio, y_inicio + altura_area), (x_inicio + largura_area, y_inicio + altura_area), 2)  # Eixo X

#             # Calcular espaçamento entre os pontos
#             espaçamento_x = largura_area / self.max_dados

#             # Desenhar linha do gráfico de fitness
#             for i in range(1, len(self.dados)):
#                 x1 = x_inicio + (i - 1) * espaçamento_x
#                 y1 = y_inicio + altura_area - ((self.dados[i - 1] - min_fitness) / range_fitness) * altura_area
#                 x2 = x_inicio + i * espaçamento_x
#                 y2 = y_inicio + altura_area - ((self.dados[i] - min_fitness) / range_fitness) * altura_area
#                 pygame.draw.line(tela, self.cor, (x1, y1), (x2, y2), 2)

#             # Opcional: Desenhar pontos nos dados
#             for i in range(len(self.dados)):
#                 x = x_inicio + i * espaçamento_x
#                 y = y_inicio + altura_area - ((self.dados[i] - min_fitness) / range_fitness) * altura_area
#                 pygame.draw.circle(tela, self.cor, (int(x), int(y)), 3)

#             # Mostrar valor atual se mudou em relação à última iteração
#             if self.dados[-1] != self.dados[-2]:
#                 valor_atual_label = self.fonte.render(f"{self.dados[-1]:.2f}", True, (0, 0, 0))
#                 tela.blit(valor_atual_label, (x_inicio + largura_area + 10, y_inicio + altura_area - ((self.dados[-1] - min_fitness) / range_fitness) * altura_area - valor_atual_label.get_height() / 2))

class GraficoFitness:
    def __init__(self, largura_tela=800, altura_tela=600, largura_grafico=150, altura_grafico=100, posicao=(500, 400)):
        """
        Inicializa o gráfico de fitness.

        :param largura_tela: Largura total da tela.
        :param altura_tela: Altura total da tela.
        :param largura_grafico: Largura do gráfico.
        :param altura_grafico: Altura do gráfico.
        :param posicao: Tupla (x, y) representando a posição superior esquerda do gráfico.
        """
        self.largura_tela = largura_tela
        self.altura_tela = altura_tela
        self.largura_grafico = largura_grafico
        self.altura_grafico = altura_grafico
        self.posicao = posicao  # Posição (x, y) do canto superior esquerdo do gráfico
        self.dados = []
        self.max_dados = 100
        self.grafico = None  # Armazena a imagem do gráfico
        self.dados_mudaram = False  # Flag para indicar se os dados mudaram

    def adicionar_dado(self, fitness):
        self.dados.append(fitness)
        if len(self.dados) > self.max_dados:
            self.dados.pop(0)
        self.dados_mudaram = True  # Indica que os dados mudaram

    def criar_grafico(self):
        # Cria o gráfico com Matplotlib
        fig, ax = plt.subplots(figsize=(self.largura_grafico / 100, self.altura_grafico / 100), dpi=100)
        ax.plot(self.dados, color='red')
        ax.set_ylim(0, 1000)

        # Converte o gráfico em uma imagem
        buf = io.BytesIO()
        plt.savefig(buf, format='PNG')
        buf.seek(0)
        image = Image.open(buf)
        image = image.convert('RGBA')
        size = image.size
        image = pygame.image.fromstring(image.tobytes(), size, 'RGBA')
        buf.close()
        plt.close(fig)
        return image

    def desenhar_grafico(self, tela):
        if len(self.dados) < 2:
            return

        # Cria o gráfico apenas se os dados mudaram
        if self.dados_mudaram:
            self.grafico = self.criar_grafico()
            self.dados_mudaram = False

        # Desenha o gráfico na tela do Pygame
        if self.grafico:
            tela.blit(self.grafico, self.posicao)
