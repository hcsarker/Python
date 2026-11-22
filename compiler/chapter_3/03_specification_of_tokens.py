"""
Chapter 3 - Section 3.3: Specification of Tokens & Regular Expressions
Course: CIT 412: Compiler Design and Automata Theory Sessional

Textbook Reference: Dragon Book (Aho, Lam, Sethi, Ullman), Section 3.3
Covers:
Part 1: String Operations (Prefixes, Suffixes, Substrings, Subsequences)
Part 2: Regular Definitions & Validations:
  - Strings containing the 5 vowels in alphabetical order
  - Lowercase letters in ascending lexicographical order
  - C-style comments without nested conflicts
  - Digits with no repeated digits or at most one repeated digit
  - Binary strings over {a, b} avoiding substring 'abb'
  - Chess moves in informal algebraic/descriptive notation
"""

import re
from typing import List, Set

# ==============================================================================
# Part 1: String Operations
# ==============================================================================
def get_prefixes(s: str) -> List[str]:
    """Returns all prefixes including empty string ε."""
    return [s[:i] for i in range(len(s) + 1)]

def get_proper_prefixes(s: str) -> List[str]:
    """Returns proper prefixes (excludes ε and s itself)."""
    return [s[:i] for i in range(1, len(s))]

def get_suffixes(s: str) -> List[str]:
    """Returns all suffixes including empty string ε."""
    return [s[i:] for i in range(len(s) + 1)]

def get_proper_suffixes(s: str) -> List[str]:
    """Returns proper suffixes (excludes ε and s itself)."""
    return [s[i:] for i in range(1, len(s))]

def get_substrings(s: str) -> List[str]:
    """Returns all unique substrings."""
    res = set()
    for i in range(len(s)):
        for j in range(i + 1, len(s) + 1):
            res.add(s[i:j])
    return ["ε"] + sorted(list(res), key=lambda x: (len(x), x))

def get_subsequences(s: str) -> List[str]:
    """Returns all unique subsequences (obtained by deleting zero or more characters)."""
    n = len(s)
    res = set()
    for i in range(1 << n):
        sub = "".join(s[j] for j in range(n) if (i & (1 << j)))
        res.add(sub)
    return ["ε" if x == "" else x for x in sorted(list(res), key=lambda x: (len(x), x))]


# ==============================================================================
# Part 2: Dragon Book Regular Definitions & Validations
# ==============================================================================

def validate_vowels_in_order(s: str) -> bool:
    """
    Regex: ^[^aeiou]*a[^aeiou]*e[^aeiou]*i[^aeiou]*o[^aeiou]*u[^aeiou]*$
    Checks if string contains all 5 vowels in strict alphabetical order.
    """
    pattern = r"^[^aeiou]*a[^aeiou]*e[^aeiou]*i[^aeiou]*o[^aeiou]*u[^aeiou]*$"
    return bool(re.fullmatch(pattern, s, re.IGNORECASE))

def validate_ascending_letters(s: str) -> bool:
    """
    Checks if characters in lowercase string are in strictly ascending lexicographic order:
    e.g. 'abcfz' is valid, 'abcb' is not.
    """
    if not s or not s.islower() or not s.isalpha():
        return False
    return all(ord(s[i]) < ord(s[i+1]) for i in range(len(s) - 1))

def validate_c_comment(s: str) -> bool:
    r"""
    Regex for C-style comment:
    Pattern: /\*([^*]|\*+[^*/])*\*+/
    Matches /* ... */ correctly without internal nesting conflicts.
    """
    pattern = r"^/\*([^*]|\*+[^*/])*\*+/$"
    return bool(re.fullmatch(pattern, s))

def validate_no_repeated_digits(s: str) -> bool:
    """Checks if string consists of digits with no repeated digit (all unique)."""
    return s.isdigit() and len(s) == len(set(s))

def validate_at_most_one_repeated_digit(s: str) -> bool:
    """Checks if string consists of digits with at most one repeated digit."""
    if not s.isdigit():
        return False
    counts = {}
    for d in s:
        counts[d] = counts.get(d, 0) + 1
    repeated_count = sum(1 for c in counts.values() if c > 1)
    return repeated_count <= 1

def validate_avoiding_substring_abb(s: str) -> bool:
    """
    Regular Expression for strings over {a, b} containing NO 'abb' substring:
    b*(a+b?)* or b*(a|ba)*
    """
    if not all(c in 'ab' for c in s):
        return False
    return "abb" not in s

