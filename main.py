from constants import consts as c
from game_loop import game_loop
import pygame as pg

if __name__ == '__main__':
    pg.init()
    screen = pg.display.set_mode((0, 0), pg.FULLSCREEN)
    c.init_screen(screen)

    game_loop(screen)