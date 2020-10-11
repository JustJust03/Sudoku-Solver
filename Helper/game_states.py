import pygame as pg
from time import time
from Sudoku.Helper import board, WIDTH, ROWS, HEIGHT, COLS, WHITE, BLACK, used_nums, av_nums, check_win,\
    prev_nums, font, drawgrid, drawboard, solvboard_level1, solvboard_level6, footnote_board, board_data, \
    draw_mini_board, font_mini_board, selected, static_board, font_num, font_menu, save_board, dump_board, \
    empty_board, move_selected
from copy import deepcopy

in_game_start_time = 0
in_game_time = 0

pg.init()


# Main menu
def main_menu_key_down(key):
    if key == pg.K_RETURN:
        return "In_game"
    else:
        return "Main_menu"


def main_menu_update_screen(window, page):
    window.fill(WHITE)
    # Start button
    pg.draw.rect(window, BLACK, (WIDTH * 0.35, HEIGHT * 0.80, WIDTH * 0.30, HEIGHT * 0.15))
    pg.draw.rect(window, WHITE, (WIDTH * 0.35 + 2, HEIGHT * 0.80 + 2, WIDTH * 0.30 - 4, HEIGHT * 0.15 - 4))
    # Top boarders around "Sudoku boards"
    pg.draw.rect(window, BLACK, (WIDTH * 0.2, 0, WIDTH * 0.6, HEIGHT * 0.12))
    pg.draw.rect(window, WHITE, (WIDTH * 0.2 + 2, 0, WIDTH * 0.6 - 4, HEIGHT * 0.12 - 2))
    # Next button
    pg.draw.rect(window, BLACK, (WIDTH * 0.725, HEIGHT * 0.75, WIDTH * 0.2, HEIGHT * 0.1))
    pg.draw.rect(window, WHITE, (WIDTH * 0.725 + 2, HEIGHT * 0.75 + 2, WIDTH * 0.2 - 4, HEIGHT * 0.1 - 4))
    # Back button
    pg.draw.rect(window, BLACK, (WIDTH * 0.075, HEIGHT * 0.75, WIDTH * 0.2, HEIGHT * 0.1))
    pg.draw.rect(window, WHITE, (WIDTH * 0.075 + 2, HEIGHT * 0.75 + 2, WIDTH * 0.2 - 4, HEIGHT * 0.1 - 4))

    # Boarder around the window
    pg.draw.rect(window, BLACK, (0, 0, WIDTH, 2))
    pg.draw.rect(window, BLACK, (WIDTH - 2, 0, 2, HEIGHT))
    pg.draw.rect(window, BLACK, (0, 0, 2, HEIGHT))
    pg.draw.rect(window, BLACK, (0, HEIGHT - 2, WIDTH, 2))

    # Circles for visualizing on which page you are
    tabs = (len(board_data["BOARDS"]) - 1) // 6
    start_x = WIDTH * 0.5 - ((15 * tabs % 2 + 15) * tabs // 2)
    for x in range(tabs + 1):
        pg.draw.circle(window, BLACK, (int(start_x + 35 * x), int(HEIGHT * 0.755)), 14)
        pg.draw.circle(window, WHITE, (int(start_x + 35 * x), int(HEIGHT * 0.755)), 12)
        if x == page:
            pg.draw.circle(window, BLACK, (int(start_x + 35 * x), int(HEIGHT * 0.755)), 7)

    text0 = font.render("Sudoku   Boards", False, BLACK)
    text1 = font.render("Start", False, BLACK)
    text2 = font.render("NEXT", False, BLACK)
    text3 = font.render("BACK", False, BLACK)
    window.blit(text0, (WIDTH * 0.31, HEIGHT * 0.04))
    window.blit(text1, (WIDTH * 0.45, HEIGHT * 0.85))
    window.blit(text2, (WIDTH * 0.765, HEIGHT * 0.78))
    window.blit(text3, (WIDTH * 0.11, HEIGHT * 0.78))

    # Draws a rect around the selected board.
    if selected[0] != 444 and selected[0] // 6 == page:
        row = (selected[0] % 6) // 3
        col = (selected[0] % 3)
        pg.draw.rect(window, BLACK, (col * 220 + WIDTH * 0.055, 212 * row + HEIGHT * 0.13, 200, 220))
        pg.draw.rect(window, WHITE, (col * 220 + WIDTH * 0.062, 212 * row + HEIGHT * 0.137, 190, 210))
        if selected[0] != 0:
            # Draws del button
            pg.draw.rect(window, BLACK, (WIDTH * 0.725, HEIGHT * 0.877, WIDTH * 0.2, HEIGHT * 0.1))
            pg.draw.rect(window, WHITE, (WIDTH * 0.725 + 2, HEIGHT * 0.875 + 3, WIDTH * 0.2 - 4, HEIGHT * 0.1 - 4))
            text4 = font.render("DEL", False, BLACK)
            window.blit(text4, (WIDTH * 0.783, HEIGHT * 0.905))

    # Draw the boards from boards_data.json
    for co, b in enumerate(board_data["BOARDS"][(page * 6):(page * 6 + 6)]):
        row = co // 3
        col = co % 3
        text4 = font_mini_board.render(str(b["NAME"]), False, BLACK)
        window.blit(text4, (WIDTH * 0.08 + 220 * col, HEIGHT * 0.39 + 212 * row))
        draw_mini_board(window, b["BOARD"], HEIGHT * 0.15 + 212 * row, WIDTH * 0.08 + 220 * col)


def main_menu_mousekey_down(cox, coy, page):
    global in_game_start_time, in_game_time
    # Hit the start button
    if (WIDTH * 0.35) < cox < (WIDTH * 0.65) and (HEIGHT * 0.80) < coy < (HEIGHT * 0.95):
        print("START")
        in_game_start_time = time()
        if selected[0] != 444:
            for num in range(9):
                static_board[num].clear()
                for xnum in range(9):
                    footnote_board[num][xnum].clear()
                board[num] = deepcopy(board_data["BOARDS"][int(selected[0])]["BOARD"][num])
                for x in board_data["BOARDS"][int(selected[0])]["BOARD"][num]:
                    if x == 10:  static_board[num].append(0)
                    else:   static_board[num].append(1)
            return "In_game", page
        else:
            print("Select a board")
            return "Main_menu", page
    # Hit the first row of the boards
    elif (WIDTH * 0.08) < cox < 660 and (HEIGHT * 0.15) < coy < (HEIGHT * 0.15 + 212):
        if len(board_data["BOARDS"]) > ((cox - WIDTH * 0.08) // 200) + page * 6:
            selected[0] = ((cox - WIDTH * 0.08) // 200) + page * 6
        return "Main_menu", page
    # Hit the second row of the boards
    elif (WIDTH * 0.08) < cox < 660 and (HEIGHT * 0.15 + 212) < coy < (HEIGHT * 0.15 + 424):
        if len(board_data["BOARDS"]) > ((cox - WIDTH * 0.08) // 200) + page * 6 + 3:
            selected[0] = ((cox - WIDTH * 0.08) // 200) + page * 6 + 3
        return "Main_menu", page
    # Hit the back button
    elif (WIDTH * 0.075) < cox < (WIDTH * 0.275) and (HEIGHT * 0.75) < coy < (HEIGHT * 0.85):
        if page == 0:
            return "Main_menu", (len(board_data["BOARDS"]) - 1) // 6
        else:
            return "Main_menu", page - 1
    # Hit the next button
    elif (WIDTH * 0.725) < cox < (WIDTH * 0.925) and (HEIGHT * 0.75) < coy < (HEIGHT * 0.85):
        if page == (len(board_data["BOARDS"]) - 1) // 6:
            return "Main_menu", 0
        else:
            return "Main_menu", page + 1
    # Hit the delete button
    elif selected[0] != 444 and selected[0] // 6 == page and (WIDTH * 0.725) < cox < (WIDTH * 0.925) and \
            (HEIGHT * 0.877) < coy < (HEIGHT * 0.977):
        if selected[0] != 0:
            print(board_data["BOARDS"][int(selected[0])])
            del board_data["BOARDS"][int(selected[0])]
            selected[0] = 444
            dump_board(board_data)
        return "Main_menu", page
    else:
        return "Main_menu", page


# In game
def in_game_key_down(key, window):
    global in_game_time
    # s to solve the sudoku.
    if key == pg.K_s:
        start_time = time()
        print("solving")
        solvboard_level1(window)
        print("It took me: ", round(time() - start_time, 2), "seconds to solve this.")
        return "In_game"
    elif key == pg.K_l:
        print("solving level 6")
        solvboard_level6(window)
        return "In_game"
    elif key == pg.K_BACKSPACE:
        try:
            cox, coy = prev_nums.pop()
            for numy, yrow in enumerate(board):
                for numx, x in enumerate(yrow):
                    if x == 11:
                        board[numy][numx] = 10
            board[coy][cox] = 11
            used_nums(cox, coy)
            return "Fill_in"
        except IndexError:
            print("The board is empty, You can't go further back.")
            return "In_game"
    elif key == pg.K_ESCAPE:
        in_game_time = time() - in_game_start_time
        return "Paused"
    else:
        return "In_game"


def in_game_update_screen(window):
    window.fill(WHITE)
    drawgrid(window)
    drawboard(window)


def in_game_mousekey_down(cox, coy):
    # If coordinates on an empty cell: gamestate = Fill in.
    # Fill_in state and footnote will use this mousekey_down too.
    xrow = int(cox // (WIDTH / ROWS))
    yrow = int(coy // (HEIGHT / COLS))
    if board[yrow][xrow] == 11:
        board[yrow][xrow] = 12
        return "Footnote"
    elif board[yrow][xrow] == 12:
        board[yrow][xrow] = 10
        return"In_game"
    if static_board[yrow][xrow] == 0:
        for numy, y in enumerate(board):
            for numx, x in enumerate(y):
                if x == 11 or x == 12:
                    board[numy][numx] = 10
        if board[yrow][xrow] < 10:
            prev_nums.append((xrow, yrow, board[yrow][xrow]))
            print(prev_nums)
        board[yrow][xrow] = 11
        used_nums(xrow, yrow)
        print(av_nums)
        return "Fill_in"
    else:
        return "In_game"


# Fill in
def fill_in_key_down(key):
    global in_game_time
    if 48 <= key <= 57:
        for numy, yrow in enumerate(board):
            for numx, x in enumerate(yrow):
                if x == 11 and key - 48 in av_nums:
                    board[numy][numx] = key - 48
                    if numx < 8 and board[numy][numx + 1] == 10:
                        used_nums(numx + 1, numy)
                        print(av_nums)
                        board[numy][numx + 1] = 11
                    elif numx == 8 and board[numy + 1][0] == 10:
                        board[numy + 1][0] = 11
                        used_nums(0, numy)
                        print(av_nums)
                    prev_nums.append((numx, numy))
                    return "Fill_in"
        else: return "Fill_in"
    elif key == pg.K_BACKSPACE:
        try:
            prev = prev_nums.pop()
            for numy, yrow in enumerate(board):
                for numx, x in enumerate(yrow):
                    if x == 11:
                        board[numy][numx] = 10
            if len(prev) == 2:
                cox, coy = prev
                board[coy][cox] = 11
                used_nums(cox, coy)
            elif len(prev) == 3:
                cox, coy, num = prev
                board[coy][cox] = num
            return "Fill_in"
        except IndexError:
            print("The board is empty, You can't go further back.")
            return "Fill_in"
    elif key == pg.K_f:
        for numy, yrow in enumerate(board):
            for numx, x in enumerate(yrow):
                if x == 11:
                    board[numy][numx] = 12
        return "Footnote"
    elif key == pg.K_ESCAPE:
        in_game_time = time() - in_game_start_time
        return "Paused"
    elif key == pg.K_RIGHT or key == pg.K_TAB or key == pg.K_d:
        move_selected(1, 0, 11)
        return "Fill_in"
    elif key == pg.K_LEFT or key == pg.K_a:
        move_selected(-1, 0, 11)
        return "Fill_in"
    elif key == pg.K_UP or key == pg.K_w:
        move_selected(0, -1, 11)
        return "Fill_in"
    elif key == pg.K_DOWN or key == pg.K_RETURN or key == pg.K_s:
        move_selected(0, 1, 11)
        return "Fill_in"
    else: return "Fill_in"


def fill_in_update_screen(window):
    window.fill(WHITE)
    drawgrid(window)
    drawboard(window)


# Footnote
def footnote_key_down(key):
    global in_game_time
    if key == pg.K_f:
        for numy, yrow in enumerate(board):
            for numx, x in enumerate(yrow):
                if x == 12:
                    board[numy][numx] = 11
                    return "Fill_in"
    elif 48 <= key <= 57:
        for numy, yrow in enumerate(board):
            for numx, x in enumerate(yrow):
                if x == 12 and key - 48 not in footnote_board[numy][numx]:
                    footnote_board[numy][numx].append(key - 48)
                    return "Footnote"
    elif key == pg.K_BACKSPACE:
        for numy, yrow in enumerate(board):
            for numx, x in enumerate(yrow):
                if x == 12 and len(footnote_board[numy][numx]) > 0:
                    footnote_board[numy][numx].pop()
                    return "Footnote"
    elif key == pg.K_ESCAPE:
        in_game_time = time() - in_game_start_time
        return "Paused"
    elif key == pg.K_RIGHT or key == pg.K_TAB or key == pg.K_d:
        move_selected(1, 0, 12)
        return "Footnote"
    elif key == pg.K_LEFT or key == pg.K_a:
        move_selected(-1, 0, 12)
        return "Footnote"
    elif key == pg.K_UP or key == pg.K_w:
        move_selected(0, -1, 12)
        return "Footnote"
    elif key == pg.K_DOWN or key == pg.K_RETURN or key == pg.K_s:
        move_selected(0, 1, 12)
        return "Footnote"
    return "Footnote"


def footnote_update_screen(window):
    window.fill(WHITE)
    drawgrid(window)
    drawboard(window)

# Paused
def paused_key_down(key):
    if key == pg.K_ESCAPE:
        return "In_game"
    else:
        return "Paused"


def paused_mousekey_down(cox, coy, window):
    # Hit quit box:
    if WIDTH * 0.20 < cox < WIDTH * 0.46 and HEIGHT * 0.4 < coy < HEIGHT * 0.55:
        for boards in board_data["BOARDS"]:
            if boards["NAME"] == "Empty board":
                boards["BOARD"] = empty_board
                dump_board(board_data)
        return "Main_menu"
    # Hit Save box:
    elif WIDTH * 0.54 < cox < WIDTH * 0.8 and HEIGHT * 0.4 < coy < HEIGHT * 0.55:
        save_board(board)
        print("saved")
        return "Paused"
    # Hit Restart box:
    elif WIDTH * 0.20 < cox < WIDTH * 0.46 and HEIGHT * 0.62 < coy < HEIGHT * 0.77:
        prev_nums.clear()
        for num in range(9):
            for xnum, x in enumerate(static_board[num]):
                if x == 0:
                    board[num][xnum] = 10
            for x in footnote_board[num]:
                x.clear()
        return "In_game"
    # Hit Solve box:
    elif WIDTH * 0.54 < cox < WIDTH * 0.8 and HEIGHT * 0.62 < coy < HEIGHT * 0.77:
        start_time = time()
        print("solving")
        solvboard_level1(window)
        print("It took me: ", round(time() - start_time, 2), "seconds to solve this.")
        return "In_game"
    # Hit outside menu screen:
    elif WIDTH * 0.15 > cox or WIDTH * 0.85 < cox or HEIGHT * 0.15 > coy or HEIGHT * 0.85 < coy:
        return "In_game"
    else:
        print(cox, coy, WIDTH * 0.15, WIDTH * 0.85)
        return "Paused"


def paused_update_screen(window):
    # Draws the border:
    pg.draw.rect(window, BLACK, (WIDTH * 0.15, HEIGHT * 0.15, WIDTH * 0.7, HEIGHT * 0.7))
    pg.draw.rect(window, WHITE, (WIDTH * 0.16, HEIGHT * 0.16, WIDTH * 0.68, HEIGHT * 0.68))
    pg.draw.rect(window, BLACK, (WIDTH * 0.17, HEIGHT * 0.17, WIDTH * 0.66, HEIGHT * 0.66))
    pg.draw.rect(window, WHITE, (WIDTH * 0.18, HEIGHT * 0.18, WIDTH * 0.64, HEIGHT * 0.64))

    # Draws the title box:
    pg.draw.rect(window, BLACK, (WIDTH * 0.25, HEIGHT * 0.15, WIDTH * 0.5, HEIGHT * 0.15))
    pg.draw.rect(window, WHITE, (WIDTH * 0.26, HEIGHT * 0.16, WIDTH * 0.48, HEIGHT * 0.13))

    # Draws the Quit box:
    pg.draw.rect(window, BLACK, (WIDTH * 0.20, HEIGHT * 0.4, WIDTH * 0.26, HEIGHT * 0.15))
    pg.draw.rect(window, WHITE, (WIDTH * 0.21, HEIGHT * 0.41, WIDTH * 0.24, HEIGHT * 0.13))

    # Draws the Save box:
    pg.draw.rect(window, BLACK, (WIDTH * 0.54, HEIGHT * 0.4, WIDTH * 0.26, HEIGHT * 0.15))
    pg.draw.rect(window, WHITE, (WIDTH * 0.55, HEIGHT * 0.41, WIDTH * 0.24, HEIGHT * 0.13))

    # Draws the Restart box:
    pg.draw.rect(window, BLACK, (WIDTH * 0.20, HEIGHT * 0.62, WIDTH * 0.26, HEIGHT * 0.15))
    pg.draw.rect(window, WHITE, (WIDTH * 0.21, HEIGHT * 0.63, WIDTH * 0.24, HEIGHT * 0.13))

    # Draws the Solve box:
    pg.draw.rect(window, BLACK, (WIDTH * 0.54, HEIGHT * 0.62, WIDTH * 0.26, HEIGHT * 0.15))
    pg.draw.rect(window, WHITE, (WIDTH * 0.55, HEIGHT * 0.63, WIDTH * 0.24, HEIGHT * 0.13))

    # Writes the text:
    text0 = font_num.render("Paused", False, BLACK)
    text1 = font_menu.render("Quit", False, BLACK)
    text2 = font_menu.render("Save", False, BLACK)
    text3 = font_menu.render("Restart", False, BLACK)
    text4 = font_menu.render("Solve", False, BLACK)
    window.blit(text0, (WIDTH * 0.34, HEIGHT * 0.18))
    window.blit(text1, (WIDTH * 0.25, HEIGHT * 0.44))
    window.blit(text2, (WIDTH * 0.59, HEIGHT * 0.44))
    window.blit(text3, (WIDTH * 0.21, HEIGHT * 0.66))
    window.blit(text4, (WIDTH * 0.58, HEIGHT * 0.66))
