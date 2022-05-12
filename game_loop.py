from constants import consts as c
from player import Player

from numba import njit
import numpy as np
import pygame as pg

@njit(fastmath=True, nogil=True)
def ray_cast(layout, distances, player_params, render_params):
    player_x, player_y, player_angle = player_params[0], player_params[1], player_params[2]
    fov, dtheta, increment = render_params[0], render_params[1], render_params[2]
    angles = np.arange(player_angle - fov / 2, player_angle + fov / 2, dtheta)

    for i, angle in enumerate(angles):
        x, y = player_x, player_y
        dx, dy = increment * np.cos(angle), increment * np.sin(angle)

        while layout[int(x)][int(y)] == 0:
            x += dx
            y += dy
        
        distances[i] = np.sqrt((x - player_x) ** 2 + (y - player_y) ** 2)

def game_loop(screen):
    clock = pg.time.Clock()

    layout = np.array([
        [1, 1, 1, 1, 1],
        [1, 0, 0, 0, 1],
        [1, 0, 1, 0, 1],
        [1, 0, 0, 0, 1],
        [1, 1, 1, 1, 1]
    ])

    player = Player(1, 1, np.deg2rad(45))

    sky_color = pg.Color(0, 0, 255)
    ground_color = pg.Color(0, 255, 0)
    ground_rect = pg.Rect(0, c.SCREEN_HEIGHT / 2, c.SCREEN_WIDTH, c.SCREEN_HEIGHT / 2)
    wall_color = pg.Color(255, 0, 0)

    while 1:
        clock.tick(c.fps)

        keys_pressed = pg.key.get_pressed()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    pg.quit()
                    quit()

        player.update(keys_pressed)
        distances = np.zeros(c.SCREEN_WIDTH)
        ray_cast(layout, distances, (player.x, player.y, player.angle), (c.fov, c.dtheta, c.increment))
        
        screen.fill(sky_color)
        pg.draw.rect(screen, ground_color, ground_rect)

        

        for i, distance in enumerate(distances):
            height = c.height_multiplier / distance
            pg.draw.line(screen, wall_color, (i, c.SCREEN_HEIGHT / 2 - height / 2), (i, c.SCREEN_HEIGHT / 2 + height / 2))

        pg.display.flip()

        c.set_dt(clock.get_time() / 1000)
        print(c.dt)

if __name__ == '__main__':
    pg.init()
    screen = pg.display.set_mode((0, 0), pg.FULLSCREEN)
    c.init_screen(screen)
    game_loop(screen)