"""
# Otimização do layout do painel solar usando algoritmo genético

**Objetivo:** Otimizar a colocação de painéis solares em uma determinada área para maximizar a produção total de energia

Critérios de sucesso:

* Maximize a produção total de energia considerando os efeitos de sombreamento entre os painéis
* Minimize o espaço não utilizado dentro de uma determinada área
* Convergir com eficiência para a solução ideal ou quase ideal dentro de um * tempo de cálculo razoável
* Plano de implementação
* Definir o espaço do problema e as restrições
* Implementar o algoritmo genético
* Visualize os layouts iniciais e otimizados
* Compare os resultados com uma estratégia de posicionamento heurística simples
"""

import matplotlib.pyplot as plt
import random

# constantes do problema
area_width = 100 # largura da área do parque solar
area_height = 100 # altura da área do parque solar
panel_width = 5 # largura de um único painel solar
panel_height = 10 # altura de um único painel solar
num_panels = 20 # número de painéis solares a serem colocados

# função auxiliar para visualizar o layout
def visualize_layout(layout, title):
    fig, ax = plt.subplots()
    for (x, y) in layout:
        rect = plt.Rectangle((x, y), panel_width, panel_height, edgecolor='blue', facecolor='lightblue')
        ax.add_patch(rect)
    plt.xlim(0, area_width)
    plt.ylim(0, area_height)
    plt.title(title)
    plt.gca().set_aspect('equal', adjustable='box')
    plt.show()

# população inicial
def generate_initial_population(size):
    population = []
    for _ in range(size):
        layout = [(random.uniform(0, area_width - panel_width), random.uniform(0, area_height - panel_height)) for _ in range(num_panels)]
        population.append(layout)
    return population

# função fitness
def calculate_fitness(layout):
    total_energy = 0
    for i, (x1, y1) in enumerate(layout):
        shadowing_factor = 1
        for j, (x2, y2) in enumerate(layout):
            if i != j:
                if (x1 < x2 < x1 + panel_width) and (y1 < y2 < y1 + panel_height):
                    shadowing_factor -= 0.1
        total_energy += shadowing_factor
    return total_energy

# seleção
def selection(population):
    sorted_population = sorted(population, key=lambda layout: calculate_fitness(layout), reverse=True)
    return sorted_population[:len(population)//2]

# crossover
def crossover(parent1, parent2):
    split = random.randint(0, num_panels-1)
    child1 = parent1[:split] + parent2[split:]
    child2 = parent2[:split] + parent1[split:]
    return child1, child2

# mutação
def mutate(layout):
    if random.random() < 0.1:  # Mutation probability
        idx = random.randint(0, num_panels-1)
        layout[idx] = (random.uniform(0, area_width - panel_width), random.uniform(0, area_height - panel_height))
    return layout

# algoritmo genético
def genetic_algorithm(population_size, generations):
    population = generate_initial_population(population_size)
    for generation in range(generations):
        selected_population = selection(population)
        next_population = []
        while len(next_population) < population_size:
            parent1, parent2 = random.sample(selected_population, 2)
            child1, child2 = crossover(parent1, parent2)
            next_population.extend([mutate(child1), mutate(child2)])
        population = next_population
        best_layout = max(population, key=lambda layout: calculate_fitness(layout))
        print(f'Generation {generation+1}, Best Fitness: {calculate_fitness(best_layout)}')
    return best_layout

# parâmetros
population_size = 200
generations = 100

# execute o algoritmo genético
best_layout = genetic_algorithm(population_size, generations)

# visualizar o layout final
visualize_layout(best_layout, "Layout otimizado do painel solar")