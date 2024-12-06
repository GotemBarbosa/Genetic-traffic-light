import pygame
from classes.individuo import Individuo
from config import *
from classes.estatisticas import DisplayEstatisticas, Grafico

'''
TODO:
- Mudar para ter a acumulada do tempo de espera nas ruas
- Fazer com que cada iteraçao da futura geraçao de treinamento seja um loop de pygame
- Fazer as caracteristicas do individuo em si que serao usadas no evolutivo (informacoes do gene)
- Fazer com que essas caracteristicas alterem essa futura funcao de treinamento
- Fazer com que essa funcao de treinamento tenha um tempo definido ( OU INTERAÇOES DO WHILE RUNNING, QUE EU ACHO MELHOR )
- Desenvolver a funçao de crossover
- Desenvolver a funçao de mutaçao
- Desenvolver a funcao de fitness
- Fazer novas estatisticas inScreen considerando o algoritmo genetico
'''



# Iniciando o pygame
pygame.init()
pygame.font.init()


clock = pygame.time.Clock()

tamanho_populacao = 10
populacao = []

#gerando populacao
for i in range(tamanho_populacao):
    individuo = Individuo(id=i)
    populacao.append(individuo)

#loop principal da simulacao usando um individuo da populacao (pode ser o melhor futuramente)
individuo_atual = populacao[1]

displayEstatisticas = DisplayEstatisticas(individuo_atual.ruas, LARGURA_TELA)
grafico = Grafico(individuo_atual.ruas, LARGURA_TELA, ALTURA_TELA)

# Configuraçao da janela
tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA)) # Tamanho da janela
pygame.display.set_caption("Simulaçao Semáforos") # Nome da janela

running = True


# Loop principal 
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    tela.fill(COR_VERDE)

    count = 0
    for val, individuo in enumerate(populacao):
        #gerar carros no individuo atual
        individuo.gerar_carros()
        #atualizar seus dados
        individuo.atualizar()
        # print(f"individuo {val} { individuo.ruas[0].semaforos[0].carros_esperando}")
        if(count == 0):
            print(f"individuo atual { individuo_atual.ruas[0].semaforos[0].carros_esperando}")
            
        count += 1

    #Renderizando apenas o individuo atual

    # Desenhar o individuo atual (ruas, interconexoes, semaforos e carros)
    individuo_atual.desenhar(tela)

    displayEstatisticas.desenhar_estatisticas(tela)
    grafico.adicionar_dados()
    grafico.desenhar_grafico(tela)

    pygame.display.update()
    clock.tick(FPS)

pygame.quit()
    
