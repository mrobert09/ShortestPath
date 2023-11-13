import pygame as pg
import _ui
from lib.grid import Grid
from lib.slider import Slider
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
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        self.sp = ShortestPath((0, 0), (TILEWIDTH - 1, TILEHEIGHT-1), TILEWIDTH, TILEHEIGHT)
        pg.display.set_caption("Shortest Path")
        self.grid = Grid(TILESIZE, (TILEWIDTH, TILEHEIGHT), (X_OFFSET, Y_OFFSET))
        self.slider = Slider(600, 50, 150)
        self.slider_drag = False
        self.clock = pg.time.Clock()
        self.running = True
        self.playing = True
        self.all_sprites = pg.sprite.Group()

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
            self.clock.tick(1000)
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

            self.slider.handle_event(event)

            # Grid event logic
            cell = self.grid.get_cell(pos)
            if click[0] and keys[pg.K_LSHIFT]:
                self.alter_start(cell, self.sp)
            elif click[2] and keys[pg.K_LSHIFT]:
                self.alter_end(cell, self.sp)
            elif click[0] and not keys[pg.K_LSHIFT]:
                self.add_walls(cell, self.sp)
            elif click[2] and not keys[pg.K_LSHIFT]:
                self.remove_walls(cell, self.sp)
            elif event.type == pg.MOUSEBUTTONDOWN and event.button == 2:
                self.sp.print_info()

            # # Slider event logic
            # if event.type == pg.MOUSEBUTTONDOWN:
            #     self.slider_drag = self.slider.slider_clicked(pos)
            #     if self.slider_drag:
            #         mouse_x, _ = pg.mouse.get_pos()
            #         self.slider.handle_x = max(min(mouse_x, self.slider.slider_x + self.slider.slider_length),
            #                                    self.slider.slider_x)
            # if event.type == pg.MOUSEBUTTONUP:
            #     self.slider_drag = False



    def update(self):
        """
        Game Loop - Update
        :return:
        """
        self.all_sprites.update()
        self.sp.calculate_path()
        self.update_colors(self.grid, self.sp)
        self.slider.update()

    def draw(self):
        """
        Game Loop - Draw
        :return:
        """
        self.screen.fill((255, 255, 255))
        self.grid.draw(self.screen)
        self.slider.draw(self.screen)
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