def validate_chess_move(s: str) -> bool:
    """
    Informal / descriptive chess moves:
    e.g. 'P-K4', 'N-KB3', 'KBP*QN', 'O-O', 'O-O-O', 'b-n5'
    Piece/Descriptor: [KQRBNP]+ (e.g. P, N, KBP, QN)
    Separator: - (moves to) or x / * (captures)
    Target: [KQRBNP]+[1-8]? or algebraic like e4, cxd4
    """
    pattern = r"^([KQRBNP]+[1-8]?[-x*][KQRBNP]+[1-8]?|O-O(-O)?|[a-h][1-8]|[a-h]x[a-h][1-8])$"
    return bool(re.fullmatch(pattern, s, re.IGNORECASE))


def main():
    print("=" * 80)
    print(" CIT 412: Chapter 3 - Section 3.3: Specification of Tokens & Regular Definitions")
    print("=" * 80)

    # 1. String Operations on 'banana'
    test_word = "ban"
    print(f"\n[Part 1: String Operations for word: '{test_word}']")
    print(f"  Length:           {len(test_word)}")
    print(f"  Prefixes:         {get_prefixes(test_word)}")
    print(f"  Proper Prefixes:  {get_proper_prefixes(test_word)}")
    print(f"  Suffixes:         {get_suffixes(test_word)}")
    print(f"  Proper Suffixes:  {get_proper_suffixes(test_word)}")
    print(f"  Substrings ({len(get_substrings(test_word))}): {get_substrings(test_word)}")
    print(f"  Subsequences ({len(get_subsequences(test_word))}): {get_subsequences(test_word)}")

    # 2. Regular Definitions Demonstrations
    print("\n[Part 2: Regular Definitions & Validations]")
    
    # 2.1 Five vowels in alphabetical order
    vowel_tests = ["abstemious", "facetious", "arsenious", "apple", "aeiou", "uoiea"]
    print("\n2.1 Five vowels in alphabetical order (^[^aeiou]*a[^aeiou]*e[^aeiou]*i[^aeiou]*o[^aeiou]*u[^aeiou]*$):")
    for w in vowel_tests:
        print(f"  '{w}': {'MATCH' if validate_vowels_in_order(w) else 'NO MATCH'}")

    # 2.2 Ascending letters
    asc_tests = ["abc", "aegz", "abcb", "zyx"]
    print("\n2.2 Letters in strictly ascending order:")
    for w in asc_tests:
        print(f"  '{w}': {'VALID' if validate_ascending_letters(w) else 'INVALID'}")

    # 2.3 C-style comment
    comment_tests = ["/* simple comment */", "/* multi\nline\n* comment */", "/* comment * with * stars */", "/* unterminated"]
    print("\n2.3 C-style comments (regex: /\\*([^*]|\\*+[^*/])*\\*+/):")
    for c in comment_tests:
        display_c = c.replace('\n', '\\n')
        print(f"  '{display_c}': {'VALID COMMENT' if validate_c_comment(c) else 'INVALID'}")

    # 2.4 Digits with repeat restrictions
    digit_tests = ["12345", "11234", "11223", "98760"]
    print("\n2.4 Digits repeat restrictions:")
    for d in digit_tests:
        no_rep = validate_no_repeated_digits(d)
        at_most_one = validate_at_most_one_repeated_digit(d)
        print(f"  '{d}': No repeats? {no_rep} | At most 1 repeated digit? {at_most_one}")

    # 2.5 Strings over {a, b} avoiding 'abb'
    ab_tests = ["aabab", "ababa", "aabb", "abb", "baabaa", "b"]
    print("\n2.5 Strings over {a, b} avoiding substring 'abb':")
    for s in ab_tests:
        print(f"  '{s}': {'ACCEPTED' if validate_avoiding_substring_abb(s) else 'REJECTED'}")

    # 2.6 Informal chess moves
    chess_tests = ["P-K4", "N-KB3", "KBP*QN", "O-O", "e4", "INVALID_MOVE_XYZ"]
    print("\n2.6 Informal chess notation moves:")
    for m in chess_tests:
        print(f"  '{m}': {'VALID CHESS MOVE' if validate_chess_move(m) else 'INVALID'}")

    print("\n" + "=" * 80)

if __name__ == "__main__":
    main()
