from board import Board

def minimax(position, depth, is_maximizing, old=False):
    if depth == 0 or position.is_terminal_state():
        return position.eval_board(old), None

    best_move = None
    
    if is_maximizing:
        max_eval = float("-inf")
        for move, value in position.row_table.items():
            if value >= 0:
                position.make_move(move+1, "p1")
                cur_eval, _ = minimax(position, depth-1, False)
                position.undo_move()

                if cur_eval >= max_eval:
                    best_move = move
                    max_eval = cur_eval

        return max_eval, best_move

    else:
        min_eval = float("inf")

        for move, value in position.row_table.items():
            if value >= 0:
                position.make_move(move+1, "p2")
                cur_eval, _ = minimax(position, depth-1, True)
                position.undo_move()

                if cur_eval <= min_eval:
                    best_move = move
                    min_eval = cur_eval

        return min_eval, best_move


def minimax_with_prune(position, depth, is_maximizing, alpha=float("-inf"), beta=float("inf"), old=False):
    if depth == 0 or position.is_terminal_state():
        return position.eval_board(old), None

    best_move = None

    if is_maximizing:
        max_eval = float("-inf")
        for move, value in position.row_table.items():
            if value >= 0:  
                position.make_move(move + 1, "p1")
                cur_eval, _ = minimax_with_prune(position, depth - 1, False, alpha, beta, old)
                position.undo_move() 

                if cur_eval > max_eval:
                    best_move = move
                    max_eval = cur_eval

                alpha = max(alpha, cur_eval)
                if beta <= alpha:
                    break

        return max_eval, best_move if best_move is not None else 0

    else:
        min_eval = float("inf")
        for move, value in position.row_table.items():
            if value >= 0: 
                position.make_move(move + 1, "p2") 
                cur_eval, _ = minimax_with_prune(position, depth - 1, True, alpha, beta, old)
                position.undo_move()

                if cur_eval < min_eval:
                    best_move = move
                    min_eval = cur_eval

                beta = min(beta, cur_eval) 
                if beta <= alpha:
                    break

        return min_eval, best_move if best_move is not None else 0

