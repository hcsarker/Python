# Section 4.7 - Canonical LR and LALR Parsers
# Demonstrates LR(1) items, lookahead, LALR core merging, and comparison.
# Run: python 4.7.py

def lr1_items():
    print("1) LR(1) item examples (production, dot, lookahead)")
    items = [
        ("S'", ["S"], 0, "$"),
        ("S", ["a", "A"], 0, "$"),
        ("A", ["b"], 0, "$"),
    ]
    for lhs, rhs, dot, lookahead in items:
        symbols = rhs[:]
        symbols.insert(dot, ".")
        print(f"[{lhs} -> {' '.join(symbols)}, {lookahead}]")


def lalr_merge():
    print("\n2) LALR merging example")
    state_1 = ("A -> a .", "lookahead b")
    state_2 = ("A -> a .", "lookahead c")
    print("State 1:", state_1)
    print("State 2:", state_2)
    print("Same LR(0) core: A -> a .")
    print("Merged state: [A -> a ., {b, c}]")


def comparison():
    print("\n3) Parser comparison")
    print("SLR  : LR(0) items; reductions use FOLLOW sets.")
    print("CLR  : LR(1) items; each item carries a lookahead.")
    print("LALR : merges CLR states that have the same LR(0) core.")
    print("State counts depend on the grammar.")


if __name__ == "__main__":
    print("SECTION 4.7 - CLR AND LALR")
    lr1_items()
    lalr_merge()
    comparison()
