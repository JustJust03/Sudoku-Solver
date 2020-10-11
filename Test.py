board = [0, 5, 2, 0, 0, 0, 9, 1, 6]
static_board = []

for num, x in enumerate(board):
    if x == 0:  static_board.append(0)
    else:   static_board.append(1)

print(static_board)
