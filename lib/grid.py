import pygame as pg
from lib.settings import *

class Grid:
    def __init__(self, tile_size, tile_dimensions, offset):
        self.tile_size = tile_size
        self.tile_width, self.tile_height = tile_dimensions
        self.board_width = self.tile_size * self.tile_width
        self.board_height = self.tile_size * self.tile_height
        self.x_offset, self.y_offset = offset
        # organized by cells
        self.cell_colors = {}
        # organized by colors
        self.unique_colored_cells = {}

    def get_cell(self, pos):
        """
        Takes a given pixel coordinate on the screen and returns the cell position on the board.
        :param pos: tuple
        :return: Relative cell position or None
        """
        x, y = pos
        x = (x - self.x_offset) / self.tile_size
        y = (y - self.y_offset) / self.tile_size
        if x <= 0 or x >= self.tile_width or y <= 0 or y >= self.tile_height:
            return None
        else:
            x, y = int(x), int(y)
            return x, y


    def global_pos(self, cell):
        """
        Opposite of cell_pos method, converts a cell grid position to it's center pixel.
        :param cell: tuple
        :return: Global pixel position of cell
        """
        if cell:  # does not attempt to convert when cell is None
            x, y = cell
            x = x * self.tile_size + self.x_offset + self.tile_size/2
            y = y * self.tile_size + self.y_offset + self.tile_size/2
            return x, y


    def add_cell_color(self, cell, color, unique=0):
        if unique:
            if color in self.unique_colored_cells.keys():
                self.unique_colored_cells.pop(color)
            self.unique_colored_cells[color] = cell
        else:
            self.cell_colors[cell] = color


    def draw_lines(self, screen):
        for x in range(0 + self.x_offset, self.board_width+1 + self.x_offset, self.tile_size):
            pg.draw.line(screen, BLACK, (x, 0 + self.y_offset), (x, self.board_height + self.y_offset))
        for y in range(0 + self.y_offset, self.board_height+1 + self.y_offset, self.tile_size):
            pg.draw.line(screen, BLACK, (0 + self.x_offset, y), (self.board_width + self.x_offset, y))


    def color_cells(self, screen):
        def color(cell, color):
            g_pos = self.global_pos(cell)
            if g_pos:
                x, y = g_pos
                # Target corner of cell for start of coloring
                x -= self.tile_size / 2
                y -= self.tile_size / 2
                surface = pg.Surface((self.tile_size - 1, self.tile_size - 1)) # prevents border coloring
                surface.fill(color)
                screen.blit(surface, (x + 1, y + 1))

        for cell in self.cell_colors:
            color(cell, self.cell_colors[cell])

        for unique_color in self.unique_colored_cells:
            color(self.unique_colored_cells[unique_color], unique_color)


    def draw(self, screen):
        """
        Draws the grid elements onto the surface.
        :param screen: PyGame surface
        :return: None
        """
        self.draw_lines(screen)
        self.color_cells(screen)


def main():
    pass


if __name__ == '__main__':
    main()
