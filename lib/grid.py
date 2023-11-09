import pygame as pg

# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GRAY = (133, 133, 133)
PINK = (239, 99, 210)

class Grid:
    def __init__(self, tile_size, tile_width, tile_height, x_offset = 0, y_offset = 0):
        self.tile_size = tile_size
        self.tile_width = tile_width
        self.tile_height = tile_height
        self.board_width = self.tile_size * self.tile_width
        self.board_height = self.tile_size * self.tile_height
        self.x_offset = x_offset
        self.y_offset = y_offset

    def get_cell(self, pos):
        """
        Takes a given pixel coordinate on the screen and returns the cell position on the board.
        :param pos: tuple
        :return: None
        """
        x, y = pos
        x = (x - self.x_offset) / self.tile_size
        y = (y - self.y_offset) / self.tile_size
        if x < 0 or x > self.tile_width or y < 0 or y > self.tile_height:
            return None
        else:
            x, y = int(x), int(y)
            return x, y


    def draw(self, screen):
        """
        Draws the grid onto the surface.
        :param screen: PyGame surface
        :return: None
        """
        for x in range(0 + self.x_offset, self.board_width+1 + self.x_offset, self.tile_size):
            pg.draw.line(screen, BLACK, (x, 0 + self.y_offset), (x, self.board_height + self.y_offset))
        for y in range(0 + self.y_offset, self.board_height+1 + self.y_offset, self.tile_size):
            pg.draw.line(screen, BLACK, (0 + self.x_offset, y), (self.board_width + self.x_offset, y))


def main():
    pass


if __name__ == '__main__':
    main()
