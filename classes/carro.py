import pygame
import random
from classes.rua import Rua
from config import *

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

    def desenhar_carro(self, tela):
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