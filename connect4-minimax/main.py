from board import Board
from minimax import minimax, minimax_with_prune


def check_end(board, player):
    # Check if the game is over after the player's move
    if board.is_terminal_state():
        if board.is_draw:
            print("DRAW")
        else:
            print(f"{player} HAS WON")
        return True
    return False

def validate_and_make_move(board, move, player):
        try:
            if not board.make_move(int(move), player):
                print("Invalid move. Try again.")
                return False
        except:
            print("Invalid input")
            return False
        
        return True

def make_ai_move(board, depth, is_first, log=True):
    player = "p1" if is_first else "p2"

    if log: print("AI is thinking...")
    pos_eval, best_move = minimax_with_prune(board, depth, is_first)

    if log: print(f"Pos eval {pos_eval}")

    board.make_move(best_move + 1, player)
    print(f"AI chose move: {best_move + 1}")
    board.pretty_print()



# Main game function
def p_v_p():
    board1 = Board(2,2)
    player = "p1"
    while True:
        move = input("Move: ")
        if not(board1.make_move(int(move), player)):
            continue

        board1.pretty_print()
        print(board1.row_table)
        if board1.is_terminal_state():
            if board1.is_draw: 
                print("DRAW")
                break

            print(f"{player} HAS WON")
            break
        
        player = "p2" if player == "p1" else "p1"

def p_v_ai():
    board2 = Board()
    board2.pretty_print()
    player = "p1"  # Human player
    ai = "p2"  # AI

    while True:
        # Player's turn
        player_move = input("Move: ")
        if not validate_and_make_move(board2, player_move, player): continue
        board2.pretty_print()
        if check_end(board2, player): break
        
        make_ai_move(board2, 7, False, True)
        if check_end(board2, ai): break
        
def ai_v_ai():
    board3 = Board()
    while True:
        make_ai_move(board3, 5, True)
        if check_end(board3, "NEW AI"): break

        make_ai_move(board3, 7, False, True)
        if check_end(board3, "Old AI"): break

if __name__ == "__main__":
    p_v_ai()