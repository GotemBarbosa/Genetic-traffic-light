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
        fitness_penalizaçao += individuo_gen.penalizacao[i] * 2 # Peso maior para penalizações


    fitness_total = fitness_tempo_acumulado + fitness_penalizaçao

    individuo_gen.fitness_total = fitness_total
    individuo_gen.fitness_penalizacao = fitness_penalizaçao
    individuo_gen.fitness_tempo_acumulado = fitness_tempo_acumulado
    
    return fitness_total

# Função de seleção por torneio 
def selecao_torneio(populacao, k=3):
    torneio = random.sample(populacao, k)
    torneio.sort(key=lambda x: x.fitness_total)
    return torneio[0]


def crossover_um_ponto(pai1, pai2):
    ponto = random.randint(1, len(pai1.state) - 1)  # Escolhe um ponto de crossover

    filho1 = Individuo_evol(len(pai1.state))
    filho2 = Individuo_evol(len(pai1.state))

    # Cópia dos genes até o ponto de crossover
    filho1.state[:ponto] = pai1.state[:ponto]
    filho1.open_time[:ponto] = pai1.open_time[:ponto]
    filho2.state[:ponto] = pai2.state[:ponto]
    filho2.open_time[:ponto] = pai2.open_time[:ponto]

    # Troca dos genes a partir do ponto de crossover
    filho1.state[ponto:] = pai2.state[ponto:]
    filho1.open_time[ponto:] = pai2.open_time[ponto:]
    filho2.state[ponto:] = pai1.state[ponto:]
    filho2.open_time[ponto:] = pai1.open_time[ponto:]

    return filho1, filho2

def mutacao(individuo, mutation_rate=0.1, base_mutation_step=5, 
           min_open_time=1, max_open_time=120,  # Ajuste conforme necessário
           min_state=0, max_state=10):
    
    for i in range(len(individuo.tempoAcumulado)):
        # Mutação do open_time
        if random.random() < mutation_rate:
            delta_tempo = random.randint(-base_mutation_step, base_mutation_step)
            individuo.open_time[i] += delta_tempo
            # Garante que open_time esteja dentro dos limites
            individuo.open_time[i] = max(min(individuo.open_time[i], max_open_time), min_open_time)

        # Mutação do state
        if random.random() < mutation_rate:
            delta_state = random.randint(-1, 1)
            individuo.state[i] += delta_state
            # Garante que state só seja 0 ou 1
            individuo.state[i] = 1 if individuo.state[i] > 0 else 0
    return individuo

def elitismo(populacao, elite_size=1):
    populacao_sorted = sorted(populacao, key=lambda x: x.fitness_total)
    elites = populacao_sorted[:elite_size]
    return elites

def algoritmo_evolutivo(populacao_atual, elite_size=1, mutation_rate=0.1, 
                        k_torneio=3, crossover_rate=0.8):
    """
    Executa uma geração do algoritmo evolutivo.

    Parâmetros:
        populacao_atual (list): Lista de indivíduos da geração atual.
        elite_size (int): Número de indivíduos a serem mantidos como elites.
        mutation_rate (float): Taxa de mutação para os indivíduos.
        k_torneio (int): Número de indivíduos participantes do torneio.
        crossover_rate (float): Probabilidade de realizar crossover.

    Retorna:
        melhor (Individuo_evol): O melhor indivíduo da nova geração.
        nova_populacao (list): Lista de indivíduos da nova geração.
    """

    # Avaliar fitness de todos os indivíduos
    for individuo in populacao_atual:
        calcular_fitness(individuo)

    # Ordenar a população com base no fitness
    populacao_atual.sort(key=lambda x: x.fitness_total)
    melhor = populacao_atual[0]

    # Selecionar elites
    elites = elitismo(populacao_atual, elite_size)

    # Inicializar nova população com elites
    nova_populacao = elites.copy()

    # Gerar novos indivíduos até preencher a população
    while len(nova_populacao) < len(populacao_atual):
        # Seleção dos pais
        pai1 = selecao_torneio(populacao_atual, k=k_torneio)
        pai2 = selecao_torneio(populacao_atual, k=k_torneio)

        # Crossover
        if random.random() < crossover_rate:
            filho1, filho2 = crossover_um_ponto(pai1, pai2)
        else:
            # Sem crossover, os filhos são cópias dos pais
            filho1 = Individuo_evol(len(pai1.state))
            filho1.state = pai1.state.copy()
            filho1.open_time = pai1.open_time.copy()
            filho2 = Individuo_evol(len(pai2.state))
            filho2.state = pai2.state.copy()
            filho2.open_time = pai2.open_time.copy()

        # Mutação
        filho1 = mutacao(filho1, mutation_rate=mutation_rate)
        filho2 = mutacao(filho2, mutation_rate=mutation_rate)

        # Adicionar filhos à nova população
        nova_populacao.append(filho1)
        if len(nova_populacao) < len(populacao_atual):
            nova_populacao.append(filho2)

    # Garantir que a nova população tenha o tamanho correto
    nova_populacao = nova_populacao[:len(populacao_atual)]

    # Avaliar fitness da nova população
    for individuo in nova_populacao:
        calcular_fitness(individuo)

    # Atualizar o melhor indivíduo
    nova_populacao.sort(key=lambda x: x.fitness_total)
    melhor = nova_populacao[0]

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
        semaforo.timer = semaforo.timer_clock
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

        # pegar o melhor individuo para ser o atual
        individuo_atual = populacao[0]
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
    historico_fitness.append(melhor.fitness_total)  # Adicionar o fitness do melhor indivíduo ao histórico

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