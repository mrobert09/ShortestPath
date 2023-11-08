import pygame as pg
import _ui

class UI(_ui.Mixin):
    """
    Instance of PyGame.
    """

    def __init__(self):
        """
        Init
        """
        pg.init()
        self.cells = self.create_cells(100, 3)
        self.screen = pg.display.set_mode((300, 300))
        pg.display.set_caption("Shortest Path")
        self.clock = pg.time.Clock()
        self.running = True


    def new(self):
        """
        New Game
        :return:
        """
        self.all_sprites = pg.sprite.Group()
        self.run()


    def run(self):
        """
        Game Loop
        :return:
        """
        self.playing = True
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
        self.draw_grid(self.cells, self.screen)
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
