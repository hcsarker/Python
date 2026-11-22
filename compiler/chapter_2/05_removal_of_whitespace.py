"""
Chapter 2 - Problem 5: Removal of White Space and Comments
Course: CIT 412: Compiler Design and Automata Theory Sessional

This program demonstrates lexical preprocessing:
1. Removal and compression of whitespace (spaces, tabs, newlines).
2. Removal of single-line (// ...) and multi-line (/* ... */) comments.
3. CRITICAL COMPILER RULE: Preserving whitespace and comments inside string/char literals!
4. Displaying statistical comparison (raw characters, stripped characters, reduction %).
"""

import re

class SourcePreprocessor:
    def __init__(self, source_code: str):
        self.raw_source = source_code

    def remove_comments(self, code: str) -> str:
        """
        Removes both single-line and multi-line comments while safely ignoring
        comment symbols located inside string literals.
        """
        result = []
        i = 0
        n = len(code)
        in_string = False
        string_char = ''

        while i < n:
            ch = code[i]

            # Handle string and character literals
            if not in_string and (ch == '"' or ch == "'"):
                in_string = True
                string_char = ch
                result.append(ch)
                i += 1
                continue
            elif in_string:
                result.append(ch)
                if ch == '\\' and i + 1 < n:
                    # Escaped character inside string (e.g. \", \')
                    i += 1
                    result.append(code[i])
                elif ch == string_char:
                    in_string = False
                i += 1
                continue

            # Outside strings: check for comments
            if ch == '/' and i + 1 < n:
                next_ch = code[i + 1]
                if next_ch == '/':
                    # Single-line comment: skip until newline
                    i += 2
                    while i < n and code[i] != '\n':
                        i += 1
                    continue
                elif next_ch == '*':
                    # Multi-line comment: skip until */
                    i += 2
                    while i + 1 < n and not (code[i] == '*' and code[i + 1] == '/'):
                        i += 1
                    i += 2 # Skip * and /
                    continue

            result.append(ch)
            i += 1

        return "".join(result)

    def remove_unnecessary_whitespace(self, code: str) -> str:
        """
        Compresses redundant whitespace (multiple spaces/tabs into one)
        and trims empty lines, preserving literal strings.
        """
        code_without_comments = self.remove_comments(code)
        
        result = []
        i = 0
        n = len(code_without_comments)
        in_string = False
        string_char = ''

        while i < n:
            ch = code_without_comments[i]

            if not in_string and (ch == '"' or ch == "'"):
                in_string = True
                string_char = ch
                result.append(ch)
                i += 1
                continue
            elif in_string:
                result.append(ch)
                if ch == '\\' and i + 1 < n:
                    i += 1
                    result.append(code_without_comments[i])
                elif ch == string_char:
                    in_string = False
                i += 1
                continue

            # Outside string: normalize whitespace
            if ch.isspace():
                # If last added char is not space, add single space
                if result and not result[-1].isspace():
                    result.append(' ')
                i += 1
                continue

            result.append(ch)
            i += 1

        return "".join(result).strip()

    def minify_code(self, code: str) -> str:
        """
        Extreme whitespace removal: removes all whitespace except where necessary
        to separate two alphanumeric identifiers/keywords (e.g. 'int x' needs space,
        but 'x = y + 1;' becomes 'x=y+1;').
        """
        cleaned = self.remove_comments(code)
        result = []
        i = 0
        n = len(cleaned)
        in_string = False
        string_char = ''

        def is_word_char(c):
            return c.isalnum() or c == '_'

        while i < n:
            c = cleaned[i]

            if not in_string and (c == '"' or c == "'"):
                in_string = True
                string_char = c
                result.append(c)
                i += 1
                continue
            elif in_string:
                result.append(c)
                if c == '\\' and i + 1 < n:
                    i += 1
                    result.append(cleaned[i])
                elif c == string_char:
                    in_string = False
                i += 1
                continue

            if c.isspace():
                # Peek forward to next non-space char
                j = i + 1
                while j < n and cleaned[j].isspace():
                    j += 1
                if result and j < n:
                    prev_char = result[-1]
                    next_char = cleaned[j]
                    # If both are alphanumeric, we MUST keep a single space: 'int a'
                    if is_word_char(prev_char) and is_word_char(next_char):
                        result.append(' ')
                i = j
                continue

            result.append(c)
            i += 1

        return "".join(result)


def main():
    print("=" * 75)
    print(" CIT 412: Chapter 2 - Problem 5: Removal of White Space and Comments")
    print("=" * 75)

    sample_c_code = """
    #include <stdio.h>

    /* 
       Multi-line comment explaining 
       the Euclidean algorithm 
    */
    int gcd(int a,   int b) {
        // Loop until remainder is zero
        while (  b  !=  0  ) {
            int t   =   b ;
            b       =   a   %   b ;
            a       =   t ;
        }
        return a;
    }

    int main() {
        // String literal with spaces that MUST NOT be removed:
        char message[] = "Result of gcd(12, 18)  is:   ";
        int res = gcd( 12 ,  18 );
        printf( "%s %d\\n" , message , res );
        return 0;
    }
    """

    preprocessor = SourcePreprocessor(sample_c_code)

    print("\n--- 1. Original Source Code ---")
    print(sample_c_code.strip())

    cleaned_comments = preprocessor.remove_comments(sample_c_code)
    print("\n--- 2. Source Code after Removing Comments ---")
    print(cleaned_comments.strip())

    compressed_ws = preprocessor.remove_unnecessary_whitespace(sample_c_code)
    print("\n--- 3. Source Code with Normalized Whitespace (Single-line normalized) ---")
    print(compressed_ws)

    minified = preprocessor.minify_code(sample_c_code)
    print("\n--- 4. Fully Minified / Stripped Whitespace Code (Compiler Input Ready) ---")
    print(minified)

    # Statistics
    orig_len = len(sample_c_code)
    min_len = len(minified)
    reduction = ((orig_len - min_len) / orig_len) * 100

    print("\n" + "=" * 75)
    print("                       PREPROCESSING METRICS")
    print("=" * 75)
    print(f" Original character count: {orig_len}")
    print(f" Minified character count: {min_len}")
    print(f" Characters eliminated:    {orig_len - min_len} ({reduction:.1f}% reduction)")
    print(" Notice that strings like '\"Result of gcd(12, 18)  is:   \"' retained all spaces!")
    print("=" * 75)

if __name__ == "__main__":
    main()
