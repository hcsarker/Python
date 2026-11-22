# Section 4.9 - Parser Generators (Yacc/Bison concepts in Python)
# Problems: calculator with variables, error recovery, and mini-parser/AST.
# This is a Python learning version, not a Lex/Yacc implementation.
# Run: python 4.9.py

import ast
import operator

# Safe evaluator for a small arithmetic language; no Python eval() is used.
OPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.USub: operator.neg,
    ast.UAdd: operator.pos,
}


def evaluate_node(node, variables):
    if isinstance(node, ast.Expression):
        return evaluate_node(node.body, variables)
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return node.value
    if isinstance(node, ast.Name):
        if node.id not in variables:
            raise ValueError("Unknown variable: " + node.id)
        return variables[node.id]
    if isinstance(node, ast.BinOp) and type(node.op) in OPS:
        left = evaluate_node(node.left, variables)
        right = evaluate_node(node.right, variables)
        if isinstance(node.op, ast.Div) and right == 0:
            raise ValueError("Division by zero")
        return OPS[type(node.op)](left, right)
    if isinstance(node, ast.UnaryOp) and type(node.op) in OPS:
        return OPS[type(node.op)](evaluate_node(node.operand, variables))
    raise ValueError("Unsupported expression")


def main():
    print("SECTION 4.9 - MINI CALCULATOR / PARSER")
    print("Enter: x = 10, then x + 5. Type q to quit.")
    variables = {}

    while True:
        line = input(">>> ").strip()
        if line.lower() == "q":
            break
        if not line:
            continue

        try:
            if "=" in line:
                name, expression = line.split("=", 1)
                name = name.strip()
                if not name.isidentifier():
                    raise ValueError("Invalid variable name")
                tree = ast.parse(expression.strip(), mode="eval")
                value = evaluate_node(tree, variables)
                variables[name] = value
                print(name, "=", value)
            else:
                tree = ast.parse(line, mode="eval")
                print("Result =", evaluate_node(tree, variables))
                print("AST =", ast.dump(tree, indent=2))
        except (SyntaxError, ValueError, ZeroDivisionError) as error:
            # Panic-mode style recovery: report the bad line and accept the next line.
            print("Syntax/Error:", error)
            print("Skipping this line; enter the next statement.")


if __name__ == "__main__":
    main()
