import arcade
from Main import *

class BasicTile(arcade.Sprite):
    def __init__(self, filename):
        super().__init__(filename=filename, center_x=0, center_y=0, scale=.25)


grass = BasicTile(":resources:images/tiles/grassCenter.png")
map_det = {
    'grass' : grass
}