from constants import consts as c

import numpy as np
import pygame as pg

class Player:
    def __init__(self, x, y, angle):
        self.x = x
        self.y = y
        self.angle = angle

        self.front_enabled = False
        self.back_enabled = False
        self.left_enabled = False
        self.right_enabled = False

    def check_collisions(self, maze):
        x, y = self.x + self.cos_nudge, self.y + self.sin_nudge
        if maze[int(x)][int(y)] > 0:
            self.front_enabled = False
        else:
            self.front_enabled = True

        x, y = self.x - self.cos_nudge, self.y - self.sin_nudge
        if maze[int(x)][int(y)] > 0:
            self.back_enabled = False
        else:
            self.back_enabled = True

        x, y = self.x + self.sin_nudge, self.y - self.cos_nudge
        if maze[int(x)][int(y)] > 0:
            self.left_enabled = False
        else:
            self.left_enabled = True

        x, y = self.x - self.sin_nudge, self.y + self.cos_nudge
        if maze[int(x)][int(y)] > 0:
            self.right_enabled = False
        else:
            self.right_enabled = True

    def look(self, dtheta):
        self.angle += dtheta * c.rotate_speed * c.dt

    def update(self, keys_pressed, maze):
        self.cos_nudge, self.sin_nudge = c.move_speed * c.dt * np.cos(self.angle), c.move_speed * c.dt * np.sin(self.angle)
        self.check_collisions(maze)

        if self.front_enabled and (keys_pressed[pg.K_w] or keys_pressed[pg.K_UP]):
            self.x += self.cos_nudge
            self.y += self.sin_nudge
        if self.back_enabled and (keys_pressed[pg.K_s] or keys_pressed[pg.K_DOWN]):
            self.x -= self.cos_nudge
            self.y -= self.sin_nudge
        if self.left_enabled and (keys_pressed[pg.K_a] or keys_pressed[pg.K_LEFT]):
            self.x += self.sin_nudge
            self.y -= self.cos_nudge
        if self.right_enabled and (keys_pressed[pg.K_d] or keys_pressed[pg.K_RIGHT]):
            self.x -= self.sin_nudge
            self.y += self.cos_nudge