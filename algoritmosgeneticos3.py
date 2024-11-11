"""
Definição do Problema:
Encontrar a melhor combinação de compostos químicos que tenha a maior eficácia no tratamento da doença e o menor efeito colateral.

Parâmetros: Estruturas químicas dos compostos, eficácia, toxicidade, biodisponibilidade.
Representação dos Indivíduos:

Cada indivíduo na população será uma combinação única de compostos químicos. Podemos representar esses compostos como cadeias de caracteres ou sequências binárias.
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
pygame.display.set_caption("Drug Development Solver using Pygame")
clock = pygame.time.Clock()
FPS = 10

# Parâmetros do problema
NUM_COMPOUNDS = 15
POPULATION_SIZE = 50
MUTATION_PROBABILITY = 0.1
MAX_GENERATIONS = 100

# Gera eficácia, toxicidade e biodisponibilidade aleatórias para compostos
efficacy = np.random.rand(NUM_COMPOUNDS)
toxicity = np.random.rand(NUM_COMPOUNDS)
bioavailability = np.random.rand(NUM_COMPOUNDS)

# Funções GA
def generate_random_population(size):
    return [np.random.randint(0, 2, NUM_COMPOUNDS) for _ in range(size)]

def calculate_fitness(chromosome):
    total_efficacy = np.dot(chromosome, efficacy)
    total_toxicity = np.dot(chromosome, toxicity)
    total_bioavailability = np.dot(chromosome, bioavailability)
    fitness = total_efficacy / (total_toxicity + 1) * total_bioavailability
    return fitness

def sort_population(population):
    return sorted(population, key=calculate_fitness, reverse=True)

def mutate(chromosome, probability):
    if random.random() < probability:
        i = random.randint(0, NUM_COMPOUNDS - 1)
        chromosome[i] = 1 - chromosome[i]
    return chromosome

def crossover(parent1, parent2):
    size = len(parent1)
    cx_point = random.randint(1, size - 1)
    return (np.concatenate((parent1[:cx_point], parent2[cx_point:])),
            np.concatenate((parent2[:cx_point], parent1[cx_point:])))

def draw_population(screen, population, best_solution):
    screen.fill((255, 255, 255))
    font = pygame.font.SysFont('Arial', 16)

    for i in range(NUM_COMPOUNDS):
        color = (200, 200, 200) if best_solution[i] == 1 else (255, 255, 255)
        pygame.draw.rect(screen, color, (50, 50 + i * 30, 50, 20))
        text = font.render(f"E:{efficacy[i]:.2f} T:{toxicity[i]:.2f} B:{bioavailability[i]:.2f}", True, (0, 0, 0))
        screen.blit(text, (110, 50 + i * 30))

    for i, compound in enumerate(best_solution):
        if compound == 1:
            pygame.draw.line(screen, (0, 0, 255), (75, 60 + i * 30), (95, 60 + i * 30), 3)
    
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

    population = sort_population(population)
    best_solution = population[0]
    best_fitness = calculate_fitness(best_solution)
    best_fitness_values.append(best_fitness)

    print(f"Generation {generation}: Best fitness = {best_fitness}")

    draw_population(screen, population, best_solution)

    if generation >= MAX_GENERATIONS:
        break

    new_population = [best_solution]
    while len(new_population) < POPULATION_SIZE:
        parent1, parent2 = random.choices(population[:POPULATION_SIZE // 2], k=2)
        child1, child2 = crossover(parent1, parent2)
        new_population.extend([mutate(child1, MUTATION_PROBABILITY), mutate(child2, MUTATION_PROBABILITY)])
    
    population = new_population

    clock.tick(FPS)

pygame.quit()
sys.exit()
