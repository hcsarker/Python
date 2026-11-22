"""
Chapter 3 - Section 3.4: Recognition of Tokens via Transition Diagrams (DFA Simulation)
Course: CIT 412: Compiler Design and Automata Theory Sessional

Textbook Reference: Dragon Book (Aho, Lam, Sethi, Ullman), Section 3.4
Focus:
Explicitly simulating state machines (Transition Diagrams) for:
1. Identifiers: letter (letter | digit)*
2. Numbers:
   - Integer (e.g. 42)
   - Floating point (e.g. 3.14159)
   - Scientific notation / Exponential (e.g. 6.022e+23, 1.5e-3)
3. Relational Operators (<, <=, <>, >, >=, ==, =)
"""

from typing import Tuple, Optional, Any

class TransitionDiagramSimulator:
    def __init__(self, text: str):
        self.text = text
        self.pos = 0
        self.n = len(text)

    def peek(self) -> Optional[str]:
        if self.pos < self.n:
            return self.text[self.pos]
        return None

    def advance(self) -> Optional[str]:
        ch = self.peek()
        if ch is not None:
            self.pos += 1
        return ch

    def retract(self, count: int = 1):
        self.pos = max(0, self.pos - count)

    # --------------------------------------------------------------------------
    # 1. Transition Diagram for Identifiers (Dragon Book Fig 3.23)
    # --------------------------------------------------------------------------
    # State 0: [start] --(letter)--> State 1
    # State 1: --(letter|digit)--> State 1
    # State 1: --(other)--> State 2 [accept, retract]
    def recognize_identifier(self) -> Optional[Tuple[str, str, list]]:
        start_pos = self.pos
        state = 0
        lexeme = []
        transitions = []

        while True:
            c = self.peek()
            transitions.append((state, c))

            if state == 0:
                if c is not None and (c.isalpha() or c == '_'):
                    state = 1
                    lexeme.append(self.advance())
                else:
                    return None  # Not an identifier
            elif state == 1:
                if c is not None and (c.isalnum() or c == '_'):
                    state = 1
                    lexeme.append(self.advance())
                else:
                    # Other character -> accept state 2 with retraction
                    state = 2
                    # Retract not needed if we only peeked 'other' without advance
                    return ("IDENTIFIER", "".join(lexeme), transitions)

    # --------------------------------------------------------------------------
    # 2. Transition Diagram for Numbers (Dragon Book Fig 3.26)
    # --------------------------------------------------------------------------
    # Integer, Float, and Scientific Exponential (e.g. 1.25E+10)
    # States:
    # 10: [start] --digit--> 11
    # 11: --digit--> 11; --'.'--> 12; --'e'|'E'--> 14; --other--> 19 [Accept INT]
    # 12: --digit--> 13
    # 13: --digit--> 13; --'e'|'E'--> 14; --other--> 20 [Accept FLOAT]
    # 14: --'+'|'-'--> 15; --digit--> 16
    # 15: --digit--> 16
    # 16: --digit--> 16; --other--> 21 [Accept EXP_NUM]
    def recognize_number(self) -> Optional[Tuple[str, Any, list]]:
        start_pos = self.pos
        state = 10
        lexeme = []
        transitions = []

        while True:
            c = self.peek()
            transitions.append((state, c))

            if state == 10:
                if c is not None and c.isdigit():
                    state = 11
                    lexeme.append(self.advance())
                else:
                    return None
            elif state == 11:
                if c is not None and c.isdigit():
                    lexeme.append(self.advance())
                elif c == '.':
                    state = 12
                    lexeme.append(self.advance())
                elif c in ('e', 'E'):
                    state = 14
                    lexeme.append(self.advance())
                else:
                    state = 19  # Accept Integer
                    return ("INT", int("".join(lexeme)), transitions)
            elif state == 12:
                if c is not None and c.isdigit():
                    state = 13
                    lexeme.append(self.advance())
                else:
                    # A dot without following digits -> rollback
                    self.pos = start_pos
                    return None
            elif state == 13:
                if c is not None and c.isdigit():
                    lexeme.append(self.advance())
                elif c in ('e', 'E'):
                    state = 14
                    lexeme.append(self.advance())
                else:
                    state = 20  # Accept Float
                    return ("FLOAT", float("".join(lexeme)), transitions)
            elif state == 14:
                if c in ('+', '-'):
                    state = 15
                    lexeme.append(self.advance())
                elif c is not None and c.isdigit():
                    state = 16
                    lexeme.append(self.advance())
                else:
                    self.pos = start_pos
                    return None
            elif state == 15:
                if c is not None and c.isdigit():
                    state = 16
                    lexeme.append(self.advance())
                else:
                    self.pos = start_pos
                    return None
            elif state == 16:
                if c is not None and c.isdigit():
                    lexeme.append(self.advance())
                else:
                    state = 21  # Accept Exponential Float
                    return ("EXP_FLOAT", float("".join(lexeme)), transitions)

    # --------------------------------------------------------------------------
    # 3. Transition Diagram for Relational Operators (Dragon Book Fig 3.25)
    # --------------------------------------------------------------------------
    # State 0:
    #   '<' -> 1: '=' -> 2 (LE); '>' -> 3 (NE); other -> 4 (LT)
    #   '=' -> 5: '=' -> 6 (EQ); other -> 7 (ASSIGN)
    #   '>' -> 8: '=' -> 9 (GE); other -> 10 (GT)
    def recognize_relop(self) -> Optional[Tuple[str, str, list]]:
        state = 0
        transitions = []
        c = self.peek()
        if c not in ('<', '=', '>', '!'):
            return None

        transitions.append((0, c))
        ch = self.advance()

        if ch == '<':
            c2 = self.peek()
            transitions.append((1, c2))
            if c2 == '=':
                self.advance()
                return ("RELOP", "LE", transitions)
            elif c2 == '>':
                self.advance()
                return ("RELOP", "NE", transitions)
            else:
                return ("RELOP", "LT", transitions)

        elif ch == '>':
            c2 = self.peek()
            transitions.append((8, c2))
            if c2 == '=':
                self.advance()
                return ("RELOP", "GE", transitions)
            else:
                return ("RELOP", "GT", transitions)

        elif ch == '=':
            c2 = self.peek()
            transitions.append((5, c2))
            if c2 == '=':
                self.advance()
                return ("RELOP", "EQ", transitions)
            else:
                return ("ASSIGNOP", "ASSIGN", transitions)

        elif ch == '!':
            c2 = self.peek()
            transitions.append((11, c2))
            if c2 == '=':
                self.advance()
                return ("RELOP", "NE", transitions)
            else:
                return ("NOTOP", "NOT", transitions)

        return None


