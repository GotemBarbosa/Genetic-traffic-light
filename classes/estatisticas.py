import pygame
import random
from classes.semaforo import Semaforo
from config import *

# Classe para exibir estatísticas
class displayEstatisticas:
    def __init__(self, ruas, largura_tela=800):
        self.ruas = ruas
        self.largura_tela = LARGURA_TELA
        self.fonte = pygame.font.Font(None, 20)
    
    def desenhar_estatisticas(self,tela):
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

    def desenhar_grafico(self,tela):
        for rua in self.ruas:
            cor = self.cores[rua]
            for i in range(1, len(self.dados[rua])):
                pygame.draw.line(tela, cor, (self.largura_tela - self.max_dados + i - 1, self.altura_tela - self.dados[rua][i - 1] * 5),
                                 (self.largura_tela - self.max_dados + i, self.altura_tela - self.dados[rua][i] * 5))