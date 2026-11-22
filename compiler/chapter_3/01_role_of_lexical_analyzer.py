"""
Chapter 3 - Section 3.1: The Role of the Lexical Analyzer
Course: CIT 412: Compiler Design and Automata Theory Sessional

Textbook Reference: Dragon Book (Aho, Lam, Sethi, Ullman), Section 3.1
Tasks:
1. Divide a sample code block into appropriate lexemes.
2. Determine token names, lexemes, and associated attribute values.
3. Identify tokens that require attribute values (e.g. numeric values, symbol table pointers)
   versus tokens that do not (e.g. keywords, punctuation).
"""

from typing import List, Dict, Any, Tuple

# Token specifications
class Token:
    def __init__(self, token_name: str, lexeme: str, attribute_value: Any, line: int, col: int):
        self.token_name = token_name
        self.lexeme = lexeme
        self.attribute_value = attribute_value
        self.line = line
        self.col = col

    def __repr__(self):
        attr_display = f"'{self.attribute_value}'" if isinstance(self.attribute_value, str) else str(self.attribute_value)
        return f"<{self.token_name}, {attr_display}> (lexeme: '{self.lexeme}', L{self.line}:C{self.col})"


KEYWORDS = {"int", "float", "char", "if", "else", "while", "for", "return", "void"}
RELATIONAL_OPS = {"<", "<=", ">", ">=", "==", "!="}
ARITHMETIC_OPS = {"+", "-", "*", "/", "%"}
ASSIGN_OP = {"="}
DELIMITERS = {";", ",", "(", ")", "{", "}", "[", "]"}


