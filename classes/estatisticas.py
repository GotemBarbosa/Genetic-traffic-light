import pygame
import random
from classes.semaforo import Semaforo
from config import *

# Classe para exibir estatísticas
class DisplayEstatisticas:
    def __init__(self, ruas, largura_tela=800):
        self.ruas = ruas
        self.largura_tela = largura_tela
        self.altura_tela = ALTURA_TELA
        pygame.font.init()
        self.fonte_titulo = pygame.font.SysFont('Arial', 18, bold=True)
        self.fonte_texto = pygame.font.SysFont('Arial', 14)
        self.cor_fundo = (40, 40, 40)
        self.cor_texto = (255, 255, 255)
        self.cor_titulo = (255, 215, 0)
        self.cor_borda = (255, 255, 255)
        self.padding = 8

        self.melhor_fitness_geral = int(1e9)

    def desenhar_estatisticas(self, tela, geracao, individuo_evol):
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

        fitness_melhor = individuo_evol.fitness
        fitness_melhor_texto = self.fonte_texto.render(f'Melhor Fitness atual: {fitness_melhor:.2f}', True, self.cor_texto)
        tela.blit(fitness_melhor_texto, (x_painel + self.padding, y_offset))
        y_offset += fitness_melhor_texto.get_height() + self.padding

        if(fitness_melhor < self.melhor_fitness_geral):
            self.melhor_fitness_geral = fitness_melhor
        
        fitness_melhor_geral_texto = self.fonte_texto.render(f'Melhor fitness encontrado: {self.melhor_fitness_geral:.2f}', True, self.cor_texto)
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

            # Carros esperando
            carros_esperando = self.fonte_texto.render(f'Esperando: {rua.carros_esperando}', True, self.cor_texto)
            tela.blit(carros_esperando, (x_painel + self.padding + 5, y_offset))
            y_offset += carros_esperando.get_height() + self.padding

            tempo = self.fonte_texto.render(f'Tempo aberto: {individuo_evol.open_time[index]}', True, self.cor_texto)
            tela.blit(tempo, (x_painel + self.padding + 5, y_offset))
            y_offset += tempo.get_height() + 2
            
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