import arcade
from GameView import *

class Player(arcade.Sprite):
    def __init__(self, game, filename, x, y, scale=1):
        super().__init__(filename=filename, center_x=x, center_y=y)

        self.health = 100
        self.max_health = self.health
        self.health_bar = HealthBar(game, position = (self.center_x, self.center_y-50))
        self.health_bar.fullness = self.health/self.max_health
    def update(self):
        """ Move the player """
        # Move player.
        # Remove these lines if physics engine is moving player.
        self.center_x += self.change_x
        self.center_y += self.change_y

        self.health_bar.position = self.center_x, self.center_y-50

        # Check for out-of-bounds
        if self.left < 0:
            self.left = 0
        elif self.right > SCREEN_WIDTH - 1:
            self.right = SCREEN_WIDTH - 1

        if self.bottom < 0:
            self.bottom = 0
        elif self.top > SCREEN_HEIGHT - 1:
            self.top = SCREEN_HEIGHT - 1