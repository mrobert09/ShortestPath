import pygame as pg


class Slider:
    """
    Slider module for PyGame. Adds a horizontal slider to the screen at position (x, y) with user defined length.

    Has default attributes of a minimum value of 0, max value of 100, and initial value of 0.
    """
    def __init__(self, pos, length, min_value=0, max_value=100, initial_value=0):
        self.x = pos[0]
        self.y = pos[1]
        self.length = length
        self.handle_radius = 10
        self.min_value = min_value
        self.max_value = max_value
        if self.min_value > self.max_value:
            raise self.InvalidMinMax()
        self.dragging = False
        self.line_thickness = 5
        self.line_color = (0, 0, 0)
        self.handle_color = (0, 0, 255)

        # Calculate initial handle position based on initial value
        self.initial_value = max(min(initial_value, max_value), min_value)
        proportion = (initial_value - self.min_value) / (self.max_value - self.min_value)
        self.handle_x = self.x + proportion * self.length
        self.handle_y = self.y

    def draw(self, screen):
        """
        Method for drawing the slider to the screen each frame.
        :param screen: PyGame surface
        :return: None
        """
        # Slider
        pg.draw.line(screen, self.line_color, (self.x, self.y), (self.x + self.length, self.y), self.line_thickness)
        # Handle
        pg.draw.circle(screen, self.handle_color, (int(self.handle_x), self.y), self.handle_radius)

    def handle_event(self, event):
        """
        Event handler for slider specific interactions.
        :param event: PyGame event
        :return: None
        """
        if event.type == pg.MOUSEBUTTONDOWN:
            # Check if mouse is inside radius of handle
            if abs(event.pos[0] - self.handle_x) <= self.handle_radius and \
                    abs(event.pos[1] - self.handle_y) <= self.handle_radius:
                self.dragging = True
        elif event.type == pg.MOUSEBUTTONUP:
            self.dragging = False

    def update(self):
        """
        Updates the location of the handle on the slider each frame.
        :return: None
        """
        if self.dragging:
            mouse_x, _ = pg.mouse.get_pos()
            # min() prevents handle from going past end of the line (self.x + self.length)
            # max() prevents handle from going below start of the line (self.x)
            self.handle_x = max(min(mouse_x, self.x + self.length), self.x)

    def get_value(self):
        """
        Get method for retrieving the current value of the slider based on handle position.
        :return:
        """
        # Calculate the proportional position of the handle
        proportional_position = (self.handle_x - self.x) / self.length

        # Map the proportional position to the value range
        value_range = self.max_value - self.min_value
        value = proportional_position * value_range + self.min_value

        return int(value)

    class InvalidMinMax(Exception):
        """
        Exception raised if minimum value for slider is greater than the maximum value.
        """
        def __init__(self):
            super().__init__("Minimum value must be less than maximum value.")
