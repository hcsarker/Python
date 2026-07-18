"""Solve N-Queens using backtracking (example with n=4 from PDF)."""
from __future__ import annotations


def is_safe(board: list[int], row: int, col: int) -> bool:
    for i in range(row):
        if board[i] == col or abs(board[i] - col) == row - i:
            return False
    return True


def solve_nqueens(n: int) -> list[list[int]]:
    solutions: list[list[int]] = []
    board = [-1] * n

    def backtrack(r: int) -> None:
        if r == n:
            solutions.append(board.copy())
            return
        for c in range(n):
            if is_safe(board, r, c):
                board[r] = c
                backtrack(r + 1)
                board[r] = -1

    backtrack(0)
    return solutions


if __name__ == "__main__":
    print("4-Queens solutions:", solve_nqueens(4))
