"""
Chapter 2 - Problem 2: Abstract Syntax Tree (AST)
Course: CIT 412: Compiler Design and Automata Theory Sessional

This program constructs, visualizes, and evaluates an Abstract Syntax Tree (AST).
In an AST, interior nodes represent operators (e.g. +, -, *, /) and leaves
represent operands (variables, constants). Syntactic details like parentheses and
non-terminals are discarded.
"""

class ASTNode:
    """Base class for all AST nodes."""
    pass

class NumNode(ASTNode):
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f"Num({self.value})"

class VarNode(ASTNode):
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"Var({self.name})"

class BinOpNode(ASTNode):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

    def __repr__(self):
        return f"BinOp({self.left}, '{self.op}', {self.right})"

class AssignNode(ASTNode):
    def __init__(self, var_name, expr):
        self.var_name = var_name
        self.expr = expr

    def __repr__(self):
        return f"Assign({self.var_name} = {self.expr})"


def display_ast(node, prefix="", is_last=True):
    """Prints the AST in a structured visual tree representation."""
    if node is None:
        return
    
    connector = "└── " if is_last else "├── "
    
    if isinstance(node, NumNode):
        print(prefix + connector + f"Num: {node.value}")
    elif isinstance(node, VarNode):
        print(prefix + connector + f"Var: {node.name}")
    elif isinstance(node, BinOpNode):
        print(prefix + connector + f"Op: '{node.op}'")
        new_prefix = prefix + ("    " if is_last else "│   ")
        display_ast(node.left, new_prefix, False)
        display_ast(node.right, new_prefix, True)
    elif isinstance(node, AssignNode):
        print(prefix + connector + f"Assign: '{node.var_name}' =")
        new_prefix = prefix + ("    " if is_last else "│   ")
        display_ast(node.expr, new_prefix, True)


def evaluate_ast(node, env=None):
    """Evaluates the AST given an optional variable environment dictionary."""
    if env is None:
        env = {}

    if isinstance(node, NumNode):
        return node.value
    elif isinstance(node, VarNode):
        if node.name in env:
            return env[node.name]
        raise ValueError(f"Undefined variable: '{node.name}'")
    elif isinstance(node, BinOpNode):
        lval = evaluate_ast(node.left, env)
        rval = evaluate_ast(node.right, env)
        if node.op == '+': return lval + rval
        elif node.op == '-': return lval - rval
        elif node.op == '*': return lval * rval
        elif node.op == '/': 
            if rval == 0:
                raise ZeroDivisionError("Division by zero")
            return lval / rval
        else:
            raise ValueError(f"Unknown operator: {node.op}")
    elif isinstance(node, AssignNode):
        val = evaluate_ast(node.expr, env)
        env[node.var_name] = val
        return val


class ASTParser:
    """Recursive descent parser to construct AST directly from expression/statement."""
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.tokens = self.tokenize(text)
        self.token_idx = 0

    def tokenize(self, text):
        tokens = []
        i = 0
        n = len(text)
        while i < n:
            c = text[i]
            if c.isspace():
                i += 1
                continue
            if c.isdigit():
                num_str = ""
                while i < n and (text[i].isdigit() or text[i] == '.'):
                    num_str += text[i]
                    i += 1
                tokens.append(('NUM', float(num_str) if '.' in num_str else int(num_str)))
                continue
            if c.isalpha() or c == '_':
                ident = ""
                while i < n and (text[i].isalnum() or text[i] == '_'):
                    ident += text[i]
                    i += 1
                tokens.append(('ID', ident))
                continue
            if c in "+-*/()=":
                tokens.append((c, c))
                i += 1
                continue
            raise ValueError(f"Unexpected character in lexer: {c}")
        tokens.append(('EOF', None))
        return tokens

    @property
    def current_token(self):
        return self.tokens[self.token_idx]

    def consume(self, expected_type=None):
        tok = self.current_token
        if expected_type and tok[0] != expected_type:
            raise ValueError(f"Expected token {expected_type} but got {tok[0]}")
        self.token_idx += 1
        return tok

    def parse(self):
        # Check if this is an assignment statement: ID = expr
        if self.token_idx + 1 < len(self.tokens) and self.tokens[self.token_idx][0] == 'ID' and self.tokens[self.token_idx+1][0] == '=':
            var_name = self.consume('ID')[1]
            self.consume('=')
            expr = self.expr()
            return AssignNode(var_name, expr)
        return self.expr()

    def expr(self):
        node = self.term()
        while self.current_token[0] in ('+', '-'):
            op = self.consume()[0]
            node = BinOpNode(node, op, self.term())
        return node

    def term(self):
        node = self.factor()
        while self.current_token[0] in ('*', '/'):
            op = self.consume()[0]
            node = BinOpNode(node, op, self.factor())
        return node

    def factor(self):
        tok = self.current_token
        if tok[0] == 'NUM':
            self.consume('NUM')
            return NumNode(tok[1])
        elif tok[0] == 'ID':
            self.consume('ID')
            return VarNode(tok[1])
        elif tok[0] == '(':
            self.consume('(')
            node = self.expr()
            self.consume(')')
            return node
        elif tok[0] == '-':
            self.consume('-')
            # Represent unary minus as 0 - factor
            return BinOpNode(NumNode(0), '-', self.factor())
        else:
            raise ValueError(f"Unexpected token in factor: {tok}")


def main():
    print("=" * 60)
    print(" CIT 412: Chapter 2 - Problem 2: Abstract Syntax Tree (AST)")
    print("=" * 60)

    test_cases = [
        "a + b * c",
        "(x + y) * (z - 5)",
        "result = 10 + 20 * 3"
    ]

    for test in test_cases:
        print(f"\nSource Code: {test}")
        print("-" * 50)
        parser = ASTParser(test)
        ast = parser.parse()
        print("Visual AST:")
        display_ast(ast)
        print(f"\nInternal Representation: {ast}")

    # Evaluation demonstration
    eval_expr = "x + y * 2"
    env = {'x': 10, 'y': 5}
    parser = ASTParser(eval_expr)
    ast = parser.parse()
    print(f"\nEvaluating: '{eval_expr}' with environment {env}")
    result = evaluate_ast(ast, env)
    print(f"Result = {result}")

if __name__ == "__main__":
    main()
