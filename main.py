import pygame
from classes.individuo import Individuo, Individuo_evol
from config import *
from classes.estatisticas import DisplayEstatisticas, Grafico, GraficoFitness
from classes.AlgotimoGenetico import algoritmo_evolutivo, penalizacao
import matplotlib.pyplot as plt


'''
TODO:
- Melhorar a geraçao dos carros
- Fazer resultados melhores para mais de 2 ruas
- Fazer novas estatisticas inScreen considerando o algoritmo genetico
'''


def gerar_populacao_inicial(tamanho_populacao, num_semaforos):
    populacao = []
    for _ in range(tamanho_populacao):
        individuo = Individuo_evol(num_semaforos)
        populacao.append(individuo)
    return populacao

plt.ion()  # Ativa o modo interativo
fig, ax = plt.subplots()
ax.set_title("Fitness ao longo das gerações")
ax.set_xlabel("Gerações")
ax.set_ylabel("Fitness")
line, = ax.plot([], [], 'b-', label='Fitness')  # Linha para o gráfico
ax.legend()

# Iniciando o pygame
pygame.init()
pygame.font.init()

clock = pygame.time.Clock()
fps = FPS
speed_multiplier = 1  # Multiplicador de velocidade
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
graficoFitness = GraficoFitness(LARGURA_TELA, ALTURA_TELA)

# Configuração da janela
tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))  # Tamanho da janela
pygame.display.set_caption("Simulação Semáforos")  # Nome da janela

# Flags de controle
running = True  # Controle do loop principal do Pygame
geracao_atual = 0  # Contador de gerações

# Histórico de fitness para plotagem
historico_fitness = []
melhor = None
fit_melhor_anterior = 0


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
                if event.key == pygame.K_SPACE:
                    if speed_multiplier == 1:
                        speed_multiplier = 10
                    else:
                        speed_multiplier = 1
                if event.key == pygame.K_p:
                    if(fps == FPS):
                        fps = 1
                    else:
                        fps = FPS

        # Limpar a tela a cada iteração
        tela.fill(COR_VERDE)

        # Executar múltiplas iterações de simulação baseado no multiplicador de velocidade
        for _ in range(speed_multiplier):
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

            simulation_iteration +=1
            if simulation_iteration >= NUM_ITERACOES:
                generation_running = False  # Finalizar a geração atual
                break

        # pegar o melhor individuo para ser o atual
        individuo_atual = populacao[0]
        individuo_atual.desenhar(tela)

        # Atualizar e desenhar estatísticas e gráficos

        displayEstatisticas.desenhar_estatisticas(tela, geracao_atual, melhor, individuo_atual)

        # if(melhor.fitness_total != fit_melhor_anterior):
        #     graficoFitness.adicionar_dado(melhor.fitness_total)
        # graficoFitness.desenhar_grafico(tela)

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
        for rua in individuo.ruas:
            rua.carros = []


    # Rodar o algoritmo evolutivo
    fit_melhor_anterior = melhor.fitness_total
    melhor, populacao_evol = algoritmo_evolutivo(populacao_evol, geracao_atual=geracao_atual)
    historico_fitness.append(melhor.fitness_total)  # Adicionar o fitness do melhor indivíduo ao histórico

    # Atualizar o gráfico
    line.set_xdata(range(len(historico_fitness)))
    line.set_ydata(historico_fitness)
    ax.relim()  # Recalcula os limites do gráfico
    ax.autoscale_view()  # Ajusta a escala do gráfico automaticamente
    plt.draw()  # Atualiza o desenho do gráfico
    plt.pause(0.01)  # Dá uma pausa curta para evitar congelamento

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

plt.ioff()  # Desativa o modo interativo
plt.show()  # Mostra o gráfico final
print("Fim da simulação")
pygame.quit()