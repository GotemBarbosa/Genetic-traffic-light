import pygame
from classes.individuo import Individuo, Individuo_evol
from config import *
from classes.estatisticas import DisplayEstatisticas, Grafico
import random
import matplotlib as plt
'''
TODO:
- Mudar para ter a acumulada do tempo de espera nas ruas (FEITO)
- Fazer com que cada iteraçao da futura geraçao de treinamento seja um loop de pygame
- Fazer as caracteristicas do individuo em si que serao usadas no evolutivo (informacoes do gene)
- Fazer com que essas caracteristicas alterem essa futura funcao de treinamento
- Fazer com que essa funcao de treinamento tenha um tempo definido ( OU INTERAÇOES DO WHILE RUNNING, QUE EU ACHO MELHOR )
- Desenvolver a funçao de crossover
- Desenvolver a funçao de mutaçao
- Desenvolver a funcao de fitness
- Fazer novas estatisticas inScreen considerando o algoritmo genetico
'''


def gerar_populacao_inicial(tamanho_populacao, num_semaforos):
    populacao = []
    for _ in range(tamanho_populacao):
        individuo = Individuo_evol(num_semaforos)
        populacao.append(individuo)
    return populacao

def calcular_fitness(individuo_gen):
    fitness_tempo_acumulado = 0; # em relaçao ao tempo acumulado de espera
    fitness_penalizaçao = 0; # penalizaçao em que 2 semaforos estao abertos ao mesmo tempo

    for i in range(len(individuo_gen.tempoAcumulado)):
        fitness_tempo_acumulado += individuo_gen.tempoAcumulado[i]
        fitness_penalizaçao += individuo_gen.penalizacao[i] * 2

    fitness_total = fitness_tempo_acumulado + fitness_penalizaçao
    
    return fitness_total, fitness_penalizaçao, fitness_tempo_acumulado

def mutacao(individuo, fitness_tempo_acumulado, fitness_penalizaçao):
    for i in range(len(individuo.tempoAcumulado)):
        if(fitness_tempo_acumulado == 0):
            fitness_tempo_acumulado = 1
        taxa_significancia_tempo = individuo.tempoAcumulado[i] / fitness_tempo_acumulado
        if random.randint(0,1) < taxa_significancia_tempo:
            individuo.open_time[i] += random.randint(int(-20*taxa_significancia_tempo), int(20*taxa_significancia_tempo))

        if(fitness_penalizaçao == 0):
            fitness_penalizaçao = 1
        taxa_significancia_penalizacao = individuo.penalizacao[i] / fitness_penalizaçao
        if random.randint(0,1) < taxa_significancia_penalizacao:
            individuo.state[i] += random.randint(int(-20*taxa_significancia_penalizacao), int(20*taxa_significancia_penalizacao))

    return individuo

# def elitismo(populacao, elite_size=1):
#     populacao.sort(key=lambda x: calcular_fitness(x))
#     return populacao[:elite_size]

def algoritmo_evolutivo(populacao_atual):

    # Avaliar fitness de todos os indivíduos
    fitness_pop_tempoAcumulado = []
    fitness_pop_penalizacao = []
    for individuo in populacao_atual:
        fitness_ind, penalizacao, tempo_acumulado = calcular_fitness(individuo)
        fitness_pop_penalizacao.append(penalizacao)
        fitness_pop_tempoAcumulado.append(tempo_acumulado)
        individuo.fitness = fitness_ind

    #ordena a populaçao atual pelo fitness
    populacao_atual.sort(key=lambda x: calcular_fitness(x))
    melhor = populacao_atual[0]
    
    nova_populacao = []
    nova_populacao.append(melhor)

    for i in range(len(populacao_atual) - 1):
        filho = mutacao(populacao_atual[i], fitness_pop_penalizacao[i], fitness_pop_tempoAcumulado[i])
        nova_populacao.append(filho)
    
    return melhor, nova_populacao

def plotar_historico_fitness(historico):
    plt.plot(historico)
    plt.xlabel('Geração')
    plt.ylabel('Fitness (Tempo Médio de Parada)')
    plt.title('Evolução do Algoritmo Evolutivo')
    plt.show()

def penalizacao(individuo, index):
    if index == len(individuo.semaforos) - 1:
        return 0
    penalizacao = 0
    if individuo.semaforos[index].estado == individuo.semaforos[index + 1].estado:
        penalizacao += 10
    return penalizacao

# Iniciando o pygame
pygame.init()
pygame.font.init()

