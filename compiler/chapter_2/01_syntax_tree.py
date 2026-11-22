"""
Chapter 2 - Problem 1: Syntax Tree (Concrete Parse Tree)
Course: CIT 412: Compiler Design and Automata Theory Sessional

This program constructs and displays a full Concrete Syntax Tree (Parse Tree)
for arithmetic expressions using a Context-Free Grammar (CFG) via Recursive Descent Parsing.

Grammar (eliminating left recursion for LL(1) parser):
    E  -> T E'
    E' -> + T E' | - T E' | ε
    T  -> F T'
    T' -> * F T' | / F T' | ε
    F  -> ( E ) | id | num
"""

class ParseTreeNode:
    def __init__(self, name, value=None):
        self.name = name          # Non-terminal or Terminal name
        self.value = value        # Optional token value
        self.children = []        # List of child ParseTreeNodes

    def add_child(self, child):
        if child is not None:
            self.children.append(child)

    def display(self, prefix="", is_last=True):
        """Displays the tree in a clean ASCII hierarchical format."""
        connector = "└── " if is_last else "├── "
        val_str = f" : '{self.value}'" if self.value is not None else ""
        print(prefix + connector + str(self.name) + val_str)
        
        prefix += "    " if is_last else "│   "
        child_count = len(self.children)
        for i, child in enumerate(self.children):
            child.display(prefix, i == (child_count - 1))

    def to_bracket_str(self):
        """Returns the tree in parenthesized LISP-like notation."""
        if not self.children:
            if self.value is not None:
                return f"({self.name} {self.value})"
            return f"{self.name}"
        children_str = " ".join(c.to_bracket_str() for c in self.children)
        return f"({self.name} {children_str})"


class ConcreteSyntaxTreeParser:
    def __init__(self, text):
        self.text = text.replace(" ", "")
        self.pos = 0
        self.current_char = self.text[0] if len(self.text) > 0 else None

    def advance(self):
        self.pos += 1
        if self.pos < len(self.text):
            self.current_char = self.text[self.pos]
        else:
            self.current_char = None

    def parse(self):
        root = self.E()
        if self.current_char is not None:
            raise ValueError(f"Unexpected character at end of input: '{self.current_char}'")
        return root

    # E -> T E'
    def E(self):
        node = ParseTreeNode("E")
        node.add_child(self.T())
        node.add_child(self.E_prime())
        return node

    # E' -> + T E' | - T E' | ε
    def E_prime(self):
        node = ParseTreeNode("E'")
        if self.current_char == '+':
            node.add_child(ParseTreeNode("+", "+"))
            self.advance()
            node.add_child(self.T())
            node.add_child(self.E_prime())
        elif self.current_char == '-':
            node.add_child(ParseTreeNode("-", "-"))
            self.advance()
            node.add_child(self.T())
            node.add_child(self.E_prime())
        else:
            node.add_child(ParseTreeNode("ε"))
        return node

    # T -> F T'
    def T(self):
        node = ParseTreeNode("T")
        node.add_child(self.F())
        node.add_child(self.T_prime())
        return node

    # T' -> * F T' | / F T' | ε
    def T_prime(self):
        node = ParseTreeNode("T'")
        if self.current_char == '*':
            node.add_child(ParseTreeNode("*", "*"))
            self.advance()
            node.add_child(self.F())
            node.add_child(self.T_prime())
        elif self.current_char == '/':
            node.add_child(ParseTreeNode("/", "/"))
            self.advance()
            node.add_child(self.F())
            node.add_child(self.T_prime())
        else:
            node.add_child(ParseTreeNode("ε"))
        return node

    # F -> ( E ) | id | num
    def F(self):
        node = ParseTreeNode("F")
        if self.current_char == '(':
            node.add_child(ParseTreeNode("(", "("))
            self.advance()
            node.add_child(self.E())
            if self.current_char == ')':
                node.add_child(ParseTreeNode(")", ")"))
                self.advance()
            else:
                raise ValueError("Expected ')'")
        elif self.current_char is not None and self.current_char.isalpha():
            # Identifier
            id_str = ""
            while self.current_char is not None and (self.current_char.isalnum() or self.current_char == '_'):
                id_str += self.current_char
                self.advance()
            node.add_child(ParseTreeNode("id", id_str))
        elif self.current_char is not None and self.current_char.isdigit():
            # Number
            num_str = ""
            while self.current_char is not None and self.current_char.isdigit():
                num_str += self.current_char
                self.advance()
            node.add_child(ParseTreeNode("num", num_str))
        else:
            raise ValueError(f"Invalid character in factor: '{self.current_char}'")
        return node


def main():
    print("=" * 60)
    print(" CIT 412: Chapter 2 - Problem 1: Concrete Syntax Tree (Parse Tree)")
    print("=" * 60)

    sample_expressions = [
        "a + b * c",
        "(x + y) * 5",
        "id1 - id2 + 10"
    ]

    for expr in sample_expressions:
        print(f"\nParsing Expression: {expr}")
        print("-" * 50)
        parser = ConcreteSyntaxTreeParser(expr)
        try:
            tree = parser.parse()
            print("Visual Parse Tree:")
            tree.display()
            print("\nParenthesized Form:")
            print(tree.to_bracket_str())
        except Exception as e:
            print(f"Error parsing '{expr}': {e}")

if __name__ == "__main__":
    main()
