"""
Chapter 3 - Section 3.5: Lex/Flex Scanner & Mini-C Lexical Analyzer
Course: CIT 412: Compiler Design and Automata Theory Sessional

Textbook Reference: Dragon Book (Aho, Lam, Sethi, Ullman), Section 3.5
Contains:
1. Word Count Utility (Classic Lex 'wc' tool: lines, words, chars)
2. Text Pattern Processor: C comment stripper, Email & URL extractor
3. Complete Mini-C Lexical Analyzer & Token-Stream Generator
"""

import re
from typing import List, Dict, Any, Tuple

# ==============================================================================
# 1. Classic Lex 'wc' (Word Count) Tool
# ==============================================================================
def run_wc(text: str) -> Dict[str, int]:
    """Simulates the classic Lex wc specification."""
    lines = text.count('\n')
    if text and not text.endswith('\n'):
        lines += 1
    words = len(text.split())
    chars = len(text)
    return {"lines": lines, "words": words, "characters": chars}


# ==============================================================================
# 2. Text Pattern Processor (Comment Stripper, Email & URL extractor)
# ==============================================================================
def extract_patterns(text: str):
    email_pattern = r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+"
    url_pattern = r"https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+[/\w\.-]*"
    
    emails = re.findall(email_pattern, text)
    urls = re.findall(url_pattern, text)
    return emails, urls


# ==============================================================================
# 3. Complete Mini-C Lexical Analyzer
# ==============================================================================
class MiniCLexer:
    KEYWORDS = {
        "int", "float", "char", "double", "void", "if", "else", 
        "while", "for", "return", "break", "continue"
    }

    TOKEN_SPEC = [
        ("COMMENT_MULTI",  r"/\*[\s\S]*?\*/"),
        ("COMMENT_SINGLE", r"//.*"),
        ("STRING_LIT",     r'"([^"\\]|\\.)*"'),
        ("CHAR_LIT",       r"'([^'\\]|\\.)*'"),
        ("FLOAT_CONST",    r"\d+\.\d+([eE][+-]?\d+)?|\d+[eE][+-]?\d+"),
        ("INT_CONST",      r"\d+"),
        ("RELOP_LE",       r"<="),
        ("RELOP_GE",       r">="),
        ("RELOP_EQ",       r"=="),
        ("RELOP_NE",       r"!="),
        ("ASSIGN",         r"="),
        ("RELOP_LT",       r"<"),
        ("RELOP_GT",       r">"),
        ("LOGIC_AND",      r"&&"),
        ("LOGIC_OR",       r"\|\|"),
        ("LOGIC_NOT",      r"!"),
        ("PLUS",           r"\+"),
        ("MINUS",          r"-"),
        ("MUL",            r"\*"),
        ("DIV",            r"/"),
        ("MOD",            r"%"),
        ("SEMICOLON",      r";"),
        ("COMMA",          r","),
        ("LPAREN",         r"\("),
        ("RPAREN",         r"\)"),
        ("LBRACE",         r"\{"),
        ("RBRACE",         r"\}"),
        ("LBRACKET",       r"\["),
        ("RBRACKET",       r"\]"),
        ("IDENTIFIER",     r"[a-zA-Z_][a-zA-Z0-9_]*"),
        ("NEWLINE",        r"\n"),
        ("SKIP",           r"[ \t\r]+"),
        ("MISMATCH",       r"."),
    ]

    def __init__(self, source_code: str):
        self.code = source_code
        self.symbol_table = {}
        # Compile regex master
        parts = [f"(?P<{name}>{pattern})" for name, pattern in self.TOKEN_SPEC]
        self.master_regex = re.compile("|".join(parts))

    def get_symbol_entry(self, name: str, line: int):
        if name not in self.symbol_table:
            idx = len(self.symbol_table) + 1
            self.symbol_table[name] = {"id": idx, "name": name, "first_line": line, "count": 1}
        else:
            self.symbol_table[name]["count"] += 1
        return self.symbol_table[name]["id"]

    def tokenize(self):
        line_num = 1
        line_start = 0
        tokens = []

        for match in self.master_regex.finditer(self.code):
            kind = match.lastgroup
            val = match.group()
            col = match.start() - line_start + 1

            if kind == "NEWLINE":
                line_start = match.end()
                line_num += 1
                continue
            elif kind == "SKIP" or kind.startswith("COMMENT"):
                # Track newlines in multi-line comments
                if '\n' in val:
                    line_num += val.count('\n')
                    line_start = match.end() - (len(val) - val.rfind('\n') - 1)
                continue
            elif kind == "IDENTIFIER":
                if val in self.KEYWORDS:
                    tokens.append((f"KW_{val.upper()}", val, None, line_num, col))
                else:
                    sym_id = self.get_symbol_entry(val, line_num)
                    tokens.append(("ID", val, f"sym#{sym_id}", line_num, col))
            elif kind == "INT_CONST":
                tokens.append(("NUM_INT", val, int(val), line_num, col))
            elif kind == "FLOAT_CONST":
                tokens.append(("NUM_FLOAT", val, float(val), line_num, col))
            elif kind == "STRING_LIT":
                tokens.append(("STRING", val, val[1:-1], line_num, col))
            elif kind == "CHAR_LIT":
                tokens.append(("CHAR", val, val[1:-1], line_num, col))
            elif kind.startswith("RELOP_"):
                op = kind.split("_")[1]
                tokens.append(("RELOP", val, op, line_num, col))
            elif kind == "MISMATCH":
                tokens.append(("LEXICAL_ERROR", val, f"Illegal char '{val}'", line_num, col))
            else:
                tokens.append((kind, val, val, line_num, col))

        return tokens


