import pygame as pg

class Switch:
    """
    Switch module for PyGame. Adds switch to PyGame surface that has an off and on state.
    :param pos: tuple (x, y)
    :param width: int
    :param height: int
    """
    def __init__(self, pos, width, height):
        self.rect = pg.Rect(pos[0], pos[1], width, height)
        self.button_rect = pg.Rect(pos[0], pos[1], width // 2, height)
        self.on_color = (0, 255, 0)
        self.off_color = (150, 150, 150)
        self.border_color = (0, 0, 0)
        self.switch_on = True

    def handle_event(self, event):
        """
        Event handler for switch specific interactions.
        :param event: PyGame event
        :return: None
        """
        if event.type == pg.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.switch_on = not self.switch_on  # flips T/F state
                self.button_rect.x = self.rect.x if self.switch_on else self.rect.x + self.rect.width // 2

    def draw(self, screen):
        """
        Drawing module for switch. Draws the button outline and button itself, along with borders.
        :param screen: PyGame surface
        :return: None
        """
        pg.draw.rect(screen, self.on_color, self.rect)
        pg.draw.rect(screen, self.off_color, self.button_rect)
        pg.draw.rect(screen, self.border_color, self.rect, 1)
        pg.draw.rect(screen, self.border_color, self.button_rect, 1)

    def is_on(self):
        """
        Simple get method to determine if switch is on or off.
        :return: True / False switch state
        """
        return self.switch_on
