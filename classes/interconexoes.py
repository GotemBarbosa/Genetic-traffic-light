import pygame
import config
from classes.semaforo import Semaforo
interconexoes_area = []


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

    def desenhar_interconexao(self, tela):
        
        # Desenha o retângulo da interconexão sobrepondo as ruas
        cor_interconexao = (50, 50, 50)  # Mesma cor da rua
        pygame.draw.rect(tela, cor_interconexao, self.area_interconexao)
        # Desenha a borda branca
        pygame.draw.rect(tela, (255, 255, 255), self.area_interconexao, 2)
