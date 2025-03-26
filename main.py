import json
import math
import numpy as np

INPUT_JSON = "params.json"


def parse_json(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

            # Extragem și validăm fiecare parametru
            population_size = data.get("population_size")
            domain = data.get("domain")
            coefficients = data.get("coefficients")
            precision = data.get("precision")
            crossover_prob = data.get("crossover_probability")
            mutation_prob = data.get("mutation_probability")
            num_generations = data.get("num_generations")

            parsed_data = {
                "population_size": population_size,
                "domain": domain,
                "coefficients": coefficients,
                "precision": precision,
                "crossover_probability": crossover_prob,
                "mutation_probability": mutation_prob,
                "num_generations": num_generations
            }

            return parsed_data
    except Exception as e:
        print(f"Eroare la citirea fișierului JSON: {e}")
        return None


def print_population(params, population, out_file, title):
    out_file.write(f"{title}:\n")
    values = population_to_values(params, population)
    fs = f(params, values)
    index = 0
    chromosome_len, precision = params["chromosome_len"], params["precision"]
    for individual in population:
        out_file.write(f"\t{index + 1:{math.ceil(math.log10(chromosome_len))}}: {individual:0{chromosome_len}b} x={
            values[index]:.0{precision}f} f={fs[index]}\n")
        index += 1


def f(params, x):
    a, b, c = params["coefficients"]
    return a * np.pow(x, 2) + b * x + c


def population_to_values(params, population):
    a, b, chromosome_len = params["domain"][0], params["domain"][1], params["chromosome_len"]
    return ((b - a) / ((1 << chromosome_len) - 1)) * population + a


def terminate(params, t):
    # return params["num_generations"] == t
    return t == 1


def init_population(params):
    chromosome_len, population_size = params["chromosome_len"], params["population_size"]
    population = np.random.randint(low=0, high=(
        1 << chromosome_len), size=population_size)
    return population


def selection(params, population, out_file=None):
    def print_probabilities():
        out_file.write("\nProbabilitati selectie\n")
        index = 0
        for prob in probabilities:
            out_file.write(f"cromozom {index + 1} probabilitate {prob}\n")

    def print_intervals():
        out_file.write("Intervale probabilitati selectie\n")
        out_file.write(f"{intervals}\n")

    def print_selections():
        index = 0
        for selection in selections:
            out_file.write(f"u={u[index]} selectam cromozomul {
                           selection + 1}\n")
            index += 1

    fitness = f(params, population_to_values(params, population))
    elitist_index = np.argmax(fitness)
    elitist = population[elitist_index]
    total_fitness = np.sum(fitness)
    probabilities = fitness / total_fitness
    intervals = np.cumsum(np.insert(probabilities, 0, 0))
    u = np.random.uniform(size=len(population)-1)
    selections = np.searchsorted(intervals, u) - 1

    if out_file:
        print_probabilities()
        print_intervals()
        print_selections()

    return population[selections], elitist


def crossover(params, population, out_file=None):
    def print_rolls():
        index = 0
        for individual in old_population:
            out_file.write(
                f"{index + 1}: {individual:0{chromosome_len}b} u={u[index]}")
            if u[index] < probability:
                out_file.write(f"<{probability} participa\n")
            else:
                out_file.write("\n")
            index += 1

    def print_crossovers():
        index = 0
        out_file.write("\n")
        while index < len(points):
            chr1_index = selected_indexes[index * 2]
            chr2_index = selected_indexes[index * 2 + 1]
            chr1 = old_population[chr1_index]
            chr2 = old_population[chr2_index]

            point = points[index]
            out_file.write(f"Recombinare dintre cromozomul {
                           chr1_index + 1} cu cromozomul {chr2_index + 1}:\n")
            out_file.write(f"{chr1:0{chromosome_len}b} {
                           chr2:0{chromosome_len}b} punct {point}\n")
            out_file.write(f"Rezultat {population[chr1_index]:0{chromosome_len}b} {
                           population[chr2_index]:0{chromosome_len}b}\n")
            index += 1

    old_population = np.copy(population)

    probability, chromosome_len = params["crossover_probability"], params["chromosome_len"]
    u = np.random.uniform(size=len(population))
    mask = u < probability
    selected = population[mask]
    temp = None
    if len(selected) % 2 == 1:
        temp = selected[-1]
        selected = selected[:-1]
    selected_indexes = np.where(mask)[0]
    sample1 = selected[::2]
    sample2 = selected[1::2]
    points = np.random.randint(low=0, high=chromosome_len, size=len(sample1))

    tail_lengths = chromosome_len - points
    heads1 = sample1 >> tail_lengths
    heads2 = sample2 >> tail_lengths
    tails1 = sample1 & ((1 << tail_lengths) - 1)
    tails2 = sample2 & ((1 << tail_lengths) - 1)

    sample1 = (heads2 << tail_lengths) + tails1
    sample2 = (heads1 << tail_lengths) + tails2

    selected[::2] = sample1
    selected[1::2] = sample2
    if temp:
        selected = np.append(selected, temp)
    population[mask] = selected

    if out_file:
        out_file.write(f"Probabilitate de incrucisare {probability}\n")
        print_rolls()
        out_file.write("\n")
        print_crossovers()
        print_population(params, population, out_file, "Dupa recombinare")


def mutation(params, population, out_file=None):
    pass


def simulate():
    OUTPUT_FILE = "./evolution.txt"
    out_file = open(OUTPUT_FILE, "w")

    params = parse_json(INPUT_JSON)
    a, b, precision = params["domain"][0], params["domain"][1], params["precision"]
    params["chromosome_len"] = math.ceil(
        math.log2((b - a) * math.pow(10, precision)))

    t = 0
    population = init_population(params)
    print_population(params, population, out_file, "Populatia initiala")

    while not terminate(params, t):
        out_file_first_iteration = None if t else out_file
        population, elitist = selection(
            params, population, out_file_first_iteration)
        population = crossover(params, population, out_file_first_iteration)
        population = mutation(params, population, out_file_first_iteration)
        population = np.append(population, elitist)
        t += 1

    out_file.close()


if __name__ == "__main__":
    simulate()
