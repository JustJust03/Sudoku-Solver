import pygame as pg


pg.init()


WIDTH = 720
HEIGHT = 720

#   ROWS is for the WIDTH, COLS is for the HEIGHT
ROWS, COLS = 9, 9
BLOCKWIDTH = WIDTH // ROWS
BLOCKHEIGHT = HEIGHT // COLS

#   Using the rgb codes
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
LIGHT_BLUE = (135,206,250)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (105, 105, 105)
LIGHT_GRAY = (170, 170, 170)

prev_nums = []
redo_nums = []
pos_nums = [1, 2, 3, 4, 5, 6, 7, 8, 9]
av_nums = []

#   The fonts to use.
font = pg.font.Font('freesansbold.ttf', 32)
font_num = pg.font.Font('freesansbold.ttf', 64)
font_footnote = pg.font.Font('freesansbold.ttf', 25)
font_mini_board = pg.font.Font("freesansbold.ttf", 20)
font_mini_num = pg.font.Font("freesansbold.ttf", 15)
font_menu = pg.font.Font("freesansbold.ttf", 48)

