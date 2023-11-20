import pygame as pg
from lib.settings import *


class Grid:
    def __init__(self, tile_size, tile_dimensions, offset):
        self.tile_size = tile_size
        self.tile_width, self.tile_height = tile_dimensions
        self.board_width = self.tile_size * self.tile_width
        self.board_height = self.tile_size * self.tile_height
        self.x_offset, self.y_offset = offset
        self.cell_colors = {}  # Color : Cell / set(Cells)

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

    def draw_lines(self, screen, alpha=255):
        """
        Line drawing method for the grid that accepts needs accepts an alpha value. Draws the grid
        on screen. Alpha amount adjusts interior line transparency. Outside edge stays at 255 alpha
        leaving behind a box if grid fully transparent.
        :param screen: PyGame surface
        :param alpha: Transparency amount (0-255)
        :return: None
        """
        # Draw interior lines
        for x in range(self.x_offset + self.tile_size, self.board_width + self.x_offset, self.tile_size):
            pg.draw.line(screen, BLACK + (alpha,), (x, self.y_offset), (x, self.board_height + self.y_offset))
        for y in range(self.y_offset + self.tile_size, self.board_height + self.y_offset, self.tile_size):
            pg.draw.line(screen, BLACK + (alpha,), (self.x_offset, y), (self.board_width + self.x_offset, y))

        # Draw outside edges
        pg.draw.line(screen, BLACK, (self.x_offset, self.y_offset),
                     (self.x_offset, self.board_height + self.y_offset))
        pg.draw.line(screen, BLACK, (self.board_width + self.x_offset, self.y_offset),
                     (self.board_width + self.x_offset, self.board_height + self.y_offset))
        pg.draw.line(screen, BLACK, (self.x_offset, self.y_offset),
                     (self.board_width + self.x_offset, self.y_offset))
        pg.draw.line(screen, BLACK, (self.x_offset, self.board_height + self.y_offset),
                     (self.board_width + self.x_offset, self.board_height + self.y_offset))


    def color_cells(self, screen, draw_path):
        """
        Paints the cells different colors based on their role in the grid.
        :param screen: PyGame surface
        :param draw_path: Shortest path from start to end
        :return: None
        """
        def paint(cell_, color_):
            g_pos = self.global_pos(cell_)
            if g_pos:
                x, y = g_pos
                # Target corner of cell for start of coloring
                x -= self.tile_size / 2
                y -= self.tile_size / 2
                surface = pg.Surface((self.tile_size + 1, self.tile_size + 1))  # prevents border coloring
                surface.fill(color_)
                screen.blit(surface, (x, y))

        for color in self.cell_colors:
            for cell in self.cell_colors[color]:
                if color == YELLOW and not draw_path:  # skips drawing path if switch is off
                    continue
                paint(cell, color)

    def draw(self, screen, draw_surface, alpha, draw_path):
        """
        Draws the grid elements onto the surface.
        :param screen: PyGame surface
        :return: None
        """
        self.color_cells(screen, draw_path)
        self.draw_lines(draw_surface, alpha)


def main():
    pass


if __name__ == '__main__':
    main()
