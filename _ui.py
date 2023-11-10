import pygame as pg
from lib.settings import *

class Mixin:
    def alter_start(self, grid, cell, path):
        grid.add_cell_color(cell, GREEN, 1)
        path.update_cell("start", cell)

    def alter_end(self, grid, cell, path):
        grid.add_cell_color(cell, RED, 1)
        path.update_cell("end", cell)

    def add_walls(self, grid, cell, path):
        grid.add_cell_color(cell, BLACK)
        path.update_cell("add", cell)

    def remove_walls(self, grid, cell, path):
        grid.add_cell_color(cell, WHITE)
        path.update_cell("remove", cell)
