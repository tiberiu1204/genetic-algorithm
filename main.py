import json

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


def terminate(t):
    pass


def init_population(pop_size):
    pass


def selection(population):
    pass


def crossover(population):
    pass


def mutation(population):
    pass


def simulate():
    params = parse_json(INPUT_JSON)

    t = 0
    population = init_population(params["population_size"])

    while not terminate(t):
        population = selection(population)
        population = crossover(population)
        population = mutation(population)
        t += 1


if __name__ == "__main__":
    simulate()
