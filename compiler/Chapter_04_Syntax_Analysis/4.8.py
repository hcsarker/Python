# Section 4.8 - Using Ambiguous Grammars
# Demonstrates precedence/associativity and dangling-else shift preference.
# Run: python 4.8.py

def calculate():
    print("1) Operator precedence example")
    print("Use only a simple arithmetic expression with numbers and + - * /.")
    expression = input("Enter expression (example 10+20*5): ")
    try:
        # This is only a classroom demonstration; do not use eval on untrusted input.
        allowed = set("0123456789+-*/(). ")
        if not expression or any(ch not in allowed for ch in expression):
            raise ValueError("Only arithmetic characters are allowed")
        result = eval(expression, {"__builtins__": {}}, {})
        print("Result =", result)
    except Exception:
        print("Invalid expression")


def dangling_else():
    print("\n2) Dangling-else conflict")
    print("Possible actions: SHIFT or REDUCE")
    print("Resolution: prefer SHIFT.")
    print("Result: else is associated with the nearest unmatched if.")


if __name__ == "__main__":
    print("SECTION 4.8 - AMBIGUOUS GRAMMARS")
    calculate()
    dangling_else()
