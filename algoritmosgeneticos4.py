import random
import pygame

def draw_plot(screen, data, width, height):
    color = (3, 0, 2)
    line_width = 2

    if not data:
        return
    
    max_x = len(data) - 1
    max_y = max(data) if data else 1

    for i in range(len(data) - 1):
        x1 = int(i * width / max_x)
        y1 = int(height - (data[i] * height / max_y))
        x2 = int((i + 1) * width / max_x)
        y2 = int(height - (data[i + 1] * height / max_y))
        pygame.draw.line(screen, color, (x1, y1), (x2, y2), line_width)

def generate_initial_population(pop_size, num_genes):
    population = []
    for _ in range(pop_size):
        individual = [random.choice(['A', 'T', 'C', 'G']) for _ in range(num_genes)]
        population.append(individual)
    return population

def evaluate(individual):
    efficacy = sum([ord(gene) for gene in individual]) % 100
    toxicity = sum([ord(gene) for gene in individual]) % 50
    fitness = efficacy - toxicity + 10
    return fitness

def selection(population, fitness_scores, threshold):
    selected_individuals = [population[i] for i in range(len(population)) if fitness_scores[i] > threshold]
    if not selected_individuals:
        selected_individuals = random.sample(population, min(5, len(population)))
    return selected_individuals

def crossover(parent1, parent2):
    crossover_point = random.randint(1, len(parent1) - 1)
    child1 = parent1[:crossover_point] + parent2[crossover_point:]
    child2 = parent2[:crossover_point] + parent1[crossover_point:]
    return child1, child2

def mutate(individual, mutation_rate):
    for i in range(len(individual)):
        if random.random() < mutation_rate:
            individual[i] = random.choice(['A', 'T', 'C', 'G'])
    return individual

pygame.init()
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Evolução das Tentativas de Combinação')

population = generate_initial_population(50, 6)
print("population", population)

num_generations = 50
best_scores = []

running = True
for generation in range(num_generations):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            break
    
    if not running:
        break

    fitness_scores = [evaluate(ind) for ind in population]
    threshold = sum(fitness_scores) / len(fitness_scores)
    print("threshold", threshold)
    
    selected_individuals = selection(population, fitness_scores, threshold)
    print("selected_individuals", selected_individuals)

    new_population = []
    for i in range(0, len(selected_individuals), 2):
        parent1 = selected_individuals[i]
        parent2 = selected_individuals[i + 1] if i + 1 < len(selected_individuals) else selected_individuals[0]
        child1, child2 = crossover(parent1, parent2)
        new_population.extend([child1, child2])
    population = [mutate(ind, 0.01) for ind in new_population]

    best_scores.append(max(fitness_scores))
    print("best_scores", best_scores)

    screen.fill((0, 0, 0))  # Preencher a tela com a cor preta
    draw_plot(screen, best_scores, width, height)
    pygame.display.flip()
    pygame.time.wait(500)

best_solution = max(population, key=evaluate)
print("Melhor solução:", best_solution)
print("Score de fitness da melhor solução:", evaluate(best_solution))

pygame.quit()
