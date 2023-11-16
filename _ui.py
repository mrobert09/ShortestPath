import pygame as pg
from lib.settings import *


class Mixin:
    @staticmethod
    def alter_start(cell, path, show_path):
        """
        Static method used for updating starting cell location.
        :param cell: tuple
        :param path: ShortestPath algorithm
        :param show_path: Bool - True if yellow path is turned on, False if not
        :return: None
        """
        if cell and cell not in path.blocked_points:
            path.update_cell("start", cell)
            if show_path:
                path.calculate_path()

    @staticmethod
    def alter_end(cell, path, show_path):
        """
        Static method used for updating ending cell location.
        :param cell: tuple
        :param path: ShortestPath algorithm
        :param show_path: Bool - True if yellow path is turned on, False if not
        :return: None
        """
        if cell and cell not in path.blocked_points:
            path.update_cell("end", cell)
            if show_path:
                path.find_path(cell)

    @staticmethod
    def add_walls(cell, path, show_path):
        """
        Static method used for adding cells as walls.
        :param cell: tuple
        :param path: ShortestPath algorithm
        :param show_path: Bool - True if yellow path is turned on, False if not
        :return: None
        """
        path.update_cell("add", cell)
        if show_path:
            path.calculate_path()

    @staticmethod
    def remove_walls(cell, path, show_path):
        """
        Static method used for removing cells as walls.
        :param cell: tuple
        :param path: ShortestPath algorithm
        :param show_path: Bool - True if yellow path is turned on, False if not
        :return: None
        """
        path.update_cell("remove", cell)
        if show_path:
            path.calculate_path()

    @staticmethod
    def update_colors(app):
        """
        Static method used to update colors of cells based on their role.
        :param app: Main UI instance
        :return: None
        """
        app.grid.cell_colors[YELLOW] = app.sp.path
        app.grid.cell_colors[GREEN] = app.sp.start
        app.grid.cell_colors[RED] = app.sp.end
        app.grid.cell_colors[BLACK] = app.sp.blocked_points

    @staticmethod
    def update_text(app):
        """
        Static method used to update text widgets.
        :param app: Main PyGame application
        :return: None
        """
        text_widgets = []
        text_widgets.append((app.screen, "Grid Alpha", BLACK, 640, 20))
        # text_widgets.append((app.screen, str(app.slider.get_value()), BLACK, 665, 60))
        text_widgets.append((app.screen, "Display Path", BLACK, 628, 120))
        # text_widgets.append((app.screen, str(app.switch.is_on()), BLACK, 630, 150))

        app.text_widgets = text_widgets

    @staticmethod
    def draw_text(screen, text, color, pos, font=None):
        """
        Static method used to draw text to a surface.
        :param screen: PyGame surface
        :param text: string
        :param color: tuple (0-255, 0-255, 0-255)
        :param pos: tuple location (x, y)
        :param font: font type
        :return: None
        """
        if font is None:
            font = pg.font.SysFont(FONT_NAME, FONT_SIZE)
        text = font.render(text, True, color)
        screen.blit(text, pos)
