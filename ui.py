import pygame as pg
import _ui
from lib.grid import Grid
from lib.slider import Slider
from lib.switch import Switch
from lib.settings import *
from main import ShortestPath


class UI(_ui.Mixin):
    """
    Instance of PyGame.
    """
    def __init__(self):
        """
        Init
        """
        pg.init()
        pg.display.set_caption("Shortest Path")
        self.clock = pg.time.Clock()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        self.draw_surface = pg.Surface((WIDTH, HEIGHT), pg.SRCALPHA)
        self.sp = ShortestPath((0, 0), (TILEWIDTH - 1, TILEHEIGHT-1), TILEWIDTH, TILEHEIGHT)
        self.grid = Grid(TILESIZE, (TILEWIDTH, TILEHEIGHT), (X_OFFSET, Y_OFFSET))
        self.alpha_slider = Slider((600, 50), 150, 0, 255, initial_value=255)
        # self.alpha_slider_drag = False  # probably not needed, clear soon
        self.tick_slider = Slider((600, 180), 150, 0, 100, initial_value=100)
        # self.tick_slider_drag = False  # probably not needed, clear soon
        self.switch = Switch((625, 100), 100, 25)
        self.text_widgets = []
        self.all_sprites = pg.sprite.Group()
        self.route_freeze = False
        self.playing = True
        self.running = True


    def new(self):
        """
        New Game
        :return:
        """
        self.run()

    def run(self):
        """
        Game Loop
        :return:
        """
        # self.grid.add_cell_color((0, 0), GREEN, 1)
        # self.grid.add_cell_color((TILEWIDTH - 1, TILEHEIGHT - 1), RED, 1)
        while self.playing:
            self.clock.tick(60)
            self.events()
            self.update()
            self.draw()

    def events(self):
        """
        Game Loop - Events
        :return:
        """
        for event in pg.event.get():
            # check for closing window
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False

            pos = pg.mouse.get_pos()
            keys = pg.key.get_pressed()
            click = pg.mouse.get_pressed(3)

            self.alpha_slider.handle_event(event)
            self.switch.handle_event(event)
            self.tick_slider.handle_event(event)

            # Grid event logic
            cell = self.grid.get_cell(pos)
            if not (self.alpha_slider.dragging or self.tick_slider.dragging):
                if click[0] and keys[pg.K_LSHIFT]:
                    if cell and self.tick_slider.get_value() < 100:
                        self.route_freeze = True
                    self.alter_start(cell, self.sp, self.switch.is_on(), self.tick_slider.get_value())
                elif click[2] and keys[pg.K_LSHIFT]:
                    if cell and self.tick_slider.get_value() < 100:
                        self.route_freeze = True
                    self.alter_end(cell, self.sp, self.switch.is_on(), self.tick_slider.get_value())
                elif click[0] and not keys[pg.K_LSHIFT]:
                    if cell and self.tick_slider.get_value() < 100:
                        self.route_freeze = True
                    self.add_walls(cell, self.sp, self.switch.is_on(), self.tick_slider.get_value())
                elif click[2] and not keys[pg.K_LSHIFT]:
                    if cell and self.tick_slider.get_value() < 100:
                        self.route_freeze = True
                    self.remove_walls(cell, self.sp, self.switch.is_on(), self.tick_slider.get_value())
                elif event.type == pg.MOUSEBUTTONDOWN and event.button == 2:
                    self.sp.print_info()
                elif event.type == pg.MOUSEBUTTONUP and (event.button == 1 or event.button == 3):
                    self.route_freeze = False

    def update(self):
        """
        Game Loop - Update
        :return:
        """
        if self.tick_slider.get_value() < 100:
            if not self.route_freeze:
                self.sp.calculate_path_with_ticks(self.tick_slider.get_value())
        else:
            self.sp.calculate_path_with_ticks(100000)
        self.all_sprites.update()
        self.update_colors(self)
        self.update_text(self)
        self.alpha_slider.update()
        self.tick_slider.update()

    def draw(self):
        """
        Game Loop - Draw
        :return:
        """
        self.screen.fill((255, 255, 255))
        self.grid.draw(self.screen, self.draw_surface, self.alpha_slider.get_value(), self.switch.is_on())
        self.screen.blit(self.draw_surface, (0, 0))
        self.alpha_slider.draw(self.screen)
        self.tick_slider.draw(self.screen)
        self.switch.draw(self.screen)
        for surface, text, color, x, y in self.text_widgets:
            self.draw_text(surface, text, color, (x, y))
        self.all_sprites.draw(self.screen)
        # always do last after drawing everything
        pg.display.flip()


def main():
    ui = UI()
    while ui.running:
        ui.new()

    pg.quit()


if __name__ == '__main__':
    main()
