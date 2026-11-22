# Section 4.6 - Introduction to LR Parsing: SLR
# This is a small, explicit LR(0) item/closure/GOTO example.
# Grammar: S' -> S ; S -> C C ; C -> c C | d
# Run: python 4.6.py

GRAMMAR = {
    "S'": [["S"]],
    "S": [["C", "C"]],
    "C": [["c", "C"], ["d"]],
}
NONTERMINALS = set(GRAMMAR)
TERMINALS = {"c", "d", "$"}


def closure(items):
    result = set(items)
    changed = True
    while changed:
        changed = False
        for lhs, rhs, dot in list(result):
            if dot < len(rhs):
                symbol = rhs[dot]
                if symbol in NONTERMINALS:
                    for production in GRAMMAR[symbol]:
                        item = (symbol, tuple(production), 0)
                        if item not in result:
                            result.add(item)
                            changed = True
    return frozenset(result)


def goto(items, symbol):
    moved = set()
    for lhs, rhs, dot in items:
        if dot < len(rhs) and rhs[dot] == symbol:
            moved.add((lhs, rhs, dot + 1))
    return closure(moved) if moved else frozenset()


def show_item(item):
    lhs, rhs, dot = item
    parts = list(rhs)
    parts.insert(dot, ".")
    return lhs + " -> " + " ".join(parts)


def main():
    print("SECTION 4.6 - SLR / LR(0) ITEMS")
    start = closure({("S'", ("S",), 0)})
    print("\nI0 = closure({S' -> . S})")
    for item in sorted(start):
        print(" ", show_item(item))

    print("\nGOTO(I0, 'c'):")
    next_state = goto(start, "c")
    for item in sorted(next_state):
        print(" ", show_item(item))

    print("\nSLR concept:")
    print("1. Build LR(0) item sets using closure and GOTO.")
    print("2. Shift actions come from terminal transitions.")
    print("3. Reduce A -> alpha is placed on FOLLOW(A).")
    print("4. Accept when S' -> S . is reached with end marker $.")


if __name__ == "__main__":
    main()
