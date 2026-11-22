# Section 4.2 - Context-Free Grammars
# Problems: leftmost/rightmost derivation, parse tree, ambiguity, language.
# Run: python 4.2.py

def derivations():
    print("\n1) Leftmost derivation for id + id")
    for step in ["E", "E + T", "T + T", "id + T", "id + id"]:
        print(step)

    print("\n2) Rightmost derivation for id + id")
    for step in ["E", "E + T", "E + id", "T + id", "id + id"]:
        print(step)


def parse_tree():
    print("\n3) Parse tree for id + id")
    print("       E")
    print("     / | \\")
    print("    E  +  T")
    print("    |     |")
    print("    T     id")
    print("    |")
    print("   id")


def ambiguity():
    print("\n4) Ambiguous grammar: E -> E+E | E*E | id")
    print("Expression: id + id * id")
    print("\nTree 1: id + (id * id)")
    print("       +")
    print("      / \\")
    print("     id  *")
    print("        / \\")
    print("       id id")
    print("\nTree 2: (id + id) * id")
    print("        *")
    print("       / \\")
    print("      +  id")
    print("     / \\")
    print("    id id")
    print("\nTwo different parse trees for the same string => ambiguous grammar.")


def main():
    print("SECTION 4.2 - CONTEXT-FREE GRAMMAR")
    print("Example grammar: E -> E + T | T ; T -> id")
    derivations()
    parse_tree()
    ambiguity()
    print("\n5) Language example")
    print("For S -> aSb | ε, the language is { a^n b^n : n >= 0 }.")


if __name__ == "__main__":
    main()
