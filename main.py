import json
import random
import copy
import vis


foods = None
dri = None
ingredients = 5  # number of foods in a meal\solution
mutation_chance = 0.1
iterations = 100
population_size = 200

plot_data = {}


def ga(pop_size, max_iters, seed):
    random.seed(seed)
    plot_data[str(seed)] = []

    population = initial_pop(pop_size)

    for i, chromossome in enumerate(population):
        population[i] = (chromossome, fitness(chromossome))

    best = max(population, key=lambda x: x[1])

    i = 0
    while i < max_iters and best[1] < 1:
        plot_data[str(seed)].append(best[1])

        new_population = []

        for j in range(pop_size):
            x, y = select(population)
            offspring = reproduce(x, y)

            if random.random() < mutation_chance:
                offspring = mutate(offspring)

            new_population.append((offspring, fitness(offspring)))

        # elitism
        if best[1] > max(new_population, key=lambda x: x[1])[1]:
            new_population.remove(min(new_population, key=lambda x: x[1]))
            new_population.append(best)

        population = copy.deepcopy(new_population)

        best = max(population, key=lambda x: x[1])  # optimization
        i += 1

    return best

def initial_pop(n):
    global foods

    population = []

    for i in range(n):
        chromossome = []

        # add foods to chromossome
        for category in random.choices(list(foods), k=ingredients):
            food = random.choice(list(foods[category]))
            chromossome.append({food: foods[category][food]})

        population.append(chromossome)

    return population

def fitness(chromossome, debug=False):
    score = {}
    fitness = 0

    for nutrient in dri:
        score[nutrient] = 0

    for nutrient in dri:
        for i, food in enumerate(chromossome):
            for food_name, food_nutrients in food.items():
                for food_nutrient in food_nutrients:
                    if nutrient.casefold() in food_nutrient.casefold() and "ergocalciferol" not in food_nutrient and "cholecalciferol" not in food_nutrient:
                        if nutrient == "Water" and food_nutrient != nutrient:
                            continue  # next iter

                        score[nutrient] += chromossome[i][food_name][food_nutrient] / dri[nutrient]

    for nutrient in score:
        if debug:
            print(f"{nutrient}: {score[nutrient]}")

            fitness += min(1, score[nutrient])
        else:
            fitness += min(1, score[nutrient] ** 0.5)


    if debug:
        vis.plot_nutrients(score)

    fitness /= len(score)

    return fitness

def select(population):
    # roulette wheel selection
    selected = random.choices(population, weights=[x[1] for x in population], k=2)

    return selected[0], selected[1]

def reproduce(parent1, parent2):
    crossover_point = random.randint(1, len(parent1[0]) - 1)

    offspring = parent1[0][:crossover_point] + parent2[0][crossover_point:]

    return offspring

def mutate(chromossome):
    # remove random food
    mutated = copy.deepcopy(chromossome)
    mutated.remove(random.choice(mutated))

    # add random food
    category = random.choice(list(foods))
    food = random.choice(list(foods[category]))
    mutated.append({food: foods[category][food]})

    if fitness(mutated) > fitness(chromossome):
        return mutated
    else:
        return chromossome


with open("foods.json") as fp:
    foods = json.load(fp)
with open("dri.json") as fp:
    dri = json.load(fp)

results = []
for i in range(10):
    results.append(ga(population_size, iterations, seed=i)[1])

vis.plot(plot_data)

print(f"Average best fitness: {sum(results) / len(results)}")

# print(f"\n{'-'*20} Nutrients {'-'*20}")
# real_ratio = fitness(result[0], debug=True)
#
# print(f"\n{'-'*20} Foods {'-'*20}")
# for food in result[0]:
#     for name, nutrients in food.items():
#         print(name)
#
# print(f"\nFitness: {result[1]}")
# print(f"Real ratio: {real_ratio}")
