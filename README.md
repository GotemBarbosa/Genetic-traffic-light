# Algoritmo evolutivo utilizado para otimizar a temporização de semáforos. 

Trabalho desenvolvido para ser apresentado na disciplina SSC-0713 Sistemas Evolutivos Aplicados a Robotica.

#### Integrantes do Grupo

* Felipe Carneiro Machado
* Gabriel Barbosa dos Santos
* Renan Parpinelli Scarpin
* Vinicius Neves Gustierrez

#### Resumo

Foi projetado um algoritmo evolutivo para determinacao do tempo ideal de abertura de semaforos em ruas, bem como seu estado inicial, de modo a minimizar o tempo de espera dos carros e evitar semaforos abertos simultaneamente.

#### Individuo

O individuo foi modelado como um vetor de pares de inteiros, cada posicao representando um semaforo do mapa, que pode ter um numero arbitrario de ruas, com seu tempo de troca de estado, e seu estado inicial.

#### Fitness

O fitness eh calculado em funcao do tempo acumulado de espera dos carros do semaforo, com penalizacoes para semaforos do mesmo cruzamento abertos simultaneamente e para semaforos com tempos de troca muito curtos, sendo uma funcao a ser minimizada

#### Selecao

O algoritmo utiliza selecao de torneio e elitismo, mantendo sempre o melhor individuo da ultima geracao

#### Variabilidade

Utilizamos cross-over uniforme, escolhendo um ponto do genoma que sera trocado entre dois individuos, alem de mutacao, que soma um delta aleatorio ao tempo de troca, ou altera o estado inicial.

#### Simulacao

Utilizamos pygame para ilustrar a simulacao