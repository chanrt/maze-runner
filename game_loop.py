from constants import consts as c
from maze_generator import *
from player import Player

from numba import njit
import numpy as np
import pygame as pg
from time import time

@njit(fastmath=True, nogil=True)
def ray_cast(maze, distances, wall_types, player_params, render_params):
    player_x, player_y, player_angle = player_params[0], player_params[1], player_params[2]
    fov, dtheta, increment = render_params[0], render_params[1], render_params[2]
    angles = np.arange(player_angle - fov / 2, player_angle + fov / 2, dtheta)

    for i, angle in enumerate(angles):
        x, y = player_x, player_y
        dx, dy = increment * np.cos(angle), increment * np.sin(angle)

        while maze[int(x)][int(y)] == 0:
            x += dx
            y += dy
        
        wall_types[i] = maze[int(x)][int(y)]
        distances[i] = np.sqrt((x - player_x) ** 2 + (y - player_y) ** 2)

def game_loop(screen):
    n = 5
    primordial_maze = maze_generator(n, n)
    maze = maze_padder(primordial_maze)
    # print(maze)

    maze[0][0] = maze[1][0] = maze[0][1] = 2
    maze[2 * n][2 * n] = maze[2 * n][2 * n - 1] = maze[2 * n - 1][2 * n] = 3

    pg.mouse.set_visible(False)
    clock = pg.time.Clock()

    simple_font = pg.font.SysFont('Comic Sans MS', 20)

    player = Player(1.5, 1.5, np.deg2rad(45))

    sky_color = pg.Color(0, 0, 255)
    ground_color = pg.Color(0, 255, 0)
    ground_rect = pg.Rect(0, c.SCREEN_HEIGHT / 2, c.SCREEN_WIDTH, c.SCREEN_HEIGHT / 2)

    normal_wall_color = pg.Color("red")
    start_wall_color = pg.Color("orange")
    end_wall_color = pg.Color("black")

    pg.mouse.set_pos((c.SCREEN_WIDTH / 2, c.SCREEN_HEIGHT / 2))
    mouse_x = c.SCREEN_WIDTH / 2

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
            if event.type == pg.MOUSEMOTION:
                x, y = pg.mouse.get_pos()
                dx = x - mouse_x

                player.look(dx)
                if x > 3 * c.SCREEN_WIDTH / 4:
                    pg.mouse.set_pos((c.SCREEN_WIDTH / 2, y))
                    mouse_x = c.SCREEN_WIDTH / 2
                elif x < c.SCREEN_WIDTH / 4:
                    pg.mouse.set_pos((c.SCREEN_WIDTH / 2, y))
                    mouse_x = c.SCREEN_WIDTH / 2
                else:
                    mouse_x = x

        player.update(keys_pressed, maze)

        distances = np.zeros(c.SCREEN_WIDTH // c.anti_aliasing)
        wall_types = np.zeros(c.SCREEN_WIDTH // c.anti_aliasing)
        ray_cast(maze, distances, wall_types, (player.x, player.y, player.angle), (c.fov, c.dtheta, c.increment))

        screen.fill(sky_color)
        pg.draw.rect(screen, ground_color, ground_rect)

        for i, distance in enumerate(distances):
            height = c.height_multiplier / distance
            wall_color = None
            if wall_types[i] == 1:
                wall_color = normal_wall_color
            elif wall_types[i] == 2:
                wall_color = start_wall_color
            elif wall_types[i] == 3:
                wall_color = end_wall_color
            # else:
            #     wall_color = pg.Color("black")
            
            wall_rect = pg.Rect(i * c.anti_aliasing, c.SCREEN_HEIGHT / 2 - height / 2, c.anti_aliasing, height)
            pg.draw.rect(screen, wall_color, wall_rect)

        fps_display = simple_font.render(f'FPS: {int(clock.get_fps())}', True, pg.Color('white'))
        screen.blit(fps_display, (0, 0))

        pg.display.flip()

        c.set_dt(clock.get_time() / 1000)

if __name__ == '__main__':
    pg.init()
    screen = pg.display.set_mode((0, 0), pg.FULLSCREEN)
    c.init_screen(screen)
    game_loop(screen)