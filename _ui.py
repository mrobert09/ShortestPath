from lib.settings import *

class Mixin:
    def alter_start(self, grid, cell, path):
        path.update_cell("start", cell)


    def alter_end(self, grid, cell, path):
        path.update_cell("end", cell)


    def add_walls(self, grid, cell, path):
        path.update_cell("add", cell)


    def remove_walls(self, grid, cell, path):
        path.update_cell("remove", cell)


    def update_colors(self, grid, path):
        grid.cell_colors[GREEN] = path.start
        grid.cell_colors[RED] = path.end
        grid.cell_colors[BLACK] = path.blocked_points
