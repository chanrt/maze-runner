import numpy as np
import pygame as pg

class Constants:
    def __init__(self):
        self.fps = 60
        self.dt = 1 / self.fps

        self.increment = 0.01
        self.anti_aliasing = 3

        self.fov = np.deg2rad(90)
        self.height_multiplier = 400

        self.move_speed = 1
        self.rotate_speed = np.deg2rad(5)

    def set_dt(self, dt):
        self.dt = dt

    def init_screen(self, screen):
        self.screen = screen
        self.SCREEN_WIDTH, self.SCREEN_HEIGHT = self.screen.get_size()

        self.dtheta = (self.fov / self.SCREEN_WIDTH) * self.anti_aliasing

consts = Constants()