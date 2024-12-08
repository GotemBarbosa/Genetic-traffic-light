import pygame
from classes.individuo import Individuo, Individuo_evol
from config import *
from classes.estatisticas import DisplayEstatisticas, Grafico
from classes.AlgotimoGenetico import algoritmo_evolutivo, penalizacao

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


# Iniciando o pygame
pygame.init()
pygame.font.init()

clock = pygame.time.Clock()
fps = FPS
populacao = []

for i in range(TAMANHO_POPULACAO):
    individuo = Individuo(id=i) # gerando um individuo
    populacao.append(individuo)

populacao_evol = gerar_populacao_inicial(TAMANHO_POPULACAO, len(populacao[0].semaforos))

# Gerando população
for i in range(TAMANHO_POPULACAO):
    for index_Sem, semaforo in enumerate(populacao[i].semaforos):
        semaforo.estado = populacao_evol[i].state[index_Sem]
        semaforo.set_timer(populacao_evol[i].open_time[index_Sem])
        semaforo.timer = semaforo.timer_clock

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
melhor = None

while running and geracao_atual < NUM_GERACOES:
    generation_running = True
    tela.fill(COR_VERDE)

    if(melhor == None):
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
                if event.key == pygame.K_s:
                    if fps == FPS:
                        fps = FPS / 3
                    else:
                        fps = FPS

        # Limpar a tela a cada iteração
        tela.fill(COR_VERDE)

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
    individuo_atual = melhor  # Supondo que a população está ordenada pelo fitness

    geracao_atual += 1  # Incrementar o contador de gerações

print("Fim da simulação")
pygame.quit()