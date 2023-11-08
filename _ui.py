import pygame as pg


class Mixin:
    def create_cells(self, cell_size, count):
        """Create the 3x3 area of cells within the window"""
        cells = []
        for i in range(count):
            row = []
            for j in range(count):
                x = j * cell_size
                y = i * cell_size
                rect = pg.Rect(x, y, cell_size, cell_size)
                row.append(rect)
            cells.append(row)

        return cells


    def draw_grid(self, cells, screen):
        for row in cells:
            for cell in row:
                pg.draw.rect(screen, (0, 0, 0), cell, 1)  # draw a 1-pixel black border around each cell
                pg.draw.line(screen, (0, 0, 0), (cell.x, cell.y), (cell.x + cell.w, cell.y))  # draw a horizontal line
                pg.draw.line(screen, (0, 0, 0), (cell.x, cell.y), (cell.x, cell.y + cell.h))  # draw a vertical line