import pygame as pg
from Sudoku.Helper import board, av_nums, pos_nums, WIDTH, HEIGHT, COLS, ROWS, BLUE, BLACK, WHITE, font_num, LIGHT_BLUE, \
    footnote_board, LIGHT_GRAY, font_footnote, font_mini_num, static_board, GRAY


def used_nums(cox, coy):
    # Will check which numbers can be inserted on the given coordinates, and update the av_nums in constants.
    av_nums.clear()
    used_nums = []
    # Checks the horizontal line
    for num in board[coy]:
        if num < 10:
            used_nums.append(num)
    # Checks the vertical line
    for yrow in board:
        if yrow[cox] < 10:
            used_nums.append(yrow[cox])
    # Checks the box
    ybox = coy // 3
    xbox = cox // 3
    for ynum in range(3):
        for xnum in range(3):
            if board[ybox * 3 + ynum][xbox * 3 + xnum] < 10:
                used_nums.append(board[ybox * 3 + ynum][xbox * 3 + xnum])
    # updating av_nums in constants.
    for num in pos_nums:
        if num not in used_nums:
            av_nums.append(num)


def check_win():
    for yrow in board:
        for x in yrow:
            if x == 10 or x == 11:
                return False
    else: return True


def drawboard(window):
    for numy, yrow in enumerate(board):
        for numx, x in enumerate(yrow):
            if x == 10:
                pass
            elif x == 11:
                pg.draw.circle(window, BLUE, (int(numx * (WIDTH // ROWS) + WIDTH // ROWS * 0.5 + 2),
                                              int(numy * (HEIGHT // COLS) + HEIGHT // COLS * 0.5 + 2)),
                               int(WIDTH // ROWS * 0.5 - 5))
                pg.draw.circle(window, WHITE, (int(numx * (WIDTH // ROWS) + WIDTH // ROWS * 0.5 + 2),
                                               int(numy * (HEIGHT // COLS) + HEIGHT // COLS * 0.5 + 2)),
                               int(WIDTH // ROWS * 0.5 - 8))
            elif x == 12:
                pg.draw.circle(window, LIGHT_BLUE, (int(numx * (WIDTH // ROWS) + WIDTH // ROWS * 0.5 + 2),
                                              int(numy * (HEIGHT // COLS) + HEIGHT // COLS * 0.5 + 2)),
                               int(WIDTH // ROWS * 0.5 - 5))
                pg.draw.circle(window, WHITE, (int(numx * (WIDTH // ROWS) + WIDTH // ROWS * 0.5 + 2),
                                               int(numy * (HEIGHT // COLS) + HEIGHT // COLS * 0.5 + 2)),
                               int(WIDTH // ROWS * 0.5 - 8))
            else:
                if static_board[numy][numx] == 1:
                    color = BLACK
                else:
                    color = GRAY
                text = font_num.render(str(x), False, color)
                window.blit(text, (numx * (WIDTH / ROWS) + (WIDTH / ROWS * 0.3),
                                   numy * (HEIGHT / COLS) + (HEIGHT / COLS * 0.15)))
    for numy, yrow in enumerate(footnote_board):
        for numx, x in enumerate(yrow):
            if len(x) == 0:
                pass
            elif len(x) > 0 and board[numy][numx] > 9:
                for co_num, num in enumerate(x):
                    text = font_footnote.render(str(num), False, LIGHT_GRAY)
                    window.blit(text, (numx * (WIDTH / ROWS) + (WIDTH / ROWS * 0.09) + (co_num % 3) * 25,
                                numy * (HEIGHT / COLS) + (HEIGHT / COLS * 0.07) + ((co_num // 3) * 25)))


def drawgrid(window):
    for y in range(1, WIDTH // ROWS):
        if y % 3 == 0:
            width = 4
        else:
            width = 2
        rect = pg.rect.Rect((y * WIDTH // ROWS, 0), (width, HEIGHT))
        pg.draw.rect(window, BLACK, rect)
    for x in range(HEIGHT // COLS):
        if x % 3 == 0 and x != 0:
            width = 4
        else:
            width = 2
        rect = pg.rect.Rect((0, x * HEIGHT // COLS), (HEIGHT, width))
        pg.draw.rect(window, BLACK, rect)


def draw_mini_board(window, mini_board, cox, coy):
    for num in range(10):
        if num % 3 == 0:color = BLACK
        else: color = LIGHT_GRAY
        pg.draw.rect(window, color, (coy + 18 * num, cox, 1, 162))
        pg.draw.rect(window, color, (coy, cox + 18 * num, 162, 1))

    for numy, yrow in enumerate(mini_board):
        for numx, x in enumerate(yrow):
            if x == 10:
                pass
            else:
                text = font_mini_num.render(str(x), False, BLACK)
                window.blit(text, ((numx * 18 + coy + 5), (numy * 18 + cox + 4)))


def move_selected(cox, coy, seletected_num):
    for numy, yrow in enumerate(board):
        for numx, x in enumerate(yrow):
            if x == seletected_num:
                if 0 <= (numy + coy) < 9 and 0 <= (numx + cox) < 9 and board[numy + coy][numx + cox] == 10:
                    board[numy][numx] = 10
                    board[numy + coy][numx + cox] = seletected_num
                    used_nums(numx + cox, numy + coy)
                    print(av_nums)
                return None
