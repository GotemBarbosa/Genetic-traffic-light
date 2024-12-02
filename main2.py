import pygame
import random
from config import *
from classes.rua import Rua
from classes.carro import Carro
from classes.interconexoes import interConexao
from classes.interconexoes import interconexoes_area
from classes.estatisticas import displayEstatisticas
from classes.estatisticas import Grafico
from classes.semaforo import Semaforo

# Iniciando o pygame
pygame.init()

# Configuraçao da janela
tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA)) # Tamanho da janela
pygame.display.set_caption("Simulaçao Semáforos") # Nome da janela

# Loop principal
running = True

# gerando duas ruas (classe)
rua1 = Rua(0, 200, LARGURA_TELA, 50, 'horizontal')
rua2 = Rua(200, 0, 50, ALTURA_TELA, 'vertical')
rua3 = Rua(400, 0, 50, ALTURA_TELA, 'vertical')
rua4 = Rua(0, 400, LARGURA_TELA, 50, 'horizontal')

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
grafico = Grafico([rua1, rua2], LARGURA_TELA, ALTURA_TELA)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Preenche tela com preto
    tela.fill(COR_VERDE)

    # Desenha as ruas
    for rua in ruas:
        rua.desenhar_rua(tela, interconexoes_area)

    #gerando carros aleatoriamente
    if random.random() < CAR_GENERATION_PROBABILITY:
        numRuas = len(ruas)
        ruaOrigem = ruas[random.randint(0, numRuas-1)]
        carros.append(Carro(ruaOrigem))

    #desenhando semaforos das interconexoes
    for intercon in interconexoes:
        intercon.semaforo.atualizar_semaforo()
        intercon.semaforo.desenhar_semaforo(tela)


    #desenhando carros
    for carro in carros:
        carro.desenhar_carro(tela)
        carro.mover_carro()
        if carro.orientacao == 'horizontal':
            if carro.x > LARGURA_TELA:
                carro.remover_carro()
        if carro.orientacao == 'vertical':
            if carro.y > ALTURA_TELA:
                carro.remover_carro()


    #desenhando estatisticas
    displayEstatisticas.desenhar_estatisticas(tela)

    # grafico
    grafico.adicionar_dados()
    grafico.desenhar_grafico(tela)

    # Atualiza a tela
    pygame.display.update()

# Finaliza o pygame
pygame.quit()