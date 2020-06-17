#!/usr/bin/env python
import random
import pygame
import cfg


class Actor(pygame.sprite.Sprite):

    def __init__(self, x=0, y=0, x_speed=0, y_speed=0, width=100, height=100):
        super().__init__()
        self.x = x
        self.y = y
        self.x_speed = x_speed
        self.y_speed = y_speed
        self.width = width
        self.height = height
        self.image = self.load_sprite()
        self.rect = self.image.get_rect()

    def hori_accel(self, vel):
        self.x_speed = self.bound(-1 * self.MAX_SPEED, self.x_speed + vel, self.MAX_SPEED)

    def vert_accel(self, vel):
        self.y_speed = self.bound(-1 * self.MAX_SPEED, self.y_speed + vel, self.MAX_SPEED)

    def move(self):
        dest_x = self.x + self.x_speed
        dest_y = self.y - self.y_speed

        self.x = self.bound(0, dest_x, cfg.SCREEN_WIDTH - self.width)
        self.y = self.bound(0, dest_y, cfg.SCREEN_HEIGHT - self.height)
        self.rect.x = self.x
        self.rect.y = self.y

    def die(self):
        print("DEAD!")
        self.kill()

    def get_pos(self):
        return (self.x, self.y)

    def collided_with(self, group):
        return pygame.sprite.spritecollide(self, group, False)

    def load_sprite(self):
        """
        Loads sprite image if get_sprite_name() returns a non-empty value, otherwise draws a circle
        """
        sprite_name = self.get_sprite_name()
        if sprite_name:
            print("sprite name: %s" % sprite_name)
            sprite_img = pygame.image.load("img/%s" % self.get_sprite_name()).convert_alpha()
        else:
            sprite_img = self.draw_circle()
        return pygame.transform.scale(sprite_img, (self.width, self.height))

    def draw_circle(self):
        sprite_img = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        r = (int)(self.width / 2)
        pygame.gfxdraw.filled_circle(sprite_img, r, r, r, self.color)
        return sprite_img

    @staticmethod
    def bound(min_val, val, max_val):
        """
        Returns the value closest to val within the bounds of min_val and max_val
        """
        return max(min_val, min(max_val, val))

    @staticmethod
    def get_sprite_name():
        """
        Override this in your subclass with the name of the img file under img/
        """
        return ""


class Circle(Actor):
    MIN_SIZE = 10
    MAX_SIZE = 60
    MOVE_SPEED = 15
    MAX_SPEED = 50
    MAX_SPEED_SCALING = 3 # A Circle of MIN_SIZE will accelerate at this value * MOVE_SPEED
    DECCEL_FACTOR = 1

    def __init__(self, x=0, y=0, x_speed=0, y_speed=0, size=0, color=cfg.AI_COLOR):
        self.color = color

        if size == 0:
            size = random.randint(self.MIN_SIZE, self.MAX_SIZE)

        # Reduce size range to 0-1 for use in determining acceleration factor
        relative_size = (size - self.MIN_SIZE + 1) / (self.MAX_SIZE - self.MIN_SIZE + 1)
        self.accel_factor = (1 - relative_size) * self.MAX_SPEED_SCALING

        print("New Circle: size: %d, accel: %f" % (size, self.accel_factor))

        super().__init__(x, y, x_speed, y_speed, size, size)

    def vert_accel(self, vel=1):
        super().vert_accel(vel * self.accel_factor)

    def hori_accel(self, vel=1):
        super().hori_accel(vel * self.accel_factor)

    def move(self):
        super().move()
        self.decelerate()

    def decelerate(self):
        if self.x_speed < 0:
            self.x_speed = min(0, self.x_speed + self.DECCEL_FACTOR)
        if self.x_speed > 0:
            self.x_speed = max(0, self.x_speed - self.DECCEL_FACTOR)
        if self.y_speed < 0:
            self.y_speed = min(0, self.y_speed + self.DECCEL_FACTOR)
        if self.y_speed > 0:
            self.y_speed = max(0, self.y_speed - self.DECCEL_FACTOR)


class Player(Circle):
    INIT_SIZE = 30
    # DECCEL_FACTOR = 2

    def __init__(self):
        super().__init__(0, 0, 0, 0, self.INIT_SIZE, cfg.PLAYER_COLOR)
