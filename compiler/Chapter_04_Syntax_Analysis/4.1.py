# Section 4.1 - The Role of the Parser
# Problems: simple syntax checking, parse-tree display, and error recovery.
# Run: python 4.1.py

def check_statement(statement):
    """A tiny example language: every statement must look like name = number ;"""
    statement = statement.strip()
    if not statement.endswith(";"):
        return False, "Missing semicolon"

    body = statement[:-1].strip()
    parts = body.split("=")

    if len(parts) != 2:
        return False, "Expected one '=' sign"

    name, value = parts[0].strip(), parts[1].strip()
    if not name.isidentifier():
        return False, "Invalid variable name"

    if not value.isdigit():
        return False, "Value must be an integer"

    return True, "Valid statement"


def show_parse_tree(statement):
    """Display a small parse tree for: id = number ;"""
    body = statement.strip().rstrip(";")
    name, value = body.split("=")
    print("Statement")
    print("|-- Identifier:", name.strip())
    print("|-- =")
    print("|-- Number:", value.strip())
    print("`-- ;")


def main():
    print("SECTION 4.1 - PARSER")
    print("Example grammar: statement -> id = number ;")
    line = input("Enter statements separated by ';' (example: x=10; y=20;): ")

    # Split at semicolons; keep each statement independent.
    pieces = [p.strip() for p in line.split(";") if p.strip()]

    if not pieces:
        print("No statement entered.")
        return

    for piece in pieces:
        statement = piece + ";"
        ok, message = check_statement(statement)
        print(f"\n{statement} -> {message}")

        if ok:
            show_parse_tree(statement)
        else:
            # Panic-mode demonstration: skip the bad statement and continue.
            print("Recovery: skip this statement and check the next one.")


if __name__ == "__main__":
    main()
