"""
Descrição do Problema: Temos um conjunto de tarefas e um conjunto de recursos. Cada recurso tem um custo associado à execução de uma tarefa. O objetivo é alocar recursos às tarefas de forma que o custo total seja minimizado.

Implementação de Algoritmo Genético
Criaremos um algoritmo genético com os seguintes componentes:

* Representação cromossômica: Cada cromossomo representa uma possível alocação de recursos para tarefas.
* Função Fitness: A função fitness calcula o custo total da alocação.
* Seleção: Selecione os pais com base em sua aptidão.
* Crossover: Combine dois pais para criar descendentes.
* Mutação: altera aleatoriamente a alocação na prole.
* Visualização: Use Pygame para visualizar a alocação e a evolução da população.
"""

import pygame
import random
import numpy as np
import itertools
import sys

# Inicialize o Pygame
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Resource Allocation Solver using Pygame")
clock = pygame.time.Clock()
FPS = 30

# Parâmetros do problema
NUM_TASKS = 10
NUM_RESOURCES = 5
POPULATION_SIZE = 50
MUTATION_PROBABILITY = 0.1
MAX_GENERATIONS = 100

# Gera custos aleatórios para recursos que executam tarefas
costs = np.random.randint(1, 100, (NUM_RESOURCES, NUM_TASKS))

# Funções GA
def generate_random_population(size):
    population = []
    for _ in range(size):
        chromosome = np.random.randint(0, NUM_RESOURCES, NUM_TASKS)
        population.append(chromosome)
    return population

def calculate_fitness(chromosome):
    total_cost = 0
    for task, resource in enumerate(chromosome):
        total_cost += costs[resource][task]
    return total_cost

def sort_population(population):
    return sorted(population, key=calculate_fitness)

def mutate(chromosome, probability):
    if random.random() < probability:
        i = random.randint(0, NUM_TASKS - 1)
        chromosome[i] = random.randint(0, NUM_RESOURCES - 1)
    return chromosome

def crossover(parent1, parent2):
    size = len(parent1)
    cx_point = random.randint(1, size - 1)
    child1 = np.concatenate((parent1[:cx_point], parent2[cx_point:]))
    child2 = np.concatenate((parent2[:cx_point], parent1[cx_point:]))
    return child1, child2

def draw_population(screen, population, best_solution):
    screen.fill((255, 255, 255))
    font = pygame.font.SysFont('Arial', 16)

    # Desenhar matriz de custos
    for i in range(NUM_RESOURCES):
        for j in range(NUM_TASKS):
            color = (200, 200, 200) if best_solution[j] == i else (255, 255, 255)
            pygame.draw.rect(screen, color, (50 + j * 60, 50 + i * 30, 50, 20))
            text = font.render(str(costs[i][j]), True, (0, 0, 0))
            screen.blit(text, (55 + j * 60, 50 + i * 30))

    # Desenhe a melhor solução
    for task, resource in enumerate(best_solution):
        pygame.draw.line(screen, (0, 0, 255), (75 + task * 60, 30), (75 + task * 60, 50 + resource * 30), 3)
    
    pygame.display.flip()

# Loop principal do algoritmo genético
population = generate_random_population(POPULATION_SIZE)
best_fitness_values = []

generation_counter = itertools.count(start=1)
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                running = False

    generation = next(generation_counter)

    # Calcule a fitness e classifique a população
    population = sort_population(population)
    best_solution = population[0]
    best_fitness = calculate_fitness(best_solution)
    best_fitness_values.append(best_fitness)

    print(f"Generation {generation}: Best fitness = {best_fitness}")

    # Desenhar população
    draw_population(screen, population, best_solution)

    #Verifique a condição de rescisão
    if generation >= MAX_GENERATIONS:
        break

    # Criar nova população
    new_population = [best_solution]  # Elitism: mantenha a melhor solução
    while len(new_population) < POPULATION_SIZE:
        parent1, parent2 = random.choices(population[:POPULATION_SIZE // 2], k=2)
        child1, child2 = crossover(parent1, parent2)
        new_population.extend([mutate(child1, MUTATION_PROBABILITY), mutate(child2, MUTATION_PROBABILITY)])
    
    population = new_population

    clock.tick(FPS)

pygame.quit()
sys.exit()

"""
# Explicação

* Definição do Problema: A tarefa é alocar recursos às tarefas de forma que o custo total seja minimizado.
* Representação cromossômica: Cada cromossomo representa uma alocação de recursos para tarefas. É representado como um array onde o índice é a tarefa e o valor é o recurso atribuído a essa tarefa.
* Função Fitness: A função fitness calcula o custo total da alocação somando os custos dos recursos atribuídos para cada tarefa.
* Seleção: Os pais são selecionados com base em sua aptidão. A metade superior da população é usada para seleção.
* Crossover: Dois pais são combinados para criar dois filhos usando um único ponto de cruzamento.
* Mutação: A alocação na prole é alterada aleatoriamente com uma pequena probabilidade.
* Visualização: Pygame é utilizado para desenhar a matriz de custos e a melhor solução encontrada até o momento.

Este código fornece um exemplo criativo e interessante do uso de algoritmos genéticos para um problema de alocação de recursos, com comentários detalhados e uma representação visual do progresso do algoritmo.
"""