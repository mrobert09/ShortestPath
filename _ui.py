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
