import time
import random
import pygame
import sys
import copy


def load_boards(values):
    empty = 0
    grid = [[0 for i in range(9)] for i in range(9)]
    values = [int(i) for i in values]
    for i in range(9):
        for j in range(9):
            grid[i][j] = values[i * 9 + j]
            if values[i * 9 + j] == 0:
                empty += 1
    return grid, empty


def solve_board(missing_values):
    grid = copy.deepcopy(board)    
    while missing_values >=  0:
        column_array = []
        for i in range(9):
            curr_column = []
            for j in range(9):
                if grid[j][i] > 0:
                    curr_column.append(grid[j][i])
            column_array.append(curr_column)

        row_array = []
        for i in range(9):
            curr_row = []
            for j in range(9):
                if grid[i].count(j + 1) > 0:
                    curr_row.append(j + 1)
            row_array.append(curr_row)

        possible_grid = [[[] for i in range(9)] for i in range(9)]
        possible_row = [[0 for i in range(9)] for i in range(9)]
        possible_column = [[0 for i in range(9)] for i in range(9)]

        for r in range(9):
            for c in range(9):
                if grid[r][c] == 0:
                    possible_values = [i for i in range(1, 10)]
                    for i in column_array[c]:
                        if i in possible_values:
                            possible_values.remove(i)
                    for i in row_array[r]:
                        if i in possible_values:
                            possible_values.remove(i)
                    max_row = ((r // 3) + 1) * 3 - 1
                    max_column = ((c // 3) + 1) * 3 - 1
                    min_row = r // 3 * 3
                    min_column = c // 3 * 3
                    for i in range(min_row, max_row + 1):
                        for j in range(min_column, max_column + 1):
                            if grid[i][j] != 0 and grid[i][j] in possible_values:
                                possible_values.remove(grid[i][j])
                    possible_grid[r][c] = possible_values
                    for i in possible_values:
                        possible_row[r][i - 1] += 1
                        possible_column[c][i - 1] += 1

        for i in range(9): 
            for j in range(possible_column[i].count(1)):
                valuey = [i for i, n in enumerate(possible_column[i]) if n == 1][j] + 1
                for k in range(9):
                    if valuey in possible_grid[k][i]:
                        grid[k][i] = valuey
                        missing_values -= 1
                        break
        for i in range(9): 
            for j in range(possible_row[i].count(1)):
                valuex = [i for i, n in enumerate(possible_row[i]) if n == 1][j] + 1
                for k in range(9):
                    if valuex in possible_grid[i][k]:
                        grid[i][k] = valuex
                        missing_values -= 1
                        break
    return grid


with open("C:\\Users\\jesse\\Downloads\\sudoku.csv", "r") as s:
    header = s.readline()
    puzzles = []
    for i in s:
        puzzles.append(s.readline().split(",")[0])


DIMENSION = 9
SQUARESIZE = 50
WIDTH = 1
BORDER = 40

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)


def draw_lines():
    for i in range(DIMENSION):
        if (i + 1) % 3 == 0:
            pygame.draw.lines(screen, BLACK, True, (((i + 1) * SQUARESIZE + BORDER, BORDER), (((i + 1) * SQUARESIZE + BORDER, DIMENSION * SQUARESIZE + BORDER))), 3 * WIDTH)
            pygame.draw.lines(screen, BLACK, True, ((BORDER, (i + 1) * SQUARESIZE + BORDER), ((DIMENSION * SQUARESIZE + BORDER, (i + 1) * SQUARESIZE + BORDER))), 3 * WIDTH)

        else:
            pygame.draw.lines(screen, BLACK, True, (((i + 1) * SQUARESIZE + BORDER, BORDER), (((i + 1) * SQUARESIZE + BORDER, DIMENSION * SQUARESIZE + BORDER))), WIDTH)
            pygame.draw.lines(screen, BLACK, True, ((BORDER, (i + 1) * SQUARESIZE + BORDER), ((DIMENSION * SQUARESIZE + BORDER, (i + 1) * SQUARESIZE + BORDER))), WIDTH)
    pygame.display.update()


def get_cell(x, y):
    if BORDER < x < DIMENSION * SQUARESIZE + BORDER and BORDER < y < DIMENSION * SQUARESIZE + BORDER:
        return int((y - BORDER) / SQUARESIZE), int((x - BORDER) / SQUARESIZE)
    else:
        return -1, -1


def message(size, word, color, bold=True):
    # sets font with hard coded font type and passed in size 
    set_font = pygame.font.SysFont("Courier New", size, bold)

    # creates text block with passed in message and color
    set_color = set_font.render(word, True, color)

    # gets dimension of text block in form [left,top,screen_side,game_screen_height]
    get_dimension = set_color.get_rect()

    return set_color, get_dimension[2], get_dimension[3]


def draw_values(given_value, wrongx=-1, wrongy=-1):
    bold = given_value
    if wrongx != -1:
        if board[wrongx][wrongy] == 0:
            bold = False
        else:
            bold = True
    for i in range(DIMENSION):
        for j in range(DIMENSION):
            if player_board[i][j] != 0:
                if board[i][j] == 0:
                    pygame.draw.rect(screen, WHITE, (j * SQUARESIZE + BORDER + (WIDTH * 2), i * SQUARESIZE + BORDER + (WIDTH * 2), SQUARESIZE - (WIDTH * 4), SQUARESIZE - (WIDTH * 4)))
                text, x2, y2 = "", 0, 0

                if wrongx == i and wrongy == j:
                    text, x2, y2 = message(36, str(player_board[i][j]), RED, bold)
                else:
                    text, x2, y2 = message(36, str(player_board[i][j]), BLACK, given_value)

                x1 = (SQUARESIZE - x2) / 2
                y1 = (SQUARESIZE - y2) / 2
                screen.blit(text, (j * SQUARESIZE + BORDER + x1, i * SQUARESIZE + BORDER + y1, SQUARESIZE, SQUARESIZE))
            else:
                pygame.draw.rect(screen, WHITE, (j * SQUARESIZE + BORDER + (WIDTH * 2), i * SQUARESIZE + BORDER + (WIDTH * 2), SQUARESIZE - (WIDTH * 4), SQUARESIZE - (WIDTH * 4)))


    pygame.display.update()

    if wrongx != -1:
        pygame.time.wait(100)
        pygame.draw.rect(screen, WHITE, (wrongy * SQUARESIZE + BORDER + (WIDTH * 2), wrongx * SQUARESIZE + BORDER + (WIDTH * 2), SQUARESIZE - (WIDTH * 4), SQUARESIZE - (WIDTH * 4)))
        text, x2, y2 = message(36, str(player_board[wrongx][wrongy]), BLACK, bold)
        x1 = (SQUARESIZE - x2) / 2
        y1 = (SQUARESIZE - y2) / 2
        screen.blit(text, (wrongy * SQUARESIZE + BORDER + x1, wrongx * SQUARESIZE + BORDER + y1, SQUARESIZE, SQUARESIZE))
        pygame.display.update()


def valid_selection(x, y):
    if board[x][y] == 0:
        return True
    else:
        return False


def valid_placement(x, y, value):
    for i in range(DIMENSION):
        if player_board[x][i] == value and i != y:
            return False, x, i
        if player_board[i][y] == value and i != x:
            return False, i, y

    max_row = ((x // 3) + 1) * 3 - 1
    max_column = ((y // 3) + 1) * 3 - 1
    min_row = x // 3 * 3
    min_column = y // 3 * 3

    for i in range(min_row, max_row + 1):
        for j in range(min_column, max_column + 1):
            if player_board[i][j] == value and (i != x and j != y):
                return False, i, j

    return True, -1, -1
    

def create_buttons():
    pygame.draw.rect(screen, BLACK, (0, DIMENSION * SQUARESIZE + BORDER, screen_side, BORDER))

    text, x2, y2 = message(20, "NEW PUZZLE", RED)
    x1 = (screen_side / 3 - x2) / 2
    y1 = (BORDER - y2) / 2

    reset_button = pygame.draw.rect(screen, WHITE, (x1 - (WIDTH * 2), SQUARESIZE * DIMENSION + BORDER + y1 - WIDTH, x2 + (WIDTH * 4), y2 + WIDTH))
    new_button = pygame.draw.rect(screen, WHITE, (screen_side / 3 + x1 - (WIDTH * 2), SQUARESIZE * DIMENSION + BORDER + y1 - WIDTH, x2 + (WIDTH * 4), y2 + WIDTH))
    solve_button = pygame.draw.rect(screen, WHITE, (2 * screen_side / 3 + x1 - (WIDTH * 2), SQUARESIZE * DIMENSION + BORDER + y1 - WIDTH, x2 + (WIDTH * 4), y2 + WIDTH))
    
    screen.blit(text, (screen_side / 3 + x1, SQUARESIZE * DIMENSION + BORDER + y1, x2, y2))

    text, x2, y2 = message(20, "RESET", RED)
    x1 = (screen_side / 3 - x2) / 2
    y1 = (BORDER - y2) / 2
    screen.blit(text, (x1, SQUARESIZE * DIMENSION + BORDER + y1, x2, y2))

    text, x2, y2 = message(20, "SOLVE", RED)
    x1 = (screen_side / 3 - x2) / 2
    y1 = (BORDER - y2) / 2
    screen.blit(text, (2 * screen_side / 3 + x1, SQUARESIZE * DIMENSION + BORDER + y1, x2, y2))

    pygame.display.update()

    return reset_button, new_button, solve_button


def show_solution():
    for i in range(DIMENSION):
        for j in range(DIMENSION):
            color = BLACK
            given = True
            if player_board[i][j] != 0:                    
                pygame.draw.rect(screen, WHITE, (j * SQUARESIZE + BORDER + (WIDTH * 2), i * SQUARESIZE + BORDER + (WIDTH * 2), SQUARESIZE - (WIDTH * 4), SQUARESIZE - (WIDTH * 4)))
                if player_board[i][j] == complete_board[i][j] != board[i][j]:
                    color = GREEN
                    given = False
                elif player_board[i][j] != complete_board[i][j]:
                    color = RED
                    given = False
            else:
                given = False
            text, x2, y2 = message(36, str(complete_board[i][j]), color, given)
            x1 = (SQUARESIZE - x2) / 2
            y1 = (SQUARESIZE - y2) / 2
            screen.blit(text, (j * SQUARESIZE + BORDER + x1, i * SQUARESIZE + BORDER + y1, SQUARESIZE, SQUARESIZE))
    
    pygame.display.update()


def end_game():
    pygame.draw.rect(screen, BLACK, (0, DIMENSION * SQUARESIZE + BORDER, screen_side, BORDER))

    text, x2, y2 = message(28, "PLAY AGAIN?", RED)
    x1 = (screen_side - x2) / 2
    y1 = (BORDER - y2) / 2
    screen.blit(text, (x1, SQUARESIZE * DIMENSION + BORDER + y1, screen_side, BORDER))

    text, x2, y2 = message(28, "YES", BLACK)
    x1 = (screen_side / 3 - x2) / 2
    y1 = (BORDER - y2) / 2

    yes_block = pygame.draw.rect(screen, GREEN, (x1, SQUARESIZE * DIMENSION + BORDER + y1, x2, -2 * y1 + BORDER))
    no_block = pygame.draw.rect(screen, RED, (2 / 3 * screen_side + x1, SQUARESIZE * DIMENSION + BORDER + y1, x2, -2 * y1 + BORDER))

    screen.blit(text, (x1, SQUARESIZE * DIMENSION + BORDER + y1, screen_side, BORDER))

    text, x2, y2 = message(28, "NO", BLACK)
    x1 = (screen_side / 3 - x2) / 2
    y1 = (BORDER - y2) / 2

    screen.blit(text, (2 / 3 * screen_side + x1, SQUARESIZE * DIMENSION + BORDER + y1, screen_side, BORDER))

    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                choice = event.pos
                if yes_block.collidepoint(choice):
                    return True
                if no_block.collidepoint(choice):
                    return False


def clear_board():
    for i in range(DIMENSION):
        for j in range(DIMENSION):
            pygame.draw.rect(screen, WHITE, (j * SQUARESIZE + BORDER + (WIDTH * 2), i * SQUARESIZE + BORDER + (WIDTH * 2), SQUARESIZE - (WIDTH * 4), SQUARESIZE - (WIDTH * 4)))

    pygame.display.update()


pygame.init()

screen_side = DIMENSION * SQUARESIZE + (2 * BORDER)
screen = pygame.display.set_mode((screen_side, screen_side))
pygame.display.set_caption("SUDOKU")

play_again = True
while play_again:
    pygame.draw.rect(screen, WHITE, (BORDER, BORDER, DIMENSION * SQUARESIZE, DIMENSION * SQUARESIZE))

    draw_lines()

    game = True
    selected = False

    reset, new_puzzle, solve = create_buttons()
    
    board, blank_cells = load_boards(puzzles[random.randint(0, len(puzzles) - 1)])
    player_board = copy.deepcopy(board)

    draw_values(True)
    
    start_time = pygame.time.get_ticks()

    clock = pygame.time.Clock()

    clock.tick(60)

    while game:
        pygame.draw.rect(screen, BLACK, (0, 0, screen_side, BORDER))
        minutes = int((pygame.time.get_ticks() - start_time) / 1000 / 60)
        seconds = round(round((pygame.time.get_ticks() - start_time) / 1000, 1) % 60, 1)
        display_clock = "{}:{}".format(minutes, seconds)
        if minutes == 0:
            display_clock = "{}".format(seconds)
        elif seconds < 10:
            display_clock = "{}:0{}".format(minutes, seconds)
        text, x2, y2 = message(32, display_clock, RED)
        x1 = (screen_side - x2) / 2
        y1 = (BORDER - y2) / 2
        
        screen.blit(text, (x1, y1, screen_side, BORDER))
        pygame.display.update()

        for event in pygame.event.get():    
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                posx = event.pos[0]
                posy = event.pos[1]
                selectedx, selectedy = get_cell(posx, posy)
                if selectedx != -1 and valid_selection(selectedx, selectedy):
                    selected = True
                else:
                    if new_puzzle.collidepoint(event.pos) or reset.collidepoint(event.pos):
                        if new_puzzle.collidepoint(event.pos):
                            clear_board()
                            board, blank_cells = load_boards(puzzles[random.randint(0, 3)])
                        player_board = copy.deepcopy(board)
                        draw_values(True)
                        selected = False
                        start_time = pygame.time.get_ticks()
                    elif solve.collidepoint(event.pos):
                        complete_board = solve_board(blank_cells)
                        show_solution()
                        game = False

            if event.type == pygame.KEYDOWN:
                if selected:
                    new_value = 0
                    if event.key == pygame.K_1:
                        new_value = 1
                    elif event.key == pygame.K_2:
                        new_value = 2
                    elif event.key == pygame.K_3:
                        new_value = 3
                    elif event.key == pygame.K_4:
                        new_value = 4
                    elif event.key == pygame.K_5:
                        new_value = 5
                    elif event.key == pygame.K_6:
                        new_value = 6
                    elif event.key == pygame.K_7:
                        new_value = 7
                    elif event.key == pygame.K_8:
                        new_value = 8
                    elif event.key == pygame.K_9:
                        new_value = 9

                    if new_value > 0:
                        valid, conflictx, conflicty = valid_placement(selectedx, selectedy, new_value)
                        if valid:
                            player_board[selectedx][selectedy] = new_value
                            draw_values(False)
                            selected = False
                        else:
                            draw_values(False, conflictx, conflicty)
                            
    play_again = end_game()
                    