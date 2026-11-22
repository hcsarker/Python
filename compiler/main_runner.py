"""
CIT 412: Compiler Design and Automata Theory Sessional
Unified Lab Runner for Chapter 2 and Chapter 3
"""

import sys
import os
import subprocess

def run_script(path):
    print("\n" + "=" * 80)
    print(f" Running: {path}")
    print("=" * 80)
    subprocess.run([sys.executable, path], check=True)

def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    ch2_runner = os.path.join(base_dir, "chapter_2", "run_all_ch2.py")
    ch3_runner = os.path.join(base_dir, "chapter_3", "run_all_ch3.py")

    print("=" * 80)
    print("  CIT 412: COMPILER DESIGN AND AUTOMATA THEORY SESSIONAL")
    print("=" * 80)
    print(" Select an option to execute:")
    print("   1. Run Chapter 2 Lab Problems (Syntax Tree, AST, Infix->Postfix, Keyword/ID, Whitespace)")
    print("   2. Run Chapter 3 Lab Problems (Sec 3.1 - 3.5: Lexical Analysis, Buffering, DFA, Mini-C)")
    print("   3. Run ALL (Chapter 2 + Chapter 3)")
    print("=" * 80)

    choice = sys.argv[1] if len(sys.argv) > 1 else None

    if choice == "1":
        run_script(ch2_runner)
    elif choice == "2":
        run_script(ch3_runner)
    elif choice == "3" or choice is None:
        print("\n>>> Running Chapter 2 Solutions...")
        run_script(ch2_runner)
        print("\n>>> Running Chapter 3 Solutions...")
        run_script(ch3_runner)
    else:
        print(f"Invalid option '{choice}'. Use 1, 2, or 3.")

if __name__ == "__main__":
    main()
