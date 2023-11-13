import pygame as pg


class Slider:
    def __init__(self, x, y, length, initial_value=0):
        self.x = x
        self.y = y
        self.length = length
        self.handle_radius = 10
        self.dragging = False

        # Calculate initial handle position based on initial value
        self.handle_x = x + (initial_value / 100.0) * length
        self.handle_y = y

    def draw(self, screen):
        # Draw the line
        pg.draw.line(screen, (0, 0, 0), (self.x, self.y), (self.x + self.length, self.y), 5)

        # Draw the handle
        pg.draw.circle(screen, (0, 0, 255), (int(self.handle_x), self.y), self.handle_radius)

    def handle_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            if abs(event.pos[0] - self.handle_x) <= self.handle_radius and \
                    abs(event.pos[1] - self.handle_y) <= self.handle_radius:
                self.dragging = True
        elif event.type == pg.MOUSEBUTTONUP:
            self.dragging = False

    def update(self):
        if self.dragging:
            mouse_x, _ = pg.mouse.get_pos()
            self.handle_x = max(min(mouse_x, self.x + self.length), self.x)

    def get_value(self):
        # Convert handle position to a value between 0 and 100
        return ((self.handle_x - self.x) / self.length) * 100
