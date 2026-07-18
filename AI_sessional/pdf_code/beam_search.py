"""
Toy Beam Search example keeping top-k nodes by a simple score function.
This mirrors the PDF's illustrative example.
"""

def score(x: float) -> float:
    # same objective as others for consistency: maximize -x^2 + 4x
    return -(x ** 2) + 4 * x


def beam_search(start: float, k: int = 2, steps: int = 5):
    frontier = [start]
    for _ in range(steps):
        candidates = []
        for node in frontier:
            neighbors = [node + 1, node - 1]
            candidates.extend(neighbors)
        frontier = sorted(candidates, key=score, reverse=True)[:k]
    return frontier


if __name__ == "__main__":
    print("Beam search result:", beam_search(0))
