#   10 means the cell is emtpy, 11 means the cell is selected, all the other numbers represent themself.
from copy import deepcopy
import json

with open(r"Z:\justh\pycode\Shared_project\Sudoku\Helper\boards_data.json", "r") as json_read_file:
    board_data = json.load(json_read_file)


def get_name():
    print("\nPlease give your save a name.")
    name = input("> ")
    if 0 < len(name) < 14:
        found = False
        for other_names in board_data["BOARDS"]:
            if name == other_names["NAME"]:
                found = True
                print("This name was already used.")
                break
        if not found:
            return name
        else:
            return get_name()
    else:
        print("Sorry, this name is too long.\nKeep it under 17 chars.")
        return get_name()


def save_board(s_board):
    dic = {}
    name = get_name()
    dic["NAME"] = name
    dic["BOARD"] = deepcopy(s_board)
    board_data["BOARDS"].append(dic)
    dump_board(board_data)


def dump_board(board):
    with open(r"Z:\justh\pycode\Shared_project\Sudoku\Helper\boards_data.json", "w") as json_write_file:
        json.dump(board, json_write_file, indent=4)


empty_board = [[10,10,10,10,10,10,10,10,10],
               [10,10,10,10,10,10,10,10,10],
               [10,10,10,10,10,10,10,10,10],
               [10,10,10,10,10,10,10,10,10],
               [10,10,10,10,10,10,10,10,10],
               [10,10,10,10,10,10,10,10,10],
               [10,10,10,10,10,10,10,10,10],
               [10,10,10,10,10,10,10,10,10],
               [10,10,10,10,10,10,10,10,10]]

selected = [444]

board = board_data["BOARDS"][0]["BOARD"]

#   10 means the cell is filled. av_nums displayed in tuple.
av_board = [[],
            [],
            [],

            [],
            [],
            [],

            [],
            [],
            []]

# Shows the footnotes on the cells.
footnote_board = [[[], [], [],   [], [], [],     [], [], []],
               [[], [], [],   [], [], [],     [], [], []],
               [[], [], [],   [], [], [],     [], [], []],

                [[], [], [],   [], [], [],     [], [], []],
                [[], [], [],   [], [], [],     [], [], []],
                [[], [], [],   [], [], [],     [], [], []],

               [[], [], [],   [], [], [],     [], [], []],
               [[], [], [],   [], [], [],     [], [], []],
               [[], [], [],   [], [], [],     [], [], []]]

# Creates a static board, 0 means the cell is variable, 1 means it's static
static_board = [[],
            [],
            [],

            [],
            [],
            [],

            [],
            [],
            []]