class LexicalAnalyzerSec31:
    def __init__(self, source_code: str):
        self.src = source_code
        self.n = len(source_code)
        self.pos = 0
        self.line = 1
        self.col = 1
        self.symbol_table = {}

    def get_symbol_table_entry(self, identifier: str) -> int:
        if identifier not in self.symbol_table:
            idx = len(self.symbol_table) + 1
            self.symbol_table[identifier] = idx
        return self.symbol_table[identifier]

    def tokenize(self) -> List[Token]:
        tokens = []

        while self.pos < self.n:
            ch = self.src[self.pos]

            # Whitespace handling
            if ch.isspace():
                if ch == '\n':
                    self.line += 1
                    self.col = 1
                else:
                    self.col += 1
                self.pos += 1
                continue

            # Comment handling: // and /* */
            if ch == '/' and self.pos + 1 < self.n:
                next_c = self.src[self.pos + 1]
                if next_c == '/':
                    while self.pos < self.n and self.src[self.pos] != '\n':
                        self.pos += 1
                    continue
                elif next_c == '*':
                    self.pos += 2
                    self.col += 2
                    while self.pos + 1 < self.n and not (self.src[self.pos] == '*' and self.src[self.pos + 1] == '/'):
                        if self.src[self.pos] == '\n':
                            self.line += 1
                            self.col = 1
                        else:
                            self.col += 1
                        self.pos += 1
                    self.pos += 2 # skip */
                    self.col += 2
                    continue

            start_col = self.col
            start_line = self.line

            # Two-character Relational/Logical Operators
            if self.pos + 1 < self.n:
                two_char = self.src[self.pos:self.pos+2]
                if two_char in ("<=", ">=", "==", "!="):
                    attr = {"<=": "LE", ">=": "GE", "==": "EQ", "!=": "NE"}[two_char]
                    tokens.append(Token("RELOP", two_char, attr, start_line, start_col))
                    self.pos += 2
                    self.col += 2
                    continue

            # Single-character Relational Operators
            if ch in ('<', '>'):
                attr = "LT" if ch == '<' else "GT"
                tokens.append(Token("RELOP", ch, attr, start_line, start_col))
                self.pos += 1
                self.col += 1
                continue

            # Assignment or Equality
            if ch == '=':
                tokens.append(Token("ASSIGNOP", "=", None, start_line, start_col))
                self.pos += 1
                self.col += 1
                continue

            # Arithmetic Operators
            if ch in ARITHMETIC_OPS:
                tokens.append(Token("ARITHOP", ch, ch, start_line, start_col))
                self.pos += 1
                self.col += 1
                continue

            # Delimiters
            if ch in DELIMITERS:
                tokens.append(Token("DELIM", ch, None, start_line, start_col))
                self.pos += 1
                self.col += 1
                continue

            # String literals
            if ch == '"':
                start_p = self.pos
                self.pos += 1
                self.col += 1
                str_val = []
                while self.pos < self.n and self.src[self.pos] != '"':
                    str_val.append(self.src[self.pos])
                    self.pos += 1
                    self.col += 1
                if self.pos < self.n and self.src[self.pos] == '"':
                    self.pos += 1
                    self.col += 1
                content = "".join(str_val)
                lexeme = self.src[start_p:self.pos]
                tokens.append(Token("STRING_LITERAL", lexeme, content, start_line, start_col))
                continue

            # Identifiers and Keywords
            if ch.isalpha() or ch == '_':
                ident = []
                while self.pos < self.n and (self.src[self.pos].isalnum() or self.src[self.pos] == '_'):
                    ident.append(self.src[self.pos])
                    self.pos += 1
                    self.col += 1
                lexeme = "".join(ident)
                if lexeme in KEYWORDS:
                    # Keywords typically have token name equal to keyword or KEYWORD, attribute is None/KEYWORD
                    tokens.append(Token(lexeme.upper(), lexeme, None, start_line, start_col))
                else:
                    # Identifier has attribute pointing to symbol table entry
                    sym_id = self.get_symbol_table_entry(lexeme)
                    tokens.append(Token("ID", lexeme, f"sym_ptr#{sym_id}", start_line, start_col))
                continue

            # Numbers (integer or floating point)
            if ch.isdigit():
                num_chars = []
                has_dot = False
                while self.pos < self.n and (self.src[self.pos].isdigit() or self.src[self.pos] == '.'):
                    if self.src[self.pos] == '.':
                        if has_dot: break
                        has_dot = True
                    num_chars.append(self.src[self.pos])
                    self.pos += 1
                    self.col += 1
                lexeme = "".join(num_chars)
                num_val = float(lexeme) if has_dot else int(lexeme)
                tokens.append(Token("NUM", lexeme, num_val, start_line, start_col))
                continue

            # Unknown character
            tokens.append(Token("ERROR", ch, f"Unknown character '{ch}'", start_line, start_col))
            self.pos += 1
            self.col += 1

        return tokens


def main():
    print("=" * 80)
    print(" CIT 412: Chapter 3 - Section 3.1: The Role of the Lexical Analyzer")
    print("=" * 80)

    sample_code = """
    /* Calculate final price */
    float calculate_tax(float subtotal) {
        float rate = 0.075;
        if (subtotal >= 100.0) {
            rate = 0.05; // Discounted rate for large orders
        }
        float tax = subtotal * rate;
        return tax;
    }
    """

    print("Source Code Snippet:")
    print("-" * 60)
    print(sample_code.strip())
    print("-" * 60)

    analyzer = LexicalAnalyzerSec31(sample_code)
    tokens = analyzer.tokenize()

    print(f"\n{'Line:Col':<10} | {'Lexeme':<16} | {'Token Name':<16} | {'Attribute Value':<20} | {'Attribute Needed?'}")
    print("-" * 80)
    for tok in tokens:
        pos_str = f"L{tok.line}:C{tok.col}"
        attr_needed = "No (unique syntax)" if tok.attribute_value is None else "Yes (value/sym table pointer)"
        attr_str = str(tok.attribute_value) if tok.attribute_value is not None else "-"
        print(f"{pos_str:<10} | {tok.lexeme:<16} | {tok.token_name:<16} | {attr_str:<20} | {attr_needed}")

    print("\n" + "=" * 80)
    print(" Symbol Table Entries Created:")
    for ident, idx in analyzer.symbol_table.items():
        print(f"  Entry #{idx}: identifier '{ident}'")
    print("=" * 80)

if __name__ == "__main__":
    main()
