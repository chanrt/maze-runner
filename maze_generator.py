import numpy as np
import pygame as pg
from random import choice, randint


class Cell:
    def __init__(self, i, j):
        self.i = i
        self.j = j
        
        self.was_visited = False
        # up, right, down, left
        self.walls = [True, True, True, True]

    def set_visited(self):
        self.was_visited = True


def maze_padder(maze):
    n = len(maze)
    padded_maze = np.ones((2 * n + 1, 2 * n + 1))
    
    for i in range(len(maze)):
        for j in range(len(maze[i])):
            corr_i = 2 * i + 1
            corr_j = 2 * j + 1
            padded_maze[corr_i][corr_j] = 0
            if not maze[i][j].walls[0]:
                padded_maze[corr_i - 1][corr_j] = 0
            if not maze[i][j].walls[1]:
                padded_maze[corr_i][corr_j + 1] = 0
            if not maze[i][j].walls[2]:
                padded_maze[corr_i + 1][corr_j] = 0
            if not maze[i][j].walls[3]:
                padded_maze[corr_i][corr_j - 1] = 0

    return padded_maze

def maze_renderer(maze):
    cell_width = 20
    thickness = 3
    screen = pg.display.set_mode((len(maze[0]) * cell_width, len(maze) * cell_width))

    bg_color = pg.Color("black")
    wall_color = pg.Color("white")

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    pg.quit()
                    quit()
        
        screen.fill(bg_color)

        for i in range(len(maze)):
            for j in range(len(maze[i])):
                if maze[i][j].walls[0]:
                    pg.draw.line(screen, wall_color, (j * cell_width, i * cell_width), ((j + 1) * cell_width, i * cell_width), thickness)
                if maze[i][j].walls[1]:
                    pg.draw.line(screen, wall_color, ((j + 1) * cell_width, i * cell_width), ((j + 1) * cell_width, (i + 1) * cell_width), thickness)
                if maze[i][j].walls[2]:
                    pg.draw.line(screen, wall_color, ((j + 1) * cell_width, (i + 1) * cell_width), (j * cell_width, (i + 1) * cell_width), thickness)
                if maze[i][j].walls[3]:
                    pg.draw.line(screen, wall_color, (j * cell_width, (i + 1) * cell_width), (j * cell_width, i * cell_width), thickness)

        pg.display.flip()            
    

def maze_generator(width, height):
    maze = []

    for i in range(height):
        maze_row = []
        for j in range(width):
            maze_row.append(Cell(i, j))
        maze.append(maze_row)

    init_i, init_j = randint(0, height - 1), randint(0, width - 1)
    maze[init_i][init_j].set_visited()

    stack = [(init_i, init_j)]

    while len(stack) > 0:
        current_cell = stack.pop()
        i, j = current_cell[0], current_cell[1]

        empty_neighbors = []
        if i - 1 > -1 and maze[i-1][j].was_visited == False:
            empty_neighbors.append((i-1, j))
        if i + 1 < height and maze[i+1][j].was_visited == False:
            empty_neighbors.append((i+1, j))
        if j - 1 > -1 and maze[i][j-1].was_visited == False:
            empty_neighbors.append((i, j-1))
        if j + 1 < width and maze[i][j+1].was_visited == False:
            empty_neighbors.append((i, j+1))

        if len(empty_neighbors) > 0:
            stack.append((i, j))
            chosen_cell = choice(empty_neighbors)
            i_new, j_new = chosen_cell[0], chosen_cell[1]

            if i == i_new:
                if j < j_new:
                    maze[i][j].walls[1] = False
                    maze[i_new][j_new].walls[3] = False
                else:
                    maze[i][j].walls[3] = False
                    maze[i_new][j_new].walls[1] = False
            elif j == j_new:
                if i < i_new:
                    maze[i][j].walls[2] = False
                    maze[i_new][j_new].walls[0] = False
                else:
                    maze[i][j].walls[0] = False
                    maze[i_new][j_new].walls[2] = False

            maze[i_new][j_new].set_visited()
            stack.append((i_new, j_new))

    return maze

if __name__ == '__main__':
    n = 5
    maze = maze_generator(n, n)
    padded_maze = maze_padder(maze)
    print(padded_maze)
    maze_renderer(maze)