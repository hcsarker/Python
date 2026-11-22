# Section 4.3 - Writing a Grammar
# Problems: remove immediate left recursion, show non-immediate example,
# left factoring, and resolve dangling-else grammar.
# Run: python 4.3.py

def immediate_left_recursion():
    print("1) Immediate left recursion")
    print("Before: A -> A a | b")
    print("After : A -> b A'")
    print("        A' -> a A' | ε")


def non_immediate_left_recursion():
    print("\n2) Non-immediate left recursion")
    print("Before: A -> B a | c")
    print("        B -> A b | d")
    print("Substitute A's rules into B:")
    print("B -> B a b | c b | d")
    print("Remove immediate left recursion:")
    print("B -> (c b | d) B'")
    print("B' -> a b B' | ε")
    print("Note: A remains A -> B a | c.")


def left_factoring():
    print("\n3) Left factoring")
    print("Before: A -> a b | a c")
    print("After : A -> a A'")
    print("        A' -> b | c")


def dangling_else():
    print("\n4) Dangling-else resolution (matched/open form)")
    print("Stmt        -> Matched | Open")
    print("Matched     -> if E then Matched else Matched | other")
    print("Open        -> if E then Stmt")
    print("            | if E then Matched else Open")


def main():
    print("SECTION 4.3 - WRITING A GRAMMAR\n")
    immediate_left_recursion()
    non_immediate_left_recursion()
    left_factoring()
    dangling_else()


if __name__ == "__main__":
    main()
