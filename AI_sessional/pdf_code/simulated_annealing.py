"""
Simulated Annealing to maximize f(x) = -x^2 + 4x on [0,5]
"""
import math
import random


def f(x: float) -> float:
    return -x**2 + 4 * x


def simulated_annealing(start: float | None = None, T: float = 10.0, alpha: float = 0.9, iterations: int = 100) -> float:
    current = random.uniform(0, 5) if start is None else float(start)
    for _ in range(iterations):
        new = current + random.uniform(-0.5, 0.5)
        new = min(5, max(0, new))  # keep in domain
        delta = f(new) - f(current)
        if delta > 0 or random.random() < math.exp(delta / T):
            current = new
        T *= alpha
        if T < 1e-6:
            break
    return current


if __name__ == "__main__":
    best = simulated_annealing()
    print("Best x:", best)
    print("Max f(x):", f(best))