clock = pygame.time.Clock()
fps = FPS
populacao = []

populacao_evol = gerar_populacao_inicial(TAMANHO_POPULACAO, NUM_SEMAFOROS)

# Gerando população
for i in range(TAMANHO_POPULACAO):
    individuo = Individuo(id=i)  # Gerando um individuo
    for index_Sem, semaforo in enumerate(individuo.semaforos):
        semaforo.estado = populacao_evol[i].state[index_Sem]
        semaforo.set_timer(populacao_evol[i].open_time[index_Sem])
    populacao.append(individuo)

# Inicialização das estatísticas e gráficos
individuo_atual = populacao[0]  # Pode começar com o melhor ou outro indivíduo
displayEstatisticas = DisplayEstatisticas(individuo_atual.ruas, LARGURA_TELA)
grafico = Grafico(individuo_atual.ruas, LARGURA_TELA, ALTURA_TELA)

# Configuração da janela
tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))  # Tamanho da janela
pygame.display.set_caption("Simulação Semáforos")  # Nome da janela

# Flags de controle
running = True  # Controle do loop principal do Pygame
geracao_atual = 0  # Contador de gerações

# Histórico de fitness para plotagem
historico_fitness = []

while running and geracao_atual < NUM_GERACOES:
    generation_running = True
    tela.fill(COR_VERDE)
    
    melhor = populacao_evol[0]
    tela.fill(COR_VERDE)
    
    simulation_iteration = 0  # Iterações da simulação
    
    while generation_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                generation_running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_f:
                    if fps == FPS:
                        fps = FPS * FPS_MULTIPLIER
                    else:
                        fps = FPS

        # Limpar a tela a cada iteração
        tela.fill(COR_VERDE)

        count = 0
        for val, individuo in enumerate(populacao):
            individuo_evol = populacao_evol[val]
            # Gerar carros no indivíduo atual
            individuo.gerar_carros()
            # Atualizar seus dados
            individuo.atualizar()
            
            # Atualizar as métricas dos indivíduos (tempo acumulado e penalização por semáforo do indivíduo):
            for i in range(len(individuo.semaforos)):
                individuo_evol.tempoAcumulado[i] = individuo.semaforos[i].rate_carros

                if i % 2 == 0:  # Só analisar em pares
                    valor = penalizacao(individuo, i)
                    if valor > 0:
                        individuo_evol.penalizacao[i] = valor
                        individuo_evol.penalizacao[i + 1] = valor

            if count == 0:
                print(f"Indivíduo atual {individuo_atual.ruas[0].semaforos[0].carros_esperando}")
            count += 1

        # Renderizando apenas o indivíduo atual
        individuo_atual.desenhar(tela)

        # Atualizar e desenhar estatísticas e gráficos
        displayEstatisticas.desenhar_estatisticas(tela, geracao_atual, melhor)
        # grafico.adicionar_dados(melhor.fitness)  # Passar o fitness do melhor indivíduo
        # grafico.desenhar_grafico(tela)

        pygame.display.update()
        clock.tick(fps)

        simulation_iteration += 1
        if simulation_iteration >= NUM_ITERACOES:
            generation_running = False  # Finalizar a geração atual

    # Resetar métricas dos semáforos após a geração
    for individuo in populacao:
        for semaforo in individuo.semaforos:
            semaforo.zerar_rate_carros()
        for rua in individuo.ruas:
            rua.carros_esperando = 0
        #deletando os carros das ruas
        individuo.carros = []


    # Rodar o algoritmo evolutivo
    melhor, populacao_evol = algoritmo_evolutivo(populacao_evol)
    historico_fitness.append(melhor.fitness)  # Adicionar o fitness do melhor indivíduo ao histórico

    # Aplicar na população da simulação os valores da população evoluída
    for i in range(TAMANHO_POPULACAO):
        individuo = populacao[i]
        individuo_evol = populacao_evol[i]
        for index_Sem, semaforo in enumerate(individuo.semaforos):
            semaforo.estado = individuo_evol.state[index_Sem]
            semaforo.set_timer(individuo_evol.open_time[index_Sem])

    # Atualizar o indivíduo atual (pode optar por sempre selecionar o melhor)
    individuo_atual = populacao[0]  # Supondo que a população está ordenada pelo fitness

    geracao_atual += 1  # Incrementar o contador de gerações

# Após todas as gerações, plotar o histórico de fitness
plotar_historico_fitness(historico_fitness)

print("Fim da simulação")
pygame.quit()