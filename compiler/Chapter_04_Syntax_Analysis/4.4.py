# Section 4.4 - Top-Down Parsing
# Problems: FIRST/FOLLOW, LL(1) table, stack trace, recursive-descent parser.
# Example grammar:
# E  -> T E'
# E' -> + T E' | - T E' | ε
# T  -> F T'
# T' -> * F T' | / F T' | ε
# F  -> ( E ) | num
# Run: python 4.4.py

def first_follow_example():
    print("1) FIRST and FOLLOW for a small grammar")
    print("Grammar: S -> a A | b B ; A -> c ; B -> d")
    print("FIRST(S) = {a, b}")
    print("FIRST(A) = {c}")
    print("FIRST(B) = {d}")
    print("\nFor S -> A B, A -> a, B -> b:")
    print("FOLLOW(S) = {$}")
    print("FOLLOW(A) = {b}")
    print("FOLLOW(B) = {$}")


def ll1_table():
    print("\n2) LL(1) table example")
    table = {
        ("S", "a"): "S -> aA",
        ("S", "b"): "S -> bB",
        ("A", "c"): "A -> c",
        ("B", "d"): "B -> d",
    }
    for (nt, terminal), production in table.items():
        print(f"M[{nt}, {terminal}] = {production}")


def stack_trace():
    print("\n3) Predictive parsing stack trace for input ac$")
    stack = ["$", "S"]
    tokens = list("ac$")
    grammar = {"S": ["a", "A"], "A": ["c"]}
    i = 0

    print(f"{'STACK':<15} {'INPUT':<12} ACTION")
    while stack:
        before = "".join(stack)
        remaining = "".join(tokens[i:])
        top = stack[-1]
        lookahead = tokens[i]

        if top == "$" and lookahead == "$":
            print(f"{before:<15} {remaining:<12} accept")
            break
        if top == lookahead:
            stack.pop()
            i += 1
            action = f"match {lookahead}"
        elif top in grammar:
            stack.pop()
            rhs = grammar[top]
            for symbol in reversed(rhs):
                stack.append(symbol)
            action = f"{top} -> {''.join(rhs)}"
        else:
            print("Input rejected")
            return

        print(f"{before:<15} {remaining:<12} {action}")


# Recursive-descent parser for integer expressions with + - * / and parentheses.
s = ""
pos = 0

def factor():
    global pos
    if pos < len(s) and s[pos] == "(":
        pos += 1
        expression()
        if pos >= len(s) or s[pos] != ")":
            raise ValueError("Missing ')'")
        pos += 1
        return

    start = pos
    while pos < len(s) and s[pos].isdigit():
        pos += 1
    if start == pos:
        raise ValueError("Number expected")


def term():
    global pos
    factor()
    while pos < len(s) and s[pos] in "*/":
        pos += 1
        factor()


def expression():
    global pos
    term()
    while pos < len(s) and s[pos] in "+-":
        pos += 1
        term()


def recursive_descent():
    global s, pos
    print("\n4) Recursive-descent expression checker")
    s = input("Enter expression (example 12+(3*4)): ").replace(" ", "")
    pos = 0
    try:
        expression()
        if pos != len(s):
            raise ValueError("Unexpected symbol")
        print("Valid expression")
    except ValueError as error:
        print("Invalid expression:", error)


def main():
    print("SECTION 4.4 - TOP-DOWN PARSING")
    first_follow_example()
    ll1_table()
    stack_trace()
    recursive_descent()


if __name__ == "__main__":
    main()
