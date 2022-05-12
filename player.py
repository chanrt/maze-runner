

from re import X
from constants import consts as c

import numpy as np
import pygame as pg

class Player:
    def __init__(self, x, y, angle):
        self.x = x
        self.y = y
        self.angle = angle

    def update(self, keys_pressed):
        if keys_pressed[pg.K_w] or keys_pressed[pg.K_UP]:
            self.x += c.move_speed * np.cos(self.angle) * c.dt
            self.y += c.move_speed * np.sin(self.angle) * c.dt
        if keys_pressed[pg.K_s] or keys_pressed[pg.K_DOWN]:
            self.x -= c.move_speed * np.cos(self.angle) * c.dt
            self.y -= c.move_speed * np.sin(self.angle) * c.dt
        if keys_pressed[pg.K_a] or keys_pressed[pg.K_LEFT]:
            self.x += c.move_speed * np.sin(self.angle) * c.dt
            self.y -= c.move_speed * np.cos(self.angle) * c.dt
        if keys_pressed[pg.K_d] or keys_pressed[pg.K_RIGHT]:
            self.x -= c.move_speed * np.sin(self.angle) * c.dt
            self.y += c.move_speed * np.cos(self.angle) * c.dt
        if keys_pressed[pg.K_q]:
            self.angle -= c.rotate_speed * c.dt
        if keys_pressed[pg.K_e]:
            self.angle += c.rotate_speed * c.dt