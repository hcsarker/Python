"""
Simple Genetic Algorithm maximizing fitness(x) = x^2 with integer x in [0, 31].
Follows the structure shown in the PDF (selection, crossover, mutation).
"""
from __future__ import annotations
import random


def fitness(x: int) -> int:
    return x * x


def genetic_algorithm(pop_size: int = 6, generations: int = 10, domain=(0, 31), elite: int = 3, mutation_rate: float = 0.1) -> int:
    lo, hi = domain
    population = [random.randint(lo, hi) for _ in range(pop_size)]

    for _ in range(generations):
        population.sort(key=fitness, reverse=True)
        population = population[:elite]  # keep elites
        children: list[int] = []
        while len(children) < pop_size - elite:
            p1, p2 = random.sample(population, 2)
            child = (p1 + p2) // 2  # very simple 'crossover'
            if random.random() < mutation_rate:
                child += random.choice([-1, 1])
            child = min(hi, max(lo, child))
            children.append(child)
        population += children

    best = max(population, key=fitness)
    return best


if __name__ == "__main__":
    best = genetic_algorithm()
    print("Best solution:", best)
    print("Fitness:", fitness(best))
