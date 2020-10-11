import pygame as pg
from Sudoku.Helper import board, WHITE, av_nums, av_board, used_nums, check_win, drawgrid, drawboard


def guess_one():
    shortest_av_nums = 10
    shortest_x, shortest_y = 0, 0
    for ynum, yrow in enumerate(board):
        for xnum, x in enumerate(yrow):
            used_nums(xnum, ynum)
            if len(av_nums) < shortest_av_nums and x == 10:
                shortest_av_nums = len(av_nums)
                shortest_x = xnum
                shortest_y = ynum
    used_nums(shortest_x, shortest_y)
    if len(av_nums) != 0:
        print("Guessing: ", av_nums[0], "for: ", shortest_x, shortest_y)
        board[shortest_y][shortest_x] = av_nums[0]
        return shortest_x, shortest_y
    else:
        return 444, 444


def solvboard_raw_solver(window, normal_board, co):
    if co == (10, 10):
        new_cox, new_coy = guess_one()
    else:
        x, y = co
        used_nums(x, y)
        print(av_nums[0])
        print(av_nums[1])
    window.fill(WHITE)
    drawgrid(window)
    drawboard(window)
    pg.display.update()
    stuck = False
    while not stuck:
        stuck = True
        for ynum, yrow in enumerate(board):
            for xnum, x in enumerate(yrow):
                used_nums(xnum, ynum)
                if len(av_nums) == 1 and x == 10:
                    print("Making: ", xnum, ynum, ": ", av_nums[0])
                    board[ynum][xnum] = av_nums[0]
                    stuck = False
        window.fill(WHITE)
        drawgrid(window)
        drawboard(window)
        pg.display.update()
    for y in range(9):
        for x in range(9):
            if board[y][x] == 10:
                used_nums(x, y)
                av_board[y].append(tuple(av_nums))
            else:
                av_board[y].append(10)
    impossible = False
    for yrow in av_board:
        for x in yrow:
            try:
                if len(x) == 0:
                    impossible = True
            except TypeError:
                pass
    if not impossible:
        solvboard_raw_solver(window, normal_board, (new_cox, new_coy))
    else:
        print("Got stuck here.")
        print("Normal_board:")
        for i in normal_board:
            print(i)
    print("In_game")