def run_transition_demos():
    print("=" * 80)
    print(" CIT 412: Chapter 3 - Section 3.4: Transition Diagrams (DFA Recognition)")
    print("=" * 80)

    # 1. Identifier DFA Demo
    id_samples = ["temperature", "var_123", "_privateVal"]
    print("\n[1. Testing Identifier Transition Diagram (States 0 -> 1 -> 2)]")
    for s in id_samples:
        sim = TransitionDiagramSimulator(s)
        res = sim.recognize_identifier()
        if res:
            kind, lex, trace = res
            path = " -> ".join(f"S{state}(peek '{char}')" for state, char in trace)
            print(f"  Input: '{s:<15}' => Token: <{kind}, '{lex}'> | Path: {path}")

    # 2. Number DFA Demo (Int, Float, Scientific)
    num_samples = ["1024", "3.14159", "6.022e23", "1.75E-12", "0.005"]
    print("\n[2. Testing Number Transition Diagram (States 10..21)]")
    for s in num_samples:
        sim = TransitionDiagramSimulator(s)
        res = sim.recognize_number()
        if res:
            kind, val, trace = res
            print(f"  Input: '{s:<15}' => Token: <{kind}, {val}> (evaluated: {val})")

    # 3. Relational Operators DFA Demo
    relop_samples = ["<=", "<>", "<", ">=", ">", "==", "="]
    print("\n[3. Testing Relational Operators Transition Diagram]")
    for s in relop_samples:
        sim = TransitionDiagramSimulator(s)
        res = sim.recognize_relop()
        if res:
            kind, attr, trace = res
            print(f"  Input: '{s:<8}' => Token: <{kind}, {attr}>")

    print("\n" + "=" * 80)

if __name__ == "__main__":
    run_transition_demos()
