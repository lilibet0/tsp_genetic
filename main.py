from functools import partial
import random
from util import cost


def check_argument_validity(initial_population, distances, generations):
    if initial_population is None:
        return False
    if distances is None:
        return False
    if generations is None:
        return False
    if generations <= 0:
        return False
    else:
        return True
    

# Select two parents with tournament selection
def parent_selection(population, distances):
    # Tournament selection
    # Select k individuals from the population
    # Choose k to be 5 to allow for genetic diversity
    tournament_population = random.choices(population, k=5)

    # Compute their costs, sorted low to high cost
    tournament_population = sorted(tournament_population, 
                                   key=partial(cost, distances=distances), reverse=False)

    # Return the two best parents from random population
    return tournament_population[0], tournament_population[1]


# Mixing paths from two parents
# Takes two parents and returns two children
def crossover(parent_one, parent_two):
    child_one = []
    child_two = []

    # Randomly select an index and length
    rand_index = random.randint(0, len(parent_one) - 1)
    rand_length = random.randint(0, len(parent_one) - 1)

    # Put cities in positions a,…,a+al-1 in child’s path
    # child_one: parent_one, parent_two
    # child_two: parent_two, parent_one
    
    for i in range(rand_index, (rand_index + rand_length - 1)):
        # Check for wraparound
        if i >= len(parent_one):
            child_one += parent_one[i - len(parent_one)]
            child_two += parent_two[i - len(parent_one)]
        else:
            child_one += parent_one[i]
            child_two += parent_two[i]

    # Finish filling child_one
    current_index = len(parent_one) - 1
    while (len(child_one) != len(parent_one)):
        last_city = parent_two[current_index]

        if last_city not in child_one:
            child_one += parent_two[current_index]
        
        # Decrement current_index
        current_index -= 1

    # Finish filling child_two
    current_index = len(parent_one) - 1
    while (len(child_two) != len(parent_one)):
        last_city = parent_one[current_index]

        if last_city not in child_two:
            child_two += parent_one[current_index]
        
        # Decrement current_index
        current_index -= 1

    return child_one, child_two


# One generation: parent selection, crossover, selection of the fittest population  
def genetic_algorithm(population, distances):
    new_population = []

    # Create next generation
    for i in range(len(population) // 2):
        # Create pairs of (non-optimal) solutions in the population, the “parents”
        parent_one, parent_two = parent_selection(population, distances)

        # Crossover
        child_one, child_two = crossover(parent_one, parent_two)

        new_population.append(child_one)
        new_population.append(child_two)

    # Return new_population sorted from lowest to highest cost
    return sorted(new_population, key=partial(cost, distances=distances), reverse=False)


# Return the best path (a tuple of cities) from the final generation.
def ga_tsp(initial_population, distances, generations):
    if check_argument_validity(initial_population, distances, generations) is False:
        return None
    
    # Perform genetic algorithm a generations number of times
    next_generation = genetic_algorithm(initial_population, distances)
    for i in range(generations):
        next_generation = genetic_algorithm(next_generation, distances)

    return next_generation[0]
