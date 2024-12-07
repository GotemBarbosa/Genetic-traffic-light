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
            self.semaforos = []  # Lista de semáforos
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
            # rua3 = Rua(3 * LARGURA_TELA // 4 - 250, 0, 50, ALTURA_TELA, 'vertical')
            # rua4 = Rua(0, 3 * ALTURA_TELA // 4, LARGURA_TELA, 50, 'horizontal')

            self.ruas = [rua1, rua2]

            # Verificar interconexões entre as ruas
            self.verificar_interconexoes()

            # Adicionar semáforos à lista de semáforos
            for rua in self.ruas:
                for semaforo in rua.semaforos:
                    self.semaforos.append(semaforo)

    def verificar_interconexoes(self):
            for rua in self.ruas:
                for rua2 in self.ruas:
                    if (rua != rua2) and (
                        (rua.orientacao == 'horizontal' and rua2.orientacao == 'vertical') or
                        (rua.orientacao == 'vertical' and rua2.orientacao == 'horizontal')
                    ):
                        intercon = interConexao(rua, rua2)
                        self.interconexoes.append(intercon)

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

class Individuo_evol:
    def __init__(self, num_semaforos):
        self.open_time = [random.randint(0, 300) for _ in range(num_semaforos)] 
        self.state = []
        self.tempoAcumulado = [0]*num_semaforos
        self.penalizacao = [0]*num_semaforos
        self.fitness_total = int(1e9)
        self.fitness_penalizacao = int(1e9)
        self.fitness_tempo_acumulado = int(1e9)
        for i in range(num_semaforos):
            self.state.append(random.randint(0, 1))
        


        
