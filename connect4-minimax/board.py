from colorama import Fore, Back, Style

# Connect-4 board class
class Board():
    def __init__(self, width=7, height=6):
        self.width = width
        self.height = height
        self.p1_char, self.p2_char, self.empty_char = "o", "x", "#"
        self.board = [[self.empty_char] * width for _ in range(height)]
        self.row_table = {i:height-1 for i in range(width)}
        self.move_list = []
        self.dirs = {"row" : (0, 1), "col": (1, 0), "diag1": (1, 1), "diag2": (1, -1)}
        self.is_draw = False

    # pretty print board
    def pretty_print(self):
        # Get coordinates of the last move
        move_made = bool(len(self.move_list))
        if move_made:
            y, x, _ = self.move_list[-1]  # Assuming move_list contains (y, x, other_info)

        for i in range(self.height):
            print(f"{self.height - i} |", end="")  # Print row numbers
            for j in range(self.width):
                piece = self.board[i][j]

                # Highlight the last move with a cyan background
                if move_made and i == y and j == x:
                    if piece == "x":
                        print(Back.LIGHTWHITE_EX + Fore.RED + piece + Style.RESET_ALL, end="|")
                    elif piece == "o":
                        print(Back.LIGHTWHITE_EX + Fore.YELLOW + piece + Style.RESET_ALL, end="|")
                    else:
                        print(Back.CYAN + " " + Style.RESET_ALL, end="|")
                else:
                    # Normal printing for other cells
                    if piece == "x":
                        print(Fore.RED + piece + Style.RESET_ALL, end="|")
                    elif piece == "o":
                        print(Fore.YELLOW + piece + Style.RESET_ALL, end="|")
                    else:
                        print(" ", end="|")  # Empty cell

            print()  

        # Print column numbers
        print("  ", end="")  # Indent for column numbers
        for j in range(self.width):
            print(f" {j+1}", end="")
        print() 


    def make_move(self, col, player):
        col-=1
        if col >= self.width or col < 0:
            print("Invalid move")
            return False

        move_char = self.p1_char if player == "p1" else self.p2_char
        row = self.row_table[col]

        if row < 0:
            print("Invalid move")
            return False
        
        self.board[row][col] = move_char
        self.move_list.append((row, col, move_char))
        self.row_table[col] = row - 1
        return True


    def undo_move(self, move=None):
        # If the move to undo is not specified it defaults to the last move
        if not move:
            move = self.move_list[-1]
        row, col, piece = move
        self.board[row][col] = self.empty_char
        self.move_list.pop()
        self.row_table[col] = self.row_table[col] + 1
        self.draw = False


    def eval_board(self, old=False):
        # Pos - first player (o), Neg - second player - (x)
        end_status = self.is_terminal_state()
        if end_status:
            if end_status == "draw": return 0
            if end_status == "o": return float("inf")
            if end_status == "x": return float("-inf")

        return self.get_board_heuristic() if not old else self.get_board_heuristic_old()
    

    def get_board_heuristic_old(self):
        # Implement points based on wher the pieces are places - more middle more points
        pos_eval, cont_eval, total_eval = 0, 0, 0
        mid_h = (self.height-1) / 2
        mid_w = (self.width-1) / 2
        for row in range(self.height):
            for col in range(self.width):
                row_piece = self.board[row][col]

                pos_value = ((mid_w+1) - abs(mid_w - col)) * ((mid_h+1) - abs(mid_h - row))
                if row_piece == "o": pos_eval += pos_value
                elif row_piece == "x": pos_eval -= pos_value

        total_eval = pos_eval # add more heuristics
        return total_eval

    def get_board_heuristic(self):
        # Implement points based on where the pieces are placed - more middle more points
        pos_eval, cont_eval, total_eval = 0, 0, 0
        mid_h = (self.height - 1) / 2
        mid_w = (self.width - 1) / 2

        # Function to evaluate a window of 4 cells
        def evaluate_window(window):
            count_o = window.count(self.p1_char)  # Player 1 pieces
            count_x = window.count(self.p2_char)  # Player 2 pieces
            count_empty = window.count(self.empty_char)

            # Check if it's a potential opportunity for Player 1 or Player 2
            if count_o == 3 and count_empty == 1:
                return 50  # Favorable for Player 1
            elif count_x == 3 and count_empty == 1:
                return -50  # Favorable for Player 2
            return 0

        # Evaluate rows
        for row in range(self.height):
            for col in range(self.width):
                row_piece = self.board[row][col]

                # Positional evaluation
                pos_value = ((mid_w + 1) - abs(mid_w - col)) * ((mid_h + 1) - abs(mid_h - row))
                if row_piece == self.p1_char:
                    pos_eval += pos_value
                elif row_piece == self.p2_char:
                    pos_eval -= pos_value

                # Sliding window for rows
                if col <= self.width - 4:  # Ensure window is within bounds
                    window = self.board[row][col:col + 4]
                    cont_eval += evaluate_window(window)

        # Evaluate columns
        for col in range(self.width):
            for row in range(self.height - 3):  # Ensure window is within bounds
                window = [self.board[row + i][col] for i in range(4)]  # Extract vertical window
                cont_eval += evaluate_window(window)

        # Evaluate diagonals
        # Top-left to bottom-right
        for row in range(self.height - 3):
            for col in range(self.width - 3):
                window = [self.board[row + i][col + i] for i in range(4)]  # Extract diagonal window
                cont_eval += evaluate_window(window)

        # Top-right to bottom-left
        for row in range(self.height - 3):
            for col in range(3, self.width):
                window = [self.board[row + i][col - i] for i in range(4)]  # Extract anti-diagonal window
                cont_eval += evaluate_window(window)

        # Combine positional and continuation evaluations
        total_eval = pos_eval + cont_eval
        return total_eval

    # Returns False if it is not, "draw" what it is a draw, appropriate char if there is a winner
    def is_terminal_state(self):
        if len(self.move_list) < 3:
            return False

        last_move = self.move_list[-1]
        last_y, last_x, char = last_move

        for direction in self.dirs.keys():
            count = self._count_in_direction(last_x, last_y, direction)
            if count >= 4:
                return char
        
        if len(self.move_list) == (self.width * self.height):
            self.is_draw = True
            return "Draw"
        
        return False


    def _count_in_direction(self, x, y, d):
        dy, dx = self.dirs[d]
        piece = self.board[y][x]
        count = 1
        go_f, go_b = True, True
        for i in range(1, 4):
            if (not go_b and not go_f):
                break
            # forward and back
            f_nx = x + i*dx
            f_ny = y + i*dy
            b_ny = y - i*dy
            b_nx = x - i*dx

            if go_f and (0 <= f_nx < self.width) and (0 <= f_ny < self.height) and self.board[f_ny][f_nx] == piece:
                count += 1
            else:
                go_f = False

            if go_b and (0 <= b_nx < self.width) and (0 <= b_ny < self.height) and self.board[b_ny][b_nx] == piece:
                count += 1
            else:
                go_b = False

        return count
