# Shadowcrest v0.00.100
# by Brett Alexander

import pygame as pg
from settings import *

vec = pg.math.Vector2

class Spritesheet():
    def __init__(self, filename):
        self.spritesheet = pg.image.load(filename).convert()

    def get_image(self, x, y, width, height):
        image = pg.Surface([width, height])
        image.blit(self.spritesheet, (0, 0), (x, y, width, height))
        image = pg.transform.scale(image, (width, height))
        return image

class Player(pg.sprite.Sprite):
    def __init__(self, game):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.walking = False
        self.jumping = False
        self.current_frame = 0
        self.last_update = 0
        self.load_images()
        self.image = self.stand_frame_r[0]
        self.rect = self.image.get_rect()
        self.rect.center = (window_width/2, window_height/2)
        self.pos = vec(window_width/2, window_height/2)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)

    def load_images(self):
        # load animation sprites
        # standing anims
        self.stand_frame_r = [self.game.spritesheet.get_image(68, 422, 66, 82)]
        self.stand_frame_l = []
        for frame in self.stand_frame_r:
            frame.set_colorkey(BLACK)
            self.stand_frame_l.append(pg.transform.flip(frame, True, False))
        # walk anims
        self.walk_frames_r = [self.game.spritesheet.get_image(0, 339, 68, 83),
                                self.game.spritesheet.get_image(0, 0, 70, 86)]
        self.walk_frames_l = []
        for frame in self.walk_frames_r:
            frame.set_colorkey(BLACK)
            self.walk_frames_l.append(pg.transform.flip(frame, True, False))
        # jump anims
        self.jump_frame_r = [self.game.spritesheet.get_image(68, 339, 67, 83)]
        self.jump_frame_l = []
        for frame in self.jump_frame_r:
            frame.set_colorkey(BLACK)
            self.jump_frame_l.append(pg.transform.flip(frame, True, False))

    def jump(self):
        # Jump only if Standing on Platform
        self.rect.x +=1
        hits = pg.sprite.spritecollide(self, self.game.platforms, False)
        self.rect.x -= 1
        if hits:
            self.vel.y = -13

    def update(self):
        self.animate()
        self.acc = vec(0, player_gravity)

        # Player Movement
        keys = pg.key.get_pressed()
        if keys[pg.K_a]:
            self.acc.x = -player_acc
        if keys[pg.K_d]:
            self.acc.x = player_acc

        # Player Physics
        self.acc.x += self.vel.x * player_friction
        self.vel += self.acc
        if abs(self.vel.x) < 0.1:
            self.vel.x = 0
        self.pos += self.vel + 0.5 * self.acc

        # Prevent Player from going Off Screen
        if (self.pos.x > window_width-player_width/2):
            self.pos.x = window_width-player_width/2
        if self.pos.x < player_width/2:
            self.pos.x = 15

        self.rect.midbottom = self.pos

    def animate(self):
        now = pg.time.get_ticks()
        if self.vel.x != 0 and self.vel.y == 0:
            self.walking = True
            self.jumping = False
        elif self.vel.y != 0:
            self.walking = False
            self.jumping = True
        else:
            self.walking = False
            self.jumping = False


        if self.walking:
            if now - self.last_update > 125:
                self.last_update = now
                self.current_frame = (self.current_frame+1) % len(self.walk_frames_l)
                bottom = self.rect.bottom
                if self.vel.x > 0:
                    self.image = self.walk_frames_r[self.current_frame]
                else:
                    self.image = self.walk_frames_l[self.current_frame]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom

        if self.jumping:
            if now - self.last_update > 125:
                self.last_update = now
                self.current_frame = (self.current_frame+1) % len(self.jump_frame_l)
                if self.vel.x > 0 and self.vel.y != 0:
                    self.image = self.jump_frame_r[self.current_frame]
                elif self.vel.x == 0 and self.vel.y != 0:
                    self.image = self.jump_frame_r[self.current_frame]
                elif self.vel.x < 0 and self.vel.y != 0:
                    self.image = self.jump_frame_l[self.current_frame]

        if not self.jumping and not self.walking:
            self.image = self.stand_frame_r[0]

class Platform(pg.sprite.Sprite):
    def __init__(self, x, y, w, h):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface([w, h])
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        pass
