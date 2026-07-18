"""
Hill Climbing to maximize f(x) = -x^2 + 4x on [0, 5]
"""
import random


def f(x: float) -> float:
    return -x**2 + 4 * x


def hill_climb(start: float | None = None, step_size: float = 0.1, iterations: int = 100) -> float:
    current = random.uniform(0, 5) if start is None else float(start)
    for _ in range(iterations):
        neighbors = [current + step_size, current - step_size]
        # clamp to domain (optional)
        neighbors = [min(5, max(0, n)) for n in neighbors]
        next_move = max(neighbors, key=f)
        if f(next_move) <= f(current):
            break
        current = next_move
    return current


if __name__ == "__main__":
    best = hill_climb()
    print("Best x:", best)
    print("Max f(x):", f(best))
