from classes.rua import Rua
from classes.interconexoes import interConexao, interconexoes_area
from classes.carro import Carro
from config import *
import random

class Individuo:

    def __init__(self, id):
            self.id = id  # Identificador do indivíduo
            self.ruas = []  # Lista de ruas do indivíduo
            self.interconexoes = []  # Lista de interconexões
            self.carros = []  # Lista de carros
            self.fitness = None  # Valor de fitness do indivíduo

            # Inicializar o grid do indivíduo
            self.inicializar_grid()


    def inicializar_grid(self):
            # Pode-se fazer para variar o grid 

            # rua1 = Rua(0, 200, LARGURA_TELA, 50, 'horizontal')
            # rua2 = Rua(250, 0, 50, ALTURA_TELA, 'vertical')
            # rua3 = Rua(500, 0, 50, ALTURA_TELA, 'vertical')
            # rua4 = Rua(0, 400, LARGURA_TELA, 50, 'horizontal')

            rua1 = Rua(0, ALTURA_TELA // 4, LARGURA_TELA, 50, 'horizontal')
            rua2 = Rua(LARGURA_TELA // 4 - 100, 0, 50, ALTURA_TELA, 'vertical')
            rua3 = Rua(3 * LARGURA_TELA // 4 - 250, 0, 50, ALTURA_TELA, 'vertical')
            rua4 = Rua(0, 3 * ALTURA_TELA // 4, LARGURA_TELA, 50, 'horizontal')

            self.ruas = [rua1, rua2, rua3, rua4]

            # Verificar interconexões entre as ruas
            self.verificar_interconexoes()

    def verificar_interconexoes(self):
            for rua in self.ruas:
                for rua2 in self.ruas:
                    if (rua != rua2) and (
                        (rua.orientacao == 'horizontal' and rua2.orientacao == 'vertical') or
                        (rua.orientacao == 'vertical' and rua2.orientacao == 'horizontal')
                    ):
                        intercon = interConexao(rua, rua2)
                        self.interconexoes.append(intercon)

    def avaliar_fitness(self):
        # Avaliar o fitness do indivíduo
        pass

    def mutacao(self):
        # Realizar mutação no indivíduo
        pass

    def crossover(self, outro_individuo):
        # Realizar crossover com outro indivíduo
        pass

    def desenhar(self, tela):
        # Desenha as ruas do indivíduo
        for rua in self.ruas:
            rua.desenhar_rua(tela, interconexoes_area)

        # Desenha as interconexões e semáforos
        for intercon in self.interconexoes:
            intercon.semaforo.atualizar_semaforo()
            intercon.semaforo.desenhar_semaforo(tela)
            intercon.Desenhar_interconexao(tela)

        # Desenha os carros
        for carro in self.carros:
            carro.desenhar_carro(tela)
            carro.mover_carro()
            # Verificar se o carro saiu da tela e removê-lo
            if carro.x > LARGURA_TELA or carro.y > ALTURA_TELA:
                carro.remover_carro()

    def gerar_carros(self):
        # Gerar carros aleatoriamente nas ruas do indivíduo
        if random.random() < CAR_GENERATION_PROBABILITY:
            rua_origem = random.choice(self.ruas)
            carro = Carro(rua_origem)
            self.carros.append(carro)

    def atualizar(self):
         # Atualiza os semáforos nas interconexões
        for intercon in self.interconexoes:
            intercon.semaforo.atualizar_semaforo()
        
        # Atualiza os carros
        for carro in self.carros[:]:  # Usar uma cópia da lista para evitar problemas ao remover itens
            carro.mover_carro()
            # Verificar se o carro saiu da tela e removê-lo
            if carro.x > LARGURA_TELA or carro.y > ALTURA_TELA:
                carro.remover_carro()