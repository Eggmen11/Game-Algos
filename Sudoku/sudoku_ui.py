import pygame
import sys
from sudoku_gen import SudokuBoard

# Constants
WIDTH, HEIGHT = 540, 600
GRID_SIZE = 9
CELL_SIZE = WIDTH // GRID_SIZE
BLOCK_SIZE = 3

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
ORANGE = (255, 165, 0)
BLUE = (173, 216, 230)
RED = (255, 0, 0)

# Initialize Pygame
pygame.init()
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sudoku")

# Generate Sudoku Board
board_gen = SudokuBoard()
board_gen.generate_board()
board_gen.puzzle("Easy")
puzzle_board = [row[:] for row in board_gen.board]
solved_board = board_gen.solved_board
user_board = [row[:] for row in puzzle_board]

# Buttons
check_button = pygame.Rect(50, 550, 100, 40)
solve_button = pygame.Rect(220, 550, 100, 40)
reset_button = pygame.Rect(390, 550, 100, 40)

selected_cell = None
checked_cells = []
checked = False

def draw_board():
    window.fill(WHITE)
    for i in range(GRID_SIZE + 1):
        thickness = 3 if i % BLOCK_SIZE == 0 else 1
        pygame.draw.line(window, BLACK, (0, i * CELL_SIZE), (WIDTH, i * CELL_SIZE), thickness)
        pygame.draw.line(window, BLACK, (i * CELL_SIZE, 0), (i * CELL_SIZE, WIDTH), thickness)

def draw_numbers():
    font = pygame.font.SysFont(None, 40)
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            num = puzzle_board[row][col]
            if num != 0:
                if checked and (row, col) in checked_cells:
                    color = RED
                elif board_gen.board[row][col] != 0:
                    color = BLUE
                else:
                    color = BLACK
                text = font.render(str(num), True, color)
                rect = text.get_rect(center=((col+0.5)*CELL_SIZE, (row+0.5)*CELL_SIZE))
                window.blit(text, rect)

def color_cell(row, col, color):
    pygame.draw.rect(window, color, (col*CELL_SIZE, row*CELL_SIZE, CELL_SIZE, CELL_SIZE))

def draw_buttons():
    font = pygame.font.SysFont(None, 30)
    pygame.draw.rect(window, GRAY, check_button)
    pygame.draw.rect(window, GRAY, solve_button)
    pygame.draw.rect(window, GRAY, reset_button)

    window.blit(font.render('Check', True, BLACK), (check_button.x+20, check_button.y+10))
    window.blit(font.render('Solve', True, BLACK), (solve_button.x+25, solve_button.y+10))
    window.blit(font.render('Reset', True, BLACK), (reset_button.x+25, reset_button.y+10))

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            if y < WIDTH:
                selected_cell = (y//CELL_SIZE, x//CELL_SIZE)
            elif check_button.collidepoint(event.pos):
                checked_cells = board_gen.find_incorrect(puzzle_board)
                checked = True
            elif solve_button.collidepoint(event.pos):
                puzzle_board = [row[:] for row in solved_board]
            elif reset_button.collidepoint(event.pos):
                puzzle_board = [row[:] for row in board_gen.board]
                checked_cells.clear()
                checked = False

        elif event.type == pygame.KEYDOWN and selected_cell:
            row, col = selected_cell
            if board_gen.board[row][col] == 0:
                if event.unicode.isdigit() and int(event.unicode) in range(1,10):
                    puzzle_board[row][col] = int(event.unicode)
                elif event.key in [pygame.K_BACKSPACE, pygame.K_DELETE]:
                    puzzle_board[row][col] = 0

    draw_board()

    if selected_cell:
        color_cell(selected_cell[0], selected_cell[1], ORANGE)

    for (row, col) in checked_cells:
        color_cell(row, col, (255, 200, 200))

    draw_numbers()
    draw_buttons()
    pygame.display.flip()

pygame.quit()
sys.exit()
