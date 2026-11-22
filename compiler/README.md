# CIT 412: Compiler Design and Automata Theory Sessional

This directory contains complete implementations and solutions for:
1. **Chapter 2 Lab Problems**:
   - 1) Syntax Tree (Concrete Parse Tree)
   - 2) Abstract Syntax Tree (AST)
   - 3) Infix to Postfix (Syntax-Directed Translation & Shunting-Yard Stack)
   - 4) Distinguishing Keyword from Identifier (Symbol Table Lookup)
   - 5) Removal of White Space and Comments (Lexical Preprocessor)
2. **Chapter 3 Lab Problems (from `Lab Problems on Chapter 03 Lexical Analysis.docx`)**:
   - Section 3.1: The Role of the Lexical Analyzer (Tokens, Lexemes, Attributes)
   - Section 3.2: Input Buffering with Sentinels (Buffer pairs, lookahead, retraction)
   - Section 3.3: Specification of Tokens & Regular Definitions (Prefixes, suffixes, regex)
   - Section 3.4: Recognition of Tokens via Transition Diagrams (DFA for ID, Num, Relop)
   - Section 3.5: Lex/Flex Scanner & Mini-C Tokenizer (wc, comment stripper, Mini-C Lexer, Flex `.l` file)

---

## Directory Structure

```
compiler/
├── chapter_2/
│   ├── 01_syntax_tree.py                # Problem 1: Concrete Syntax Tree generator
│   ├── 02_abstract_syntax_tree.py       # Problem 2: AST generator & evaluator
│   ├── 03_infix_to_postfix.py           # Problem 3: Dragon Book SDT + Stack trace
│   ├── 04_keyword_vs_identifier.py      # Problem 4: Keyword vs Identifier & Symbol table
│   ├── 05_removal_of_whitespace.py      # Problem 5: Whitespace & comments stripper
│   └── run_all_ch2.py                   # Master runner for Chapter 2
│
├── chapter_3/
│   ├── 01_role_of_lexical_analyzer.py   # Sec 3.1: Token/Lexeme/Attribute identification
│   ├── 02_input_buffering.py            # Sec 3.2: Double buffering & sentinels
│   ├── 03_specification_of_tokens.py    # Sec 3.3: String ops & regular definitions
│   ├── 04_recognition_of_tokens_dfa.py  # Sec 3.4: Transition diagram (DFA) simulation
│   ├── 05_mini_c_lexical_analyzer.py    # Sec 3.5: Mini-C lexer & wc tool
│   ├── mini_c.l                         # Flex specification file for Mini-C
│   └── run_all_ch3.py                   # Master runner for Chapter 3
│
├── sample_input.c                       # Sample C program for testing
├── main_runner.py                       # Unified test runner
└── README.md                            # Comprehensive lab manual & documentation
```

---

## How to Run

### 1. Run Everything at Once
```bash
python compiler/main_runner.py
```

### 2. Run Chapter 2 Problems
```bash
# Run all Chapter 2 problems:
python compiler/chapter_2/run_all_ch2.py

# Or run individual problems:
python compiler/chapter_2/01_syntax_tree.py
python compiler/chapter_2/02_abstract_syntax_tree.py
python compiler/chapter_2/03_infix_to_postfix.py
python compiler/chapter_2/04_keyword_vs_identifier.py
python compiler/chapter_2/05_removal_of_whitespace.py
```

### 3. Run Chapter 3 Lab Problems
```bash
# Run all Chapter 3 sections:
python compiler/chapter_3/run_all_ch3.py

# Or run individual sections:
python compiler/chapter_3/01_role_of_lexical_analyzer.py
python compiler/chapter_3/02_input_buffering.py
python compiler/chapter_3/03_specification_of_tokens.py
python compiler/chapter_3/04_recognition_of_tokens_dfa.py
python compiler/chapter_3/05_mini_c_lexical_analyzer.py
```

---

## Detailed Topic Explanations

### Chapter 2

#### 1) Syntax Tree (Parse Tree)
- **Concept**: A graphical representation of the derivation of a string according to a Context-Free Grammar (CFG).
- **Implementation**: Uses an LL(1) grammar for arithmetic expressions ($E \rightarrow T E'$, etc.) and builds a complete hierarchical tree showing non-terminals, terminals, and $\epsilon$-productions.
- **Output**: Visual ASCII tree representation and parenthesized LISP format.

#### 2) Abstract Syntax Tree (AST)
- **Concept**: A condensed syntax tree where interior nodes represent operators and leaf nodes represent operands. Syntactic grammar rules and grouping parentheses are omitted.
- **Implementation**: Class hierarchy (`NumNode`, `VarNode`, `BinOpNode`, `AssignNode`) constructed via recursive descent parser. Supports tree visualization, prefix/infix/postfix notation, and expression evaluation.

#### 3) Infix to Postfix Translation
- **Method 1: Dragon Book SDT**: Syntax-Directed Translation using semantic actions embedded into grammar productions (`rest -> + term { print('+') } rest`).
- **Method 2: Shunting-Yard Stack Algorithm**: Tracks operator precedence, associativity, and outputs a formatted table showing stack and output at each token step.

#### 4) Distinguishing Keyword from Identifier
- **Concept**: Both match the pattern `letter (letter | digit)*`.
- **Implementation**: Lexical analyzer extracts candidate words and performs an $O(1)$ hash table lookup in a reserved keyword table. If found, it emits a `KEYWORD` token; if not, it emits an `IDENTIFIER` token and registers it in the compiler's Symbol Table with occurrence count and line/column tracking.

#### 5) Removal of White Space and Comments
- **Concept**: Stripping superfluous characters before passing the code to syntactic analysis.
- **Nuance**: Spaces and comments inside string literals (`"..."`) or character constants (`'...'`) are strictly preserved.
- **Implementation**: Three levels of processing:
  1. Comment removal (`//` and `/* ... */`).
  2. Normalization of whitespace.
  3. Compiler minification (removing all whitespace except between consecutive alphanumerics).

---

### Chapter 3 (Lexical Analysis)

- **Section 3.1**: Token classification into `<token_name, attribute_value>`. Distinguishes tokens needing attribute values (identifiers, literals) from those that do not (keywords, punctuation).
- **Section 3.2**: Double Buffering simulation with `N`-sized buffer pairs and `EOF` sentinels, demonstrating forward pointer advance, buffer reload, and lookahead retraction.
- **Section 3.3**: String manipulation (prefixes, proper prefixes, suffixes, substrings, subsequences) and regular definitions (ordered vowels, ascending letters, C comments, chess moves).
- **Section 3.4**: Deterministic Finite Automaton (DFA) state machines simulating transition diagrams for identifiers, numbers (integer, float, scientific notation), and relational operators.
- **Section 3.5**: Full Mini-C Scanner generator, `wc` line/word/char counting tool, and a Flex (`mini_c.l`) specification file.
