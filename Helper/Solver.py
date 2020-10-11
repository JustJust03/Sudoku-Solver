import pygame as pg
from copy import deepcopy
from Sudoku.Helper import board, used_nums, av_nums, check_win, WHITE, drawgrid, drawboard, av_board, guess_one

guessing = 0


def solvboard_level1(window):
    stuck = True
    for y in range(9):
        for x in range(9):
            if board[y][x] == 10:
                used_nums(x, y)
                if len(av_nums) == 1:
                    stuck = False
                    print("Making ", x, y, "this: ", av_nums)
                    board[y][x] = av_nums.pop()
                    window.fill(WHITE)
                    drawgrid(window)
                    drawboard(window)
                    pg.display.update()
    if check_win():
        print("solved")
    elif stuck:
        print("Couldn't solve more than this. going on to level 2.")
        solvboard_level2(window)
    else:
        solvboard_level1(window)


def solvboard_level2(window):
    stuck = True
    for y in range(9):
        for x in range(9):
            if board[y][x] == 10:
                xbox = x // 3
                ybox = y // 3
                used_nums(x, y)
                av_numbers = av_nums.copy()
                for num in av_numbers:
                    alone_x, alone_y, alone_cell = True, True, True
                    for x_y_in_row in range(9):
                        used_nums(x_y_in_row, y)
                        if num in av_nums and x_y_in_row != x and board[y][x_y_in_row] == 10:
                            alone_x = False
                        used_nums(x, x_y_in_row)
                        if num in av_nums and x_y_in_row != y and board[x_y_in_row][x] == 10:
                            alone_y = False
                    for y_cell in range(3):
                        for x_cell in range(3):
                            used_nums((xbox * 3 + x_cell), (ybox * 3 + y_cell))
                            if num in av_nums and (xbox * 3 + x_cell != x or ybox * 3 + y_cell != y) \
                                    and board[ybox * 3 + y_cell][xbox * 3 + x_cell] == 10:
                                alone_cell = False
                    if alone_x or alone_y or alone_cell:
                        stuck = False
                        print("Making ", x, y, "this: ", num)
                        board[y][x] = num
    if not stuck:
        print("Level 2 solved! going back to level 1")
        window.fill(WHITE)
        drawgrid(window)
        drawboard(window)
        pg.display.update()
        solvboard_level1(window)
    else:
        print("Couldn't solve more than this. going on to level 3.")
        solvboard_level3(window)


def solvboard_level3(window):
    for i in av_board:
        i.clear()
    for y in range(9):
        for x in range(9):
            if board[y][x] == 10:
                used_nums(x, y)
                av_board[y].append(tuple(av_nums))
            else:
                av_board[y].append(10)
    for y in range(9):
        for x in range(9):
            if av_board[y][x] != 10:
                for x_in_yrow in range(9):
                    if av_board[y][x] == av_board[y][x_in_yrow] and x_in_yrow != x and len(av_board[y][x]) == 2:
                        num1, num2 = av_board[y][x]
                        for xrow in range(9):
                            if av_board[y][xrow] != 10 and av_board[y][xrow] != av_board[y][x]:
                                lst = list(av_board[y][xrow])
                                try:
                                    try: lst.remove(num1); lst.remove(num2)
                                    except ValueError: lst.remove(num2)
                                except ValueError:
                                    pass
                                av_board[y][xrow] = tuple(lst)
                    if av_board[y][x] == av_board[x_in_yrow][x] and x_in_yrow != y and len(av_board[y][x]) == 2:
                        num1, num2 = av_board[y][x]
                        for yrow in range(9):
                            if av_board[yrow][x] != 10 and av_board[yrow][x] != av_board[y][x]:
                                lst = list(av_board[yrow][x])
                                try:
                                    try: lst.remove(num1); lst.remove(num2)
                                    except ValueError: lst.remove(num2)
                                except ValueError:
                                    pass
                                av_board[yrow][x] = tuple(lst)
                ybox = y // 3
                xbox = x // 3
                for y_in_grid in range(3):
                    for x_in_grid in range(3):
                        if av_board[y][x] == av_board[ybox * 3 + y_in_grid][xbox * 3 + x_in_grid]\
                                and (y != ybox * 3 + y_in_grid or x != xbox * 3 + x_in_grid)\
                                and len(av_board[y][x]) == 2:
                            num1, num2 = av_board[y][x]
                            for yrow_in_grid in range(3):
                                for xrow_in_grid in range(3):
                                    if av_board[ybox * 3 + yrow_in_grid][xbox * 3 + xrow_in_grid] != 10 \
                                            and av_board[ybox * 3 + yrow_in_grid][xbox * 3 + xrow_in_grid] != av_board[y][x]:
                                        lst = list(av_board[ybox * 3 + yrow_in_grid][xbox * 3 + xrow_in_grid])
                                        try:
                                            try:
                                                lst.remove(num1); lst.remove(num2)
                                            except ValueError:
                                                lst.remove(num2)
                                        except ValueError:
                                            pass
                                        av_board[ybox * 3 + yrow_in_grid][xbox * 3 + xrow_in_grid] = tuple(lst)
    stuck = True
    for y in range(9):
        for x in range(9):
            try:
                if len(av_board[y][x]) == 1:
                    stuck = False
                    print("Making ", x, y, "this: ", av_board[y][x][0])
                    board[y][x] = av_board[y][x][0]
            except TypeError:
                pass
    if not stuck:
        print("Level 3 solved! going back to level 1")
        for i in av_board:
            i.clear()
        window.fill(WHITE)
        drawgrid(window)
        drawboard(window)
        pg.display.update()
        solvboard_level1(window)
    else:
        print("Couldn't solve more than this. going on to level 4.")
        for i in av_board:
            i.clear()
        solvboard_level4(window)


