import pygame as pg
import _ui
from lib.grid import Grid
from lib.settings import *

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
        pg.display.set_caption("Shortest Path")
        self.grid = Grid(TILESIZE, (TILEWIDTH, TILEHEIGHT), (X_OFFSET, Y_OFFSET))
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
            if click[0] and keys[pg.K_LSHIFT]:
                self.grid.add_cell_color(pos, GREEN, 1)
            elif click[2] and keys[pg.K_LSHIFT]:
                self.grid.add_cell_color(pos, RED, 1)
            elif click[0] and not keys[pg.K_LSHIFT]:
                self.grid.add_cell_color(pos, BLACK)
            elif click[2] and not keys[pg.K_LSHIFT]:
                self.grid.add_cell_color(pos, WHITE)

    def update(self):
        """
        Game Loop - Update
        :return:
        """
        self.all_sprites.update()

    def draw(self):
        """
        Game Loop - Draw
        :return:
        """
        self.screen.fill((255, 255, 255))
        self.grid.draw(self.screen)
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
