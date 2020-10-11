import pygame as pg

import Sudoku.Helper.game_states as gmstate
from Sudoku.Helper import WIDTH, HEIGHT

running = True
gamestate = "Main_menu"
page = 0

win = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("Sudoko")


def update_screen(window, game_state):
    if game_state == "Main_menu":
        gmstate.main_menu_update_screen(window, page)
    elif game_state == "In_game":
        gmstate.in_game_update_screen(window)
    elif game_state == "Fill_in":
        gmstate.fill_in_update_screen(window)
    elif game_state == "Solving":
        pass
    elif game_state == "Footnote":
        gmstate.footnote_update_screen(window)
    elif game_state == "Paused":
        gmstate.paused_update_screen(window)
    pg.display.update()


while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
            pg.quit()

        elif event.type == pg.KEYDOWN:
            if gamestate == "Main_menu":
                gamestate = gmstate.main_menu_key_down(event.key)
            elif gamestate == "In_game":
                gamestate = gmstate.in_game_key_down(event.key, win)
            elif gamestate == "Fill_in":
                gamestate = gmstate.fill_in_key_down(event.key)
            elif gamestate == "Solving":
                gmstate.solving_key_down(event.key)
            elif gamestate == "Footnote":
                gamestate = gmstate.footnote_key_down(event.key)
            elif gamestate == "Paused":
                gamestate = gmstate.paused_key_down(event.key)

        elif event.type == pg.MOUSEBUTTONUP:
            cox, coy = pg.mouse.get_pos()
            if gamestate == "Main_menu":
                gamestate, page = gmstate.main_menu_mousekey_down(cox, coy, page)
            elif gamestate == "In_game":
                gamestate = gmstate.in_game_mousekey_down(cox, coy)
            elif gamestate == "Fill_in":
                gamestate = gmstate.in_game_mousekey_down(cox, coy)
            elif gamestate == "Solving":
                gmstate.solving_mousekey_down(cox, coy)
            elif gamestate == "Footnote":
                gamestate = gmstate.in_game_mousekey_down(cox, coy)
            elif gamestate == "Paused":
                gamestate = gmstate.paused_mousekey_down(cox, coy, win)


        if running:
            update_screen(win, gamestate)