def solvboard_level4(window):
    for i in av_board:
        i.clear()
    for y in range(9):
        for x in range(9):
            if board[y][x] == 10:
                used_nums(x, y)
                av_board[y].append(tuple(av_nums))
            else:
                av_board[y].append(10)
    for y in range(9):
        for x in range(9):
            if av_board[y][x] != 10:
                found_threes_y = []
                found_threes_x = []
                found_threes_cell = []
                for x_in_yrow in range(9):
                    if av_board[y][x] == av_board[y][x_in_yrow] and x_in_yrow != x and len(av_board[y][x]) == 3 \
                            and av_board[y][x] not in found_threes_y:
                        found_threes_y.append(av_board[y][x])
                    elif av_board[y][x] == av_board[y][x_in_yrow] and x_in_yrow != x and len(av_board[y][x]) == 3 \
                            and av_board[y][x] in found_threes_y:
                        num1, num2, num3 = av_board[y][x]
                        for xrow in range(9):
                            if av_board[y][xrow] != 10 and av_board[y][xrow] != av_board[y][x]:
                                lst = list(av_board[y][xrow])
                                try:
                                    try:
                                        try: lst.remove(num1); lst.remove(num2); lst.remove(num3)
                                        except ValueError: lst.remove(num2); lst.remove(num3)
                                    except ValueError: lst.remove(num3)
                                except ValueError:
                                    pass
                                av_board[y][xrow] = tuple(lst)
                    if av_board[y][x] == av_board[x_in_yrow][x] and x_in_yrow != y and len(av_board[y][x]) == 3 \
                            and av_board[y][x] not in found_threes_x:
                        found_threes_x.append(av_board[y][x])
                    elif av_board[y][x] == av_board[x_in_yrow][x] and x_in_yrow != y and len(av_board[y][x]) == 3 \
                            and av_board[y][x] in found_threes_x:
                        num1, num2, num3 = av_board[y][x]
                        for yrow in range(9):
                            if av_board[yrow][x] != 10 and av_board[yrow][x] != av_board[y][x]:
                                lst = list(av_board[yrow][x])
                                try:
                                    try:
                                        try: lst.remove(num1); lst.remove(num2); lst.remove(num3)
                                        except ValueError: lst.remove(num2); lst.remove(num3)
                                    except ValueError: lst.remove(num3)
                                except ValueError:
                                    pass
                                av_board[yrow][x] = tuple(lst)
                ybox = y // 3
                xbox = x // 3
                for y_in_grid in range(3):
                    for x_in_grid in range(3):
                        if av_board[y][x] == av_board[ybox * 3 + y_in_grid][xbox * 3 + x_in_grid] \
                                and (y != ybox * 3 + y_in_grid or x != xbox * 3 + x_in_grid) \
                                and len(av_board[y][x]) == 3 and av_board[y][x] not in found_threes_cell:
                            found_threes_cell.append(av_board[y][x])
                        elif av_board[y][x] == av_board[ybox * 3 + y_in_grid][xbox * 3 + x_in_grid] \
                                and (y != ybox * 3 + y_in_grid or x != xbox * 3 + x_in_grid) \
                                and len(av_board[y][x]) == 3 and av_board[y][x] in found_threes_cell:
                            num1, num2, num3 = av_board[y][x]
                            for yrow_in_grid in range(3):
                                for xrow_in_grid in range(3):
                                    if av_board[ybox * 3 + yrow_in_grid][xbox * 3 + xrow_in_grid] != 10 \
                                            and av_board[ybox * 3 + yrow_in_grid][xbox * 3 + xrow_in_grid] != av_board[y][x]:
                                        lst = list(av_board[ybox * 3 + yrow_in_grid][xbox * 3 + xrow_in_grid])
                                        try:
                                            try:
                                                try:
                                                    lst.remove(num1); lst.remove(num2); lst.remove(num3)
                                                except ValueError:
                                                    lst.remove(num2); lst.remove(num3)
                                            except ValueError:
                                                lst.remove(num3)
                                        except ValueError:
                                            pass
                                        av_board[ybox * 3 + yrow_in_grid][xbox * 3 + xrow_in_grid] = tuple(lst)
    stuck = True
    for y in range(9):
        for x in range(9):
            try:
                if len(av_board[y][x]) == 1:
                    stuck = False
                    print("Making ", x, y, "this: ", av_board[y][x][0])
                    board[y][x] = av_board[y][x][0]
            except TypeError:
                pass
    if not stuck:
        print("Level 4 solved! going back to level 1")
        for i in av_board:
            i.clear()
        window.fill(WHITE)
        drawgrid(window)
        drawboard(window)
        pg.display.update()
        solvboard_level1(window)
    else:
        print("Couldn't solve more than this. going on to level 5.")
        for i in av_board:
            i.clear()
        solvboard_level5(window)


