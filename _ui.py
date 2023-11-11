from lib.settings import *


class Mixin:
    @staticmethod
    def alter_start(cell, path):
        if cell:
            path.update_cell("start", cell)

    @staticmethod
    def alter_end(cell, path):
        if cell:
            path.update_cell("end", cell)

    @staticmethod
    def add_walls(cell, path):
        path.update_cell("add", cell)

    @staticmethod
    def remove_walls(cell, path):
        path.update_cell("remove", cell)

    @staticmethod
    def update_colors(grid, path):
        grid.cell_colors[YELLOW] = path.path
        grid.cell_colors[GREEN] = path.start
        grid.cell_colors[RED] = path.end
        grid.cell_colors[BLACK] = path.blocked_points
