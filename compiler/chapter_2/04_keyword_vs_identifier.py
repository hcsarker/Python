"""
Chapter 2 - Problem 4: Distinguishing Keyword from Identifier
Course: CIT 412: Compiler Design and Automata Theory Sessional

This program demonstrates how a compiler distinguishes between keywords and identifiers.
In programming languages (e.g., C, Java, Python), both keywords and identifiers match the same
lexical pattern:
    Pattern: [a-zA-Z_][a-zA-Z0-9_]*

Dragon Book Principle (Sec 2.6 / 2.7):
The lexical analyzer treats all words matching the pattern as candidate words, then performs
a lookup in a reserved keyword table (hash table).
    - If found in Reserved Table -> Token: KEYWORD (e.g., IF, ELSE, INT, WHILE)
    - If NOT found in Reserved Table -> Token: IDENTIFIER, and it is stored in the Symbol Table.
"""

from typing import Dict, Any, Optional

# Standard C/C++ language keywords
RESERVED_KEYWORDS = {
    "auto", "break", "case", "char", "const", "continue", "default", "do",
    "double", "else", "enum", "extern", "float", "for", "goto", "if",
    "int", "long", "register", "return", "short", "signed", "sizeof", "static",
    "struct", "switch", "typedef", "union", "unsigned", "void", "volatile", "while"
}

class SymbolTableEntry:
    def __init__(self, name: str, token_type: str, line: int, col: int, data_type: Optional[str] = None):
        self.name = name
        self.token_type = token_type
        self.first_line = line
        self.first_col = col
        self.occurrences = 1
        self.data_type = data_type

    def __repr__(self):
        return (f"SymbolTableEntry(name='{self.name}', type='{self.token_type}', "
                f"first_seen=({self.first_line}:{self.first_col}), count={self.occurrences})")


class SymbolTable:
    def __init__(self):
        self.table: Dict[str, SymbolTableEntry] = {}

    def insert(self, name: str, token_type: str, line: int, col: int, data_type: Optional[str] = None) -> SymbolTableEntry:
        if name in self.table:
            self.table[name].occurrences += 1
            return self.table[name]
        entry = SymbolTableEntry(name, token_type, line, col, data_type)
        self.table[name] = entry
        return entry

    def lookup(self, name: str) -> Optional[SymbolTableEntry]:
        return self.table.get(name, None)

    def display(self):
        print("\n" + "=" * 75)
        print("                        SYMBOL TABLE")
        print("=" * 75)
        print(f"{'Index':<6} | {'Identifier Name':<20} | {'Type':<12} | {'First Seen (L:C)':<18} | {'Occurrences'}")
        print("-" * 75)
        for i, (name, entry) in enumerate(self.table.items(), 1):
            pos_str = f"Line {entry.first_line}, Col {entry.first_col}"
            print(f"{i:<6} | {entry.name:<20} | {entry.token_type:<12} | {pos_str:<18} | {entry.occurrences}")
        print("=" * 75)


class KeywordIdentifierLexer:
    def __init__(self, source_code: str):
        self.src = source_code
        self.pos = 0
        self.length = len(source_code)
        self.line = 1
        self.col = 1
        self.symbol_table = SymbolTable()

    def advance(self):
        if self.pos < self.length:
            if self.src[self.pos] == '\n':
                self.line += 1
                self.col = 1
            else:
                self.col += 1
            self.pos += 1

    def peek(self) -> Optional[str]:
        if self.pos < self.length:
            return self.src[self.pos]
        return None

    def scan_tokens(self):
        tokens = []

        while self.pos < self.length:
            ch = self.peek()

            # Skip whitespace
            if ch.isspace():
                self.advance()
                continue

            # Skip comments
            if ch == '/' and self.pos + 1 < self.length:
                next_ch = self.src[self.pos + 1]
                if next_ch == '/':  # single line comment
                    while self.pos < self.length and self.peek() != '\n':
                        self.advance()
                    continue
                elif next_ch == '*':  # multi line comment
                    self.advance()
                    self.advance()
                    while self.pos + 1 < self.length and not (self.src[self.pos] == '*' and self.src[self.pos+1] == '/'):
                        self.advance()
                    self.advance() # consume '*'
                    self.advance() # consume '/'
                    continue

            # Candidate word matching [a-zA-Z_][a-zA-Z0-9_]*
            if ch.isalpha() or ch == '_':
                start_col = self.col
                start_line = self.line
                word = ""
                while self.pos < self.length and (self.peek().isalnum() or self.peek() == '_'):
                    word += self.peek()
                    self.advance()

                # Classification: Keyword vs Identifier
                if word in RESERVED_KEYWORDS:
                    # It's a reserved keyword
                    token = {
                        "category": "KEYWORD",
                        "lexeme": word,
                        "attribute": word.upper(),
                        "line": start_line,
                        "col": start_col
                    }
                else:
                    # It's an identifier -> register in symbol table
                    entry = self.symbol_table.insert(word, "IDENTIFIER", start_line, start_col)
                    token = {
                        "category": "IDENTIFIER",
                        "lexeme": word,
                        "attribute": f"PTR_TO_SYM_TABLE('{word}')",
                        "line": start_line,
                        "col": start_col
                    }
                tokens.append(token)
                continue

            # Numbers
            if ch.isdigit():
                start_col = self.col
                start_line = self.line
                num_str = ""
                while self.pos < self.length and (self.peek().isdigit() or self.peek() == '.'):
                    num_str += self.peek()
                    self.advance()
                tokens.append({
                    "category": "NUMBER",
                    "lexeme": num_str,
                    "attribute": float(num_str) if '.' in num_str else int(num_str),
                    "line": start_line,
                    "col": start_col
                })
                continue

            # Other symbols/operators
            start_col = self.col
            start_line = self.line
            sym = ch
            self.advance()
            tokens.append({
                "category": "SYMBOL",
                "lexeme": sym,
                "attribute": sym,
                "line": start_line,
                "col": start_col
            })

        return tokens


def main():
    print("=" * 75)
    print(" CIT 412: Chapter 2 - Problem 4: Distinguishing Keyword from Identifier")
    print("=" * 75)

    sample_code = """
    // Calculate factorial and status
    int count = 10;
    float total_sum = 0.0;
    while (count > 0) {
        if (count == 5) {
            int special_marker = 1;
            total_sum = total_sum + count;
        } else {
            total_sum = total_sum + count * 2;
        }
        count = count - 1;
    }
    return total_sum;
    """

    print("Source Code Input:")
    print("-" * 50)
    print(sample_code.strip())
    print("-" * 50)

    lexer = KeywordIdentifierLexer(sample_code)
    tokens = lexer.scan_tokens()

    print(f"\n{'Line:Col':<10} | {'Token Type':<15} | {'Lexeme':<18} | {'Attribute Value'}")
    print("-" * 75)
    for tok in tokens:
        if tok["category"] in ("KEYWORD", "IDENTIFIER"):
            pos_str = f"{tok['line']}:{tok['col']}"
            print(f"{pos_str:<10} | {tok['category']:<15} | {tok['lexeme']:<18} | {tok['attribute']}")

    # Display resulting symbol table
    lexer.symbol_table.display()

if __name__ == "__main__":
    main()