def main():
    print("=" * 80)
    print(" CIT 412: Chapter 3 - Section 3.5: Lex/Flex Scanner & Mini-C Tokenizer")
    print("=" * 80)

    sample_mini_c = """
    /* Mini-C Program demonstrating lexical analysis
       Author contact: student@university.edu
       Course Webpage: https://cse.university.edu/compiler
    */
    int factorial(int n) {
        if (n <= 1) {
            return 1;
        } else {
            return n * factorial(n - 1);
        }
    }

    int main() {
        int num = 5;
        float factor = 2.5e-1;
        // Compute result
        int ans = factorial(num);
        return 0;
    }
    """

    # 1. Word Count Demonstration
    wc_res = run_wc(sample_mini_c)
    print("\n--- 1. Lex 'wc' Tool Output ---")
    print(f"  Lines:      {wc_res['lines']}")
    print(f"  Words:      {wc_res['words']}")
    print(f"  Characters: {wc_res['characters']}")

    # 2. Pattern Extractor (Emails and URLs)
    emails, urls = extract_patterns(sample_mini_c)
    print("\n--- 2. Extracted Email Addresses & URLs ---")
    print(f"  Emails found: {emails}")
    print(f"  URLs found:   {urls}")

    # 3. Mini-C Lexical Analyzer
    lexer = MiniCLexer(sample_mini_c)
    tokens = lexer.tokenize()

    print("\n--- 3. Mini-C Token Stream (<Token_Name, Attribute_Value>) ---")
    print(f"{'Position':<10} | {'Token Name':<16} | {'Lexeme':<18} | {'Attribute'}")
    print("-" * 75)
    for tok_name, lexeme, attr, line, col in tokens:
        attr_display = str(attr) if attr is not None else "-"
        print(f"L{line:<3} C{col:<4} | {tok_name:<16} | {lexeme:<18} | {attr_display}")

    print("\n" + "=" * 75)
    print("                       SYMBOL TABLE")
    print("=" * 75)
    print(f"{'Entry ID':<10} | {'Identifier Name':<20} | {'First Seen':<15} | {'Occurrences'}")
    print("-" * 75)
    for name, info in lexer.symbol_table.items():
        print(f"{info['id']:<10} | {info['name']:<20} | Line {info['first_line']:<10} | {info['count']}")
    print("=" * 75)

if __name__ == "__main__":
    main()
