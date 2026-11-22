"""
Chapter 2 - Problem 3: Infix to Postfix Translation
Course: CIT 412: Compiler Design and Automata Theory Sessional

This program demonstrates Infix to Postfix conversion using two foundational compiler approaches:
1. Syntax-Directed Translation (SDT) via Recursive Descent (Aho, Sethi, Ullman - Dragon Book Sec 2.3)
2. Operator Precedence Stack Algorithm (Shunting-Yard) with step-by-step stack tracing.
"""

# ==============================================================================
# Method 1: Syntax-Directed Translation (Dragon Book Chapter 2.3)
# ==============================================================================
# Grammar with Semantic Actions:
#   expr -> term rest
#   rest -> + term { print('+') } rest
#         | - term { print('-') } rest
#         | ε
#   term -> 0 { print('0') } | 1 { print('1') } | ... | ( expr ) | id

class SyntaxDirectedTranslator:
    def __init__(self, expr_str):
        self.text = expr_str.replace(" ", "")
        self.pos = 0
        self.lookahead = self.text[0] if len(self.text) > 0 else None
        self.output = []

    def match(self, char):
        if self.lookahead == char:
            self.pos += 1
            self.lookahead = self.text[self.pos] if self.pos < len(self.text) else None
        else:
            raise SyntaxError(f"Syntax error: expected '{char}', found '{self.lookahead}'")

    def expr(self):
        self.term()
        self.rest()

    def rest(self):
        while self.lookahead in ('+', '-'):
            op = self.lookahead
            self.match(op)
            self.term()
            self.output.append(op)  # Semantic action: emit operator after operands

    def term(self):
        self.factor()
        while self.lookahead in ('*', '/'):
            op = self.lookahead
            self.match(op)
            self.factor()
            self.output.append(op)  # Semantic action: emit operator

    def factor(self):
        if self.lookahead is not None and self.lookahead.isalnum():
            # Variable or digit
            val = ""
            while self.lookahead is not None and (self.lookahead.isalnum() or self.lookahead == '_'):
                val += self.lookahead
                self.pos += 1
                self.lookahead = self.text[self.pos] if self.pos < len(self.text) else None
            self.output.append(val)
        elif self.lookahead == '(':
            self.match('(')
            self.expr()
            self.match(')')
        else:
            raise SyntaxError(f"Unexpected token: '{self.lookahead}'")

    def translate(self):
        self.expr()
        if self.lookahead is not None:
            raise SyntaxError(f"Unexpected trailing input: '{self.lookahead}'")
        return " ".join(self.output)


# ==============================================================================
# Method 2: Stack-based Shunting-Yard Algorithm with Step-by-Step Trace
# ==============================================================================
def infix_to_postfix_stack(expression, show_trace=True):
    """
    Converts infix expression to postfix notation using an operator stack.
    Returns: postfix string, and prints trace table if show_trace=True.
    """
    precedence = {'+': 1, '-': 1, '*': 2, '/': 2, '^': 3}
    associativity = {'+': 'L', '-': 'L', '*': 'L', '/': 'L', '^': 'R'}

    tokens = []
    i = 0
    n = len(expression)
    while i < n:
        c = expression[i]
        if c.isspace():
            i += 1
            continue
        if c.isalnum() or c == '_':
            token = ""
            while i < n and (expression[i].isalnum() or expression[i] == '_'):
                token += expression[i]
                i += 1
            tokens.append(token)
            continue
        if c in "+-*/^()":
            tokens.append(c)
            i += 1
            continue
        raise ValueError(f"Unknown character in expression: {c}")

    stack = []
    output = []

    if show_trace:
        print(f"\n{'Token':<10} | {'Action':<35} | {'Operator Stack':<20} | {'Postfix Output'}")
        print("-" * 85)

    for token in tokens:
        action = ""
        # 1. If token is operand, add to output
        if token.isalnum() or '_' in token:
            output.append(token)
            action = f"Emit operand '{token}'"
        
        # 2. If left parenthesis, push to stack
        elif token == '(':
            stack.append(token)
            action = "Push '(' to stack"

        # 3. If right parenthesis, pop until '('
        elif token == ')':
            while stack and stack[-1] != '(':
                output.append(stack.pop())
            if not stack:
                raise ValueError("Mismatched parentheses in expression")
            stack.pop() # Discard '('
            action = "Pop operators until '('"

        # 4. If operator
        elif token in precedence:
            while (stack and stack[-1] != '(' and
                   (precedence[stack[-1]] > precedence[token] or
                    (precedence[stack[-1]] == precedence[token] and associativity[token] == 'L'))):
                popped = stack.pop()
                output.append(popped)
            stack.append(token)
            action = f"Push operator '{token}'"

        if show_trace:
            stack_str = " ".join(stack) if stack else "<empty>"
            out_str = " ".join(output)
            print(f"{token:<10} | {action:<35} | {stack_str:<20} | {out_str}")

    # Pop remaining operators
    while stack:
        top = stack.pop()
        if top in ('(', ')'):
            raise ValueError("Mismatched parentheses in expression")
        output.append(top)
        if show_trace:
            stack_str = " ".join(stack) if stack else "<empty>"
            out_str = " ".join(output)
            print(f"{'<EOF>':<10} | {f'Pop remaining: {top}':<35} | {stack_str:<20} | {out_str}")

    return " ".join(output)


def main():
    print("=" * 70)
    print(" CIT 412: Chapter 2 - Problem 3: Infix to Postfix Translation")
    print("=" * 70)

    test_cases = [
        "a + b * c",
        "(A + B) * (C - D)",
        "x + y * z - (p / q + r)",
        "9 - 5 + 2"
    ]

    for expr in test_cases:
        print(f"\n=======================================================")
        print(f" Input Infix:  {expr}")
        print(f"=======================================================")
        
        # Method 1: SDT
        try:
            sdt = SyntaxDirectedTranslator(expr)
            sdt_result = sdt.translate()
            print(f" [Method 1: Dragon Book SDT]  -->  {sdt_result}")
        except Exception as e:
            print(f" [Method 1: SDT Error]        -->  {e}")

        # Method 2: Stack-based with trace
        print(f"\n [Method 2: Stack-based Shunting-Yard Trace]")
        stack_result = infix_to_postfix_stack(expr, show_trace=True)
        print(f"\n Final Postfix Result: {stack_result}")

if __name__ == "__main__":
    main()
