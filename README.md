# Genetic algorithm to find the maximum of a 2 degree polynomial function on a given domain
This repository implements a basic genetic algorithm. It outputs useful data about its evolution, and has a graphical interface for easier visualisation.

# Installing
First, make sure you have python installed on your machine.

Download the repository locally:
```bash
git clone https://github.com/tiberiu1204/genetic-algorithm
cd genetic-algorithm
```

Create virtual enviroment and install dependencies (this step may differ on windwos machines):
```bash
python -m venv .venv
source ./.venv/bin/activate
pip install -r requirements.txt
```

# Usage
First, input your paramaters in params.json, or leave the default values.

The input paramaters are:
- population_size
- domain
- coefficients
- precision
- crossover_probability
- mutation_probability
- num_generations

Run main.py and inspect results:
```bash
python main.py && cat evolution.txt
```
Do not forget to source your enviroment as shown above.
