# Shadowcrest v0.00.100
# by Brett Alexander

from os import path
import pygame as pg
import random
from settings import *
from sprites import *
from platforms import *

class Game():
    def __init__(self):
        # Initialize Game Window, etc.
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode([window_width, window_height])
        pg.display.set_caption(game_name)
        self.clock = pg.time.Clock()
        self.running = True
        self.load_data()

    def new(self):
        # Start New Game
        self.all_sprites = pg.sprite.Group()
        self.platforms = pg.sprite.Group()
        self.player = Player(self)
        self.all_sprites.add(self.player)
        for plat in platform_list:
            p = Platform(*plat)
            self.all_sprites.add(p)
            self.platforms.add(p)
        self.run()

    def run(self):
        # Game Loop
        self.playing = True
        while self.playing:
            self.clock.tick(tickrate)
            self.events()
            self.update()
            self.draw()

    def update(self):
        # Game Loop - Update
        self.all_sprites.update()
        # Collide with Platforms - Only if Falling
        if self.player.vel.y > 0:
            hits = pg.sprite.spritecollide(self.player, self.platforms, False)
            if hits:
                self.player.pos.y = hits[0].rect.top +1
                self.player.vel.y = 0

    def events(self):
        # Game Loop - Events
        for event in pg.event.get():
            # Check for Closing Window
            if event.type == pg.QUIT:
                self.playing = False
                self.running = False

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    self.player.jump()

    def draw(self):
        # Game Loop - Draw
        self.screen.fill(SKY)
        self.all_sprites.draw(self.screen)
        # *After* Drawing everything, Flip the Display
        pg.display.flip()

    def show_titlescreen(self):
        # Game Title Screen
        pass

    def goto_game(self):
        # From Game Title Screen to Gameplay
        pass

    def load_data(self):
        self.dir = path.dirname(__file__)
        img_dir = path.join(self.dir, 'res', 'imgs')
        self.spritesheet = Spritesheet(path.join(img_dir, Player_Spritesheet))


g = Game()
g.show_titlescreen

while g.running:
    g.new()
    g.goto_game()

pg.quit()
