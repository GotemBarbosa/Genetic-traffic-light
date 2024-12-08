import random
from classes.individuo import Individuo_evol
from config import *

# NAO É UMA CLASSE AINDA


# Função de seleção por torneio 
def selecao_torneio(populacao, k=3):
    torneio = random.sample(populacao, k)
    torneio.sort(key=lambda x: x.fitness_total)
    return torneio[0]

# CROSSOVER
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

# MUTAÇÃO
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



def elitismo(populacao, elite_size=TAMANHO_POPULACAO//10):
    populacao_sorted = sorted(populacao, key=lambda x: x.fitness_total)
    elites = populacao_sorted[:elite_size]
    return elites


# Funcao para calcular o fitness de um individuo
def calcular_fitness(individuo_gen):
    fitness_tempo_acumulado = 0; # em relaçao ao tempo acumulado de espera
    fitness_penalizaçao = 0; # penalizaçao em que 2 semaforos estao abertos ao mesmo tempo
    for i in range(len(individuo_gen.open_time)):
        fitness_tempo_acumulado += individuo_gen.tempoAcumulado[i]
        fitness_penalizaçao += individuo_gen.penalizacao[i] * 4 # Peso maior para penalizações


    fitness_total = fitness_tempo_acumulado + fitness_penalizaçao

    individuo_gen.fitness_total = fitness_total
    individuo_gen.fitness_penalizacao = fitness_penalizaçao
    individuo_gen.fitness_tempo_acumulado = fitness_tempo_acumulado
    return fitness_total


def penalizacao(individuo, index):
    if index == len(individuo.semaforos) - 1:
        return 0
    penalizacao = 0
    if individuo.semaforos[index].estado == individuo.semaforos[index + 1].estado:
        penalizacao += 10
    return penalizacao


def algoritmo_evolutivo(populacao_atual, elite_size=1, mutation_rate=0.1, 
                        k_torneio=3, crossover_rate=0.8, geracao_atual=0):
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
    print(f"geraçao {geracao_atual} melhorFit: {melhor.fitness_total}")

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

    return melhor, nova_populacao
