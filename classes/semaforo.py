import pygame
from classes.rua import Rua
from config import TRAFIC_LIGHT_TIMER

class Semaforo:
    def __init__(self, x, y, rua, estado=0, initial_timer=TRAFIC_LIGHT_TIMER):
        self.estado = 0 # 0 = vermelho, 1 = verde
        self.x = x
        self.y = y
        self.rua = rua
        self.estado = estado
        self.estado_inicial = estado
        self.timer_clock = initial_timer #TEMPO QUE O SEMAFORO FICA EM CADA ESTADO
        self.timer = self.timer_clock #tempo atual dele ate mudar de estado
        self.carros_esperando = 0
        self.rate_carros = 0


    def desenhar_semaforo(self,tela):
        # Cores
        cor_corpo = (50, 50, 50)         # Corpo do semáforo (cinza escuro)
        cor_borda = (0, 0, 0)            # Borda das luzes (preto)
        cor_luz_desligada = (30, 30, 30) # Luz desligada (cinza mais escuro)
        cor_poste = (80, 80, 80)         # Cor do poste (cinza escuro)


        # Dimensões do semáforo
        largura_corpo = 20
        altura_corpo = 40
        raio_luz = 8
        espaco_entre_luzes = 2

        # Dimensões do poste
        largura_poste = 5
        altura_poste = 20

        # Posição do corpo do semáforo
        corpo_x = self.x - largura_corpo // 2
        corpo_y = self.y - altura_corpo // 2

        # Posição do poste
        poste_x = self.x - largura_poste // 2
        poste_y = corpo_y + altura_corpo

        # Desenha o corpo do semáforo
        pygame.draw.rect(tela, cor_corpo, (corpo_x, corpo_y, largura_corpo, altura_corpo), border_radius=5)

        # Desenha o poste do semáforo
        pygame.draw.rect(tela, cor_poste, (poste_x, poste_y, largura_poste, altura_poste))

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
            self.timer = self.timer_clock

    def zerar_rate_carros(self):
        self.rate_carros = 0
        self.carros_esperando = 0
        self.rua.carros_esperando = 0

    def set_timer(self, timer):
        self.timer_clock = timer
        
    def set_estado(self, estado):
        self.estado = estado