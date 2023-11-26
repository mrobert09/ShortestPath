import pygame as pg

class Button:
    def __init__(self, x, y, width, height, text=''):
        self.on_color = (0, 255, 0)  # Green off_color
        self.off_color = (100, 100, 100)  # Default grey off_color
        self.text = text
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect = pg.Rect(x, y, width, height)
        self.turned_on = True

    def draw(self, surface):
        mouse_pos = pg.mouse.get_pos()
        click = pg.mouse.get_pressed()

        if self.turned_on:
            pg.draw.rect(surface, self.on_color, self.rect)
        else:
            pg.draw.rect(surface, self.off_color, self.rect)

        if self.rect.collidepoint(mouse_pos):
            if self.turned_on:
                pg.draw.rect(surface, self.off_color, self.rect, 2)  # Outline on hover
            else:
                pg.draw.rect(surface, self.on_color, self.rect, 2)
            # if click[0] == 1:
            #     pg.draw.rect(surface, self.on_color, self.rect)  # Fill on click
        # else:
        #     pg.draw.rect(surface, self.off_color, self.rect)

        if self.text:
            font = pg.font.SysFont('Arial', 20)
            text_surface = font.render(self.text, True, (0, 0, 0))  # Black text
            surface.blit(text_surface, (self.x + (self.width - text_surface.get_width()) / 2,
                                    self.y + (self.height - text_surface.get_height()) / 2))

    def handle_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.turned_on = not self.turned_on  # turns button on and off


def main():
    pass


if __name__ == '__main__':
    main()
