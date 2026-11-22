"""
Master Runner for Chapter 3 Lab Problems
Course: CIT 412: Compiler Design and Automata Theory Sessional

Runs all 5 sections of Chapter 3:
1. Section 3.1: The Role of the Lexical Analyzer (Tokens, Lexemes, Attributes)
2. Section 3.2: Input Buffering with Sentinels
3. Section 3.3: Specification of Tokens & Regular Definitions
4. Section 3.4: Recognition of Tokens (Transition Diagrams / DFA)
5. Section 3.5: Lex/Flex Scanner & Mini-C Tokenizer
"""

import subprocess
import sys
import os

SCRIPTS = [
    ("Section 3.1: The Role of the Lexical Analyzer", "01_role_of_lexical_analyzer.py"),
    ("Section 3.2: Input Buffering with Sentinels", "02_input_buffering.py"),
    ("Section 3.3: Specification of Tokens & Regular Definitions", "03_specification_of_tokens.py"),
    ("Section 3.4: Recognition of Tokens (Transition Diagrams / DFA)", "04_recognition_of_tokens_dfa.py"),
    ("Section 3.5: Lex/Flex Scanner & Mini-C Tokenizer", "05_mini_c_lexical_analyzer.py")
]

def run_script(filename):
    curr_dir = os.path.dirname(os.path.abspath(__file__))
    script_path = os.path.join(curr_dir, filename)
    print("\n" + "#" * 80)
    print(f" EXECUTION: python {filename}")
    print("#" * 80)
    subprocess.run([sys.executable, script_path], check=True)

def main():
    print("=" * 80)
    print("   CIT 412: COMPILER DESIGN SESSIONAL - CHAPTER 3 SOLUTIONS")
    print("=" * 80)
    
    if len(sys.argv) > 1 and sys.argv[1].isdigit():
        idx = int(sys.argv[1]) - 1
        if 0 <= idx < len(SCRIPTS):
            run_script(SCRIPTS[idx][1])
            return
        else:
            print("Invalid section number.")
            return

    for title, script in SCRIPTS:
        run_script(script)

    print("\n" + "=" * 80)
    print(" All Chapter 3 lab problems executed successfully!")
    print("=" * 80)

if __name__ == "__main__":
    main()
