"""
Chapter 3 - Section 3.2: Input Buffering with Sentinels
Course: CIT 412: Compiler Design and Automata Theory Sessional

Textbook Reference: Dragon Book (Aho, Lam, Sethi, Ullman), Section 3.2
Focus:
1. Multi-buffer scheme (Buffer Pairs of size N with EOF sentinels).
2. Pointer management: `lexeme_begin` and `forward`.
3. Reducing two-test overhead per character to a single test via sentinel.
4. Handling buffer reloading and lookahead retraction (forward--).
"""

from typing import Optional, List, Tuple
import io

EOF = '\0'  # Sentinel character representing buffer boundary or file end

class DoubleBufferReader:
    """
    Simulates the Dragon Book Section 3.2 double buffer with sentinels.
    Buffer structure:
    [ Buffer 1 (size N) | EOF ] [ Buffer 2 (size N) | EOF ]
    """
    def __init__(self, stream: io.StringIO, buffer_size: int = 16):
        self.stream = stream
        self.N = buffer_size
        # Total size: 2 * (N + 1)
        # Buffer 1 spans 0 .. N (index N is sentinel)
        # Buffer 2 spans N+1 .. 2N+1 (index 2N+1 is sentinel)
        self.buf_size = 2 * (self.N + 1)
        self.buffer = [EOF] * self.buf_size
        
        self.lexeme_begin = 0
        self.forward = 0
        self.file_exhausted = False
        
        # Initially reload first buffer
        self._reload_buffer_1()

    def _reload_buffer_1(self):
        chars = self.stream.read(self.N)
        for i in range(self.N):
            if i < len(chars):
                self.buffer[i] = chars[i]
            else:
                self.buffer[i] = EOF
                self.file_exhausted = True
        self.buffer[self.N] = EOF  # Sentinel at end of buffer 1

    def _reload_buffer_2(self):
        chars = self.stream.read(self.N)
        offset = self.N + 1
        for i in range(self.N):
            if i < len(chars):
                self.buffer[offset + i] = chars[i]
            else:
                self.buffer[offset + i] = EOF
                self.file_exhausted = True
        self.buffer[offset + self.N] = EOF  # Sentinel at end of buffer 2

    def next_char(self) -> str:
        """
        Dragon Book Figure 3.14: Algorithm for reading next char with sentinels.
        Single test: if *forward == EOF, check which buffer end or file end.
        """
        c = self.buffer[self.forward]
        self.forward += 1

        if c == EOF:
            # Check if at end of buffer 1
            if self.forward - 1 == self.N:
                self._reload_buffer_2()
                self.forward = self.N + 1
                c = self.buffer[self.forward]
                self.forward += 1
            # Check if at end of buffer 2
            elif self.forward - 1 == (2 * self.N + 1):
                self._reload_buffer_1()
                self.forward = 0
                c = self.buffer[self.forward]
                self.forward += 1
            else:
                # Real end of input
                c = EOF
                self.forward -= 1  # Stay at EOF

        return c

    def retract(self, steps: int = 1):
        """Retracts forward pointer when lookahead overshoots."""
        for _ in range(steps):
            self.forward -= 1
            # Adjust if jumping backwards across buffer boundaries
            if self.forward == self.N:
                self.forward -= 1
            elif self.forward < 0:
                self.forward = 2 * self.N

    def commit_lexeme(self) -> str:
        """Extracts the accepted lexeme and aligns lexeme_begin to forward."""
        lexeme_chars = []
        curr = self.lexeme_begin
        while curr != self.forward:
            if curr != self.N and curr != (2 * self.N + 1):
                if self.buffer[curr] != EOF:
                    lexeme_chars.append(self.buffer[curr])
            curr = (curr + 1) % self.buf_size
        
        self.lexeme_begin = self.forward
        return "".join(lexeme_chars)

    def print_buffer_state(self):
        """Prints visual diagram of current buffer pair."""
        b1 = "".join(c if c != EOF and not c.isspace() else ('·' if c.isspace() else '⚑') for c in self.buffer[:self.N])
        b2 = "".join(c if c != EOF and not c.isspace() else ('·' if c.isspace() else '⚑') for c in self.buffer[self.N+1:2*self.N+1])
        print(f"  [Buf 1: {b1} | EOF] [Buf 2: {b2} | EOF] | forward={self.forward}, begin={self.lexeme_begin}")


def simulate_scanning():
    print("=" * 80)
    print(" CIT 412: Chapter 3 - Section 3.2: Input Buffering with Sentinels")
    print("=" * 80)

    source = "int count = 100; while (count > 0) count = count - 1;"
    print(f"Source Stream: \"{source}\" (Length: {len(source)} chars)")
    print("Buffer Size N = 16 (Total double-buffer slots with sentinels = 34)\n")

    reader = DoubleBufferReader(io.StringIO(source), buffer_size=16)

    tokens = []
    step = 1

    while True:
        # Skip spaces
        c = reader.next_char()
        while c.isspace():
            reader.commit_lexeme()
            c = reader.next_char()

        if c == EOF:
            break

        # Identifier or Keyword
        if c.isalpha() or c == '_':
            while True:
                c = reader.next_char()
                if not (c.isalnum() or c == '_'):
                    # Lookahead overshot! Retract one position
                    reader.retract(1)
                    break
            lexeme = reader.commit_lexeme()
            tokens.append(("ID_OR_KW", lexeme))
            print(f"Step {step:02d}: Recognized ID/KW '{lexeme}' -> Retracted 1 char")
            reader.print_buffer_state()
            step += 1
            continue

        # Number
        if c.isdigit():
            while True:
                c = reader.next_char()
                if not c.isdigit():
                    reader.retract(1)
                    break
            lexeme = reader.commit_lexeme()
            tokens.append(("NUM", lexeme))
            print(f"Step {step:02d}: Recognized NUMBER '{lexeme}' -> Retracted 1 char")
            reader.print_buffer_state()
            step += 1
            continue

        # Relational / Assignment
        if c in ('<', '>', '=', '!'):
            next_c = reader.next_char()
            if next_c == '=':
                lexeme = reader.commit_lexeme()
                tokens.append(("OP", lexeme))
            else:
                reader.retract(1)
                lexeme = reader.commit_lexeme()
                tokens.append(("OP", lexeme))
            print(f"Step {step:02d}: Recognized OP '{lexeme}'")
            step += 1
            continue

        # Single char delimiters / operators
        lexeme = reader.commit_lexeme()
        tokens.append(("PUNCT", lexeme))
        print(f"Step {step:02d}: Recognized PUNCT '{lexeme}'")
        step += 1

    print("\n" + "=" * 80)
    print(" Recognized Token Stream:")
    for kind, lexeme in tokens:
        print(f"  <{kind}, '{lexeme}'>", end=" ")
    print("\n" + "=" * 80)

if __name__ == "__main__":
    simulate_scanning()
