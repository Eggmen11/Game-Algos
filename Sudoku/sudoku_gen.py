import random
import copy

class SudokuBoard:
    difficulty_levels = {
        "Easy": 81 - random.randrange(30, 40),
        "Medium": 81 - random.randrange(25, 30),
        "Hard": 81 - random.randrange(20, 25),
        "Impossible": 81 - random.randrange(17, 20)
    }

    def __init__(self):
        self.board = [[None] * 9 for _ in range(9)]
        self.row_dict = [[False] * 10 for _ in range(9)]
        self.col_dict = [[False] * 10 for _ in range(9)]
        self.block_dict = [[False] * 10 for _ in range(9)]
        self.solved_board = None

    def is_valid(self, row, col, num):
        block_index = (row // 3) * 3 + (col // 3)
        return (not self.row_dict[row][num] and
                not self.col_dict[col][num] and
                not self.block_dict[block_index][num])

    def solve(self):
        for row in range(9):
            for col in range(9):
                if self.board[row][col] is None:
                    nums = list(range(1, 10))
                    random.shuffle(nums)
                    for num in nums:
                        if self.is_valid(row, col, num):
                            self.board[row][col] = num
                            self.row_dict[row][num] = True
                            self.col_dict[col][num] = True
                            self.block_dict[(row // 3) * 3 + (col // 3)][num] = True
                            if self.solve():
                                return True
                            self.board[row][col] = None
                            self.row_dict[row][num] = False
                            self.col_dict[col][num] = False
                            self.block_dict[(row // 3) * 3 + (col // 3)][num] = False
                    return False
        self.solved_board = copy.deepcopy(self.board)
        return True

    def generate_board(self):
        self.solve()

    def puzzle(self, difficulty):
        used = []
        while len(used) < SudokuBoard.difficulty_levels[difficulty]:
            row = random.randrange(0, 9)
            col = random.randrange(0, 9)
            if (row, col) not in used:
                self.board[row][col] = 0
                used.append((row, col))

    def find_incorrect(self, board):
        incorrect = []
        for row in range(9):
            for col in range(9):
                if board[row][col] != self.solved_board[row][col] and board[row][col] != 0:
                    incorrect.append((row, col))
        return incorrect
