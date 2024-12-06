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
        self.largura_area = 50  # Ajuste conforme necessário
        self.altura_area = 50    # Ajuste conforme necessário

        # Adiciona a área da interconexão à lista global
        
        self.area_interconexao = pygame.Rect(
            self.x - self.largura_area // 2 + 25,
            self.y - self.altura_area // 2 + 25,
            self.largura_area,
            self.altura_area
        )

        interconexoes_area.append(self.area_interconexao)
        

        # apendSemaforosRua - fazer com que o semaforo seja adicionado a rua ou alguma forma da rua ter conhecimento das suas interconexoes
        if(self.rua1.orientacao == 'horizontal'):
            self.semaforo = Semaforo(self.x-30, self.y+75, self.rua1)
        else:
            self.semaforo = Semaforo(self.x+65, self.y-50, self.rua1, 1)
        
        #adiciona semaforo a rua         
        self.rua1.semaforos.append(self.semaforo)





    def Desenhar_interconexao(self, tela):
        # Cor da interconexão
        cor_interconexao = (50, 50, 50)  # Cor da rua

        # Desenha o retângulo da interconexão
        pygame.draw.rect(tela, cor_interconexao, self.area_interconexao)
        # Desenha a borda branca
        # pygame.draw.rect(tela, (255, 255, 255), self.area_interconexao, 2)

        # Tamanho da rua (fixo em 50)
        tamanho_rua = 50

        # Protuberâncias para as faixas de pedestre
        comprimento_protuberancia = tamanho_rua // 2
        largura_protuberancia = tamanho_rua

        # Coordenadas da interconexão
        x_centro = self.area_interconexao.centerx
        y_centro = self.area_interconexao.centery

        # Cor da protuberância
        cor_protuberancia = cor_interconexao

        # Protuberâncias nas quatro direções
        # Esquerda
        rect_esquerda = pygame.Rect(
            self.area_interconexao.left - comprimento_protuberancia,
            y_centro - largura_protuberancia // 2,
            comprimento_protuberancia,
            largura_protuberancia
        )
        pygame.draw.rect(tela, cor_protuberancia, rect_esquerda)

        # Direita
        rect_direita = pygame.Rect(
            self.area_interconexao.right + 0,
            y_centro - largura_protuberancia // 2,
            comprimento_protuberancia,
            largura_protuberancia
        )
        pygame.draw.rect(tela, cor_protuberancia, rect_direita)

        # Cima
        rect_cima = pygame.Rect(
            x_centro - largura_protuberancia // 2,
            self.area_interconexao.top - comprimento_protuberancia,
            largura_protuberancia,
            comprimento_protuberancia
        )
        pygame.draw.rect(tela, cor_protuberancia, rect_cima)

        # Baixo
        rect_baixo = pygame.Rect(
            x_centro - largura_protuberancia // 2,
            self.area_interconexao.bottom,
            largura_protuberancia,
            comprimento_protuberancia
        )
        pygame.draw.rect(tela, cor_protuberancia, rect_baixo)

        # Desenha apenas a borda superior e inferior da protuberância da esquerda
        pygame.draw.line(tela, (255, 255, 255), rect_esquerda.topleft , rect_esquerda.topright, 2)
        pygame.draw.line(tela, (255, 255, 255), 
                        (rect_esquerda.bottomleft[0], rect_esquerda.bottomleft[1] - 2), 
                        (rect_esquerda.bottomright[0], rect_esquerda.bottomright[1] - 2), 2)

        # Direita
        pygame.draw.line(tela, (255, 255, 255), rect_direita.topleft, rect_direita.topright, 2)
        pygame.draw.line(tela, (255, 255, 255), 
                                (rect_direita.bottomleft[0], rect_direita.bottomleft[1] - 2), 
                                (rect_direita.bottomright[0], rect_direita.bottomright[1] - 2), 2)

        # Cima
        pygame.draw.line(tela, (255, 255, 255), rect_cima.topleft, rect_cima.bottomleft, 2)
        pygame.draw.line(tela, (255, 255, 255), 
                                (rect_cima.topright[0]-2, rect_cima.topright[1]), 
                                (rect_cima.bottomright[0]-2, rect_cima.bottomright[1]), 2)
        

        # Baixo
        pygame.draw.line(tela, (255, 255, 255), rect_baixo.topleft, rect_baixo.bottomleft, 2)
        pygame.draw.line(tela, (255, 255, 255), 
                                (rect_baixo.topright[0]-2, rect_baixo.topright[1]), 
                                (rect_baixo.bottomright[0]-2, rect_baixo.bottomright[1]), 2)
        # Configurações das faixas de pedestre
        cor_faixa = (255, 255, 255)
        largura_faixa = 5
        espaco_entre_faixas = 10
        num_faixas = 3
        distancia_interconexao = 10  # Distância para afastar as faixas da interconexão

        # Cálculo do tamanho total das faixas
        largura_total_faixas = num_faixas * largura_faixa + (num_faixas - 1) * espaco_entre_faixas

        # Função para desenhar faixas verticais (paralelas ao eixo Y)
        def desenhar_faixas_verticais(x_inicial, y_inicial, comprimento):
            for i in range(num_faixas):
                x = x_inicial + i * (largura_faixa + espaco_entre_faixas)
                faixa = pygame.Rect(x, y_inicial, largura_faixa, comprimento)
                pygame.draw.rect(tela, cor_faixa, faixa)

        # Função para desenhar faixas horizontais (paralelas ao eixo X)
        def desenhar_faixas_horizontais(x_inicial, y_inicial, comprimento):
            for i in range(num_faixas):
                y = y_inicial + i * (largura_faixa + espaco_entre_faixas)
                faixa = pygame.Rect(x_inicial, y, comprimento, largura_faixa)
                pygame.draw.rect(tela, cor_faixa, faixa)

        # Faixas na esquerda e direita devem ser horizontais
        desenhar_faixas_horizontais(
            rect_esquerda.right - distancia_interconexao - largura_total_faixas + 15,
            rect_esquerda.top + (largura_protuberancia - (num_faixas * largura_faixa + (num_faixas - 1) * espaco_entre_faixas)) // 2,
            rect_esquerda.width
        )

        desenhar_faixas_horizontais(
            rect_direita.left + distancia_interconexao - 5,
            rect_direita.top + (largura_protuberancia - (num_faixas * largura_faixa + (num_faixas - 1) * espaco_entre_faixas)) // 2,
            rect_direita.width
        )

        # Faixas em cima e embaixo devem ser verticais
        desenhar_faixas_verticais(
            rect_cima.left + (largura_protuberancia - (num_faixas * largura_faixa + (num_faixas - 1) * espaco_entre_faixas)) // 2,
            rect_cima.bottom + distancia_interconexao +45,
            rect_cima.height 
        )

        desenhar_faixas_verticais(
            rect_baixo.left + (largura_protuberancia - (num_faixas * largura_faixa + (num_faixas - 1) * espaco_entre_faixas)) // 2,
            rect_baixo.top - distancia_interconexao - largura_total_faixas - 35,
            rect_baixo.height
        )