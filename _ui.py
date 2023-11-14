import pygame as pg
from lib.settings import *


class Mixin:
    @staticmethod
    def alter_start(cell, path):
        if cell and cell not in path.blocked_points:
            path.update_cell("start", cell)

    @staticmethod
    def alter_end(cell, path):
        if cell and cell not in path.blocked_points:
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

    @staticmethod
    def draw_text(screen, text, color, x, y, font=None):
        if font is None:
            font = pg.font.SysFont(FONT_NAME, FONT_SIZE)
        text = font.render(text, True, color)
        screen.blit(text, (x, y))
