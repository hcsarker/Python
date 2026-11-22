"""
Master Runner for Chapter 2 Lab Problems
Course: CIT 412: Compiler Design and Automata Theory Sessional

Runs all 5 problems of Chapter 2:
1. Syntax tree
2. Abstract syntax tree
3. Infix to Postfix
4. Distinguishing keyword from identifier
5. Removal of white space
"""

import subprocess
import sys
import os

SCRIPTS = [
    ("1. Syntax Tree (Concrete Parse Tree)", "01_syntax_tree.py"),
    ("2. Abstract Syntax Tree (AST)", "02_abstract_syntax_tree.py"),
    ("3. Infix to Postfix (SDT & Stack)", "03_infix_to_postfix.py"),
    ("4. Distinguishing Keyword from Identifier", "04_keyword_vs_identifier.py"),
    ("5. Removal of White Space and Comments", "05_removal_of_whitespace.py")
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
    print("   CIT 412: COMPILER DESIGN SESSIONAL - CHAPTER 2 SOLUTIONS")
    print("=" * 80)
    
    if len(sys.argv) > 1 and sys.argv[1].isdigit():
        idx = int(sys.argv[1]) - 1
        if 0 <= idx < len(SCRIPTS):
            run_script(SCRIPTS[idx][1])
            return
        else:
            print("Invalid problem number.")
            return

    for title, script in SCRIPTS:
        run_script(script)

    print("\n" + "=" * 80)
    print(" All Chapter 2 problems executed successfully!")
    print("=" * 80)

if __name__ == "__main__":
    main()