def solvboard_level5(window):
    for i in av_board:
        i.clear()
    for y in range(9):
        for x in range(9):
            if board[y][x] == 10:
                used_nums(x, y)
                av_board[y].append(tuple(av_nums))
            else:
                av_board[y].append(10)
    for y_cell in range(3):
        for x_cell in range(3):
            for num in range(1, 10):
                co_nums_x = []
                co_nums_y = []
                for y_in_cell in range(3):
                    for x_in_cell in range(3):
                        try:
                            if num in av_board[y_cell * 3 + y_in_cell][x_cell * 3 + x_in_cell] \
                                    or board[y_cell * 3 + y_in_cell][x_cell * 3 + x_in_cell] == num:
                                co_nums_x.append(x_cell * 3 + x_in_cell)
                                co_nums_y.append(y_cell * 3 + y_in_cell)
                        except TypeError:
                            pass
                if len(co_nums_x) > 0 and len(co_nums_x) == co_nums_x.count(co_nums_x[0]):
                    for y_down in range(9):
                        try:
                            if num in av_board[y_down][co_nums_x[0]] and y_down not in co_nums_y:
                                lst = list(av_board[y_down][co_nums_x[0]])
                                lst.remove(num)
                                av_board[y_down][co_nums_x[0]] = tuple(lst)
                        except TypeError:
                            pass
                if len(co_nums_y) > 0 and len(co_nums_y) == co_nums_y.count(co_nums_y[0]):
                    for x_right in range(9):
                        try:
                            if num in av_board[co_nums_y[0]][x_right] and x_right not in co_nums_x:
                                lst = list(av_board[co_nums_y[0]][x_right])
                                lst.remove(num)
                                av_board[co_nums_y[0]][x_right] = tuple(lst)
                        except TypeError:
                            pass
    stuck = True
    for y in range(9):
        for x in range(9):
            try:
                if len(av_board[y][x]) == 1:
                    stuck = False
                    print("Making ", x, y, "this: ", av_board[y][x][0])
                    board[y][x] = av_board[y][x][0]
            except TypeError:
                pass
    if not stuck:
        print("Level 5 solved! going back to level 1")
        for i in av_board:
            i.clear()
        window.fill(WHITE)
        drawgrid(window)
        drawboard(window)
        pg.display.update()
        solvboard_level1(window)
    elif guessing == 0:
        print("Couldn't solve more than this, going on to level 6")
        for i in av_board:
            i.clear()
        solvboard_level6(window)
    if guessing > 0:
        for i in av_board:
            i.clear
        for y in range(9):
            for x in range(9):
                if board[y][x] == 10:
                    used_nums(x, y)
                    av_board[y].append(tuple(av_nums))
                else:
                    av_board[y].append(10)
        stuck = False
        for yrow in av_board:
            for i in yrow:
                try:
                    if len(i) < 1:
                        stuck = True
                except TypeError:
                    pass
        if not stuck and not check_win():
            print("Couldn't solve more for this guess, so guessing another one.")
            for i in av_board:
                i.clear()
            solvboard_level6(window)


def solvboard_level6(window):
    global guessing
    guessing += 1
    old_board = deepcopy(board)
    guess_x, guess_y = guess_one()
    print("Guessloop: ", guessing)
    solvboard_level1(window)
    for i in av_board:
        i.clear()
    for y in range(9):
        for x in range(9):
            if board[y][x] == 10:
                used_nums(x, y)
                av_board[y].append(tuple(av_nums))
            else:
                av_board[y].append(10)
    finished = False
    zeros = 0
    for yrow in av_board:
        for i in yrow:
            try:
                if len(i) == 0 and not finished:
                    finished = True
                    for row in range(9):
                        board[row] = old_board[row]
                    used_nums(guess_x, guess_y)
                    if check_win():
                        pass
                    elif guessing == 1:
                        print("Guess was not right, So it has to be: ", av_nums[1], "for: ", guess_x, guess_y)
                        guessing -= 1
                        board[guess_y][guess_x] = av_nums[1]
                        solvboard_level1(window)
                    else:
                        print("Prev guess was not right, so will now try: ", av_nums[1], "for: ", guess_x, guess_y)
                        board[guess_y][guess_x] = av_nums[1]
                        solvboard_level1(window)
            except TypeError:
                pass
