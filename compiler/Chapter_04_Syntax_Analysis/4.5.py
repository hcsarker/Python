# Section 4.5 - Bottom-Up Parsing and Shift-Reduce Concepts
# Problems: handle identification, shift/reduce trace, conflict examples.
# Run: python 4.5.py

def shift_reduce():
    print("Shift-reduce example")
    print("Grammar: S -> aA ; A -> b")
    text = input("Enter input (try ab): ").strip()

    stack = ""
    for symbol in text:
        stack += symbol
        print(f"Shift {symbol}: stack = {stack}")

        if stack.endswith("b"):
            stack = stack[:-1] + "A"
            print("Reduce A -> b:", stack)

    if stack == "aA":
        stack = "S"
        print("Reduce S -> aA:", stack)
        print("Accepted")
    else:
        print("Rejected")


def conflict_examples():
    print("\nConflict identification")
    print("Shift-reduce conflict:")
    print("  The parser can either shift the next input symbol or reduce.")
    print("Reduce-reduce conflict:")
    print("  The parser can reduce using two different productions.")
    print("\nHandle example:")
    print("For right-sentential form aA, using S -> aA, the handle is aA.")


if __name__ == "__main__":
    print("SECTION 4.5 - BOTTOM-UP PARSING")
    shift_reduce()
    conflict_examples()
