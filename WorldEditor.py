import arcade, os, sys
import json
from Player import PlayerSprite
from Enemys import Land, Vampire, Maggot, Turret
  

dictionary = {}
class MyEditor(arcade.Window):
    """ Main application class. """
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        arcade.set_background_color(arcade.csscolor.CORNFLOWER_BLUE)

        #create sprite lists
        #also nothing should move/have gravity so don't 
        #change use_spatial_hash or is_static(objects like tiles are to be
        #deleted instead of moved for simplicity) only the player will move.
        self.Lands = arcade.SpriteList(use_spatial_hash=True, is_static=True)
        self.Blocks = arcade.SpriteList(use_spatial_hash=True, is_static=True)
        
        #to localize mouse position
        self.x = 0
        self.y = 0
        self.change_x = 0
        self.change_y = 0
        self.last = None

        self.camera = arcade.Camera(self.width, self.height)
        self.load()

    def on_draw(self):
        """Render the screen."""

        arcade.start_render()
        self.camera.use()
        self.Lands.draw()
        self.player.draw()
        self.Blocks()

    def on_key_press(self, key: int, modifiers: int):
        #move camera
        if key == arcade.key.LEFT or key == arcade.key.A:
            self.x -= 50
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.x += 50
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.y -= 50
        elif key == arcade.key.UP or key == arcade.key.W:
            self.y += 50
        elif key == arcade.key.E:
            if self.last.flipped_diagonally == False and self.last.flipped_vertically == False:
                self.last.flipped_diagonally = True
            elif self.last.flipped_diagonally == True and self.last.flipped_vertically == False:
                self.last.flipped_diagonally = False
                self.last.flipped_vertically = True
            elif self.last.flipped_diagonally == False and self.last.flipped_vertically == True:
                self.last.flipped_horizontally = True
                self.last.flipped_diagonally = True
            elif self.last.flipped_diagonally == True and self.last.flipped_vertically == True:
                self.last.flipped_diagonally = False
                self.last.flipped_vertically = False
                self.last.flipped_horizontally = False

            self.last.change()
        #save and quite
        elif key == arcade.key.Q:
            self.save()
            arcade.close_window()
        #checks if number or key is pressed
        elif key in self.numlist:
            self.num = key
        elif key in self.keylist:
            self.key = key
        
    def on_update(self, delta_time: float):
        self.camera.move_to((self.x, self.y))

    def load(self):
        with open("WorldFile.json", "r") as read_file:
            World = json.load(read_file)

        #Retrieve value's from dict and restores them as objects

        #create tiles
        for cord in World["land"]:
            self.Lands.append(Land(cord[0], cord[1]))
        #create enemys
        for cord in World["turret"]:
            self.Turrets.append(Turret(cord[0], cord[1], flipped_vertically=cord[2], flipped_horizontally=cord[3], flipped_diagonally=cord[4]))
        #create player
        if World["player"] is not None:
            self.player = PlayerSprite(1, World["player"][0], World["player"][1])
        else:
            self.player = PlayerSprite(self, 1, 500, 500)

    #saves values of objects since json doesn't support object saving
    def save(self):
        with open("WorldFile.json", "w") as write_file:
            #saves using list comprehension to save value's in a tuple
            cords = [(land.center_x, land.center_y) for land in self.Lands]
            Turret_cords = [(turret.center_x, turret.center_y, turret.flipped_vertically, turret.flipped_horizontally, turret.flipped_diagonally) for turret in self.Turrets]
            player_cords = int(self.player.center_x), int(self.player.center_y)

            #Stores each list of value's in a dict to make it easy to retrieve
            json.dump({"land":cords, "blocks":block_cords, "player":player_cords}, write_file)


    #Where is it pressed
    def on_mouse_press(self, x, y, button, modifiers):
        #all calculations in on_mouse_press are to round until
        #AddObj function
        start_x = self.x
        start_y = self.y

        x += start_x
        y += start_y


        x = x/50
        x = round(x)
        x *= 50

        y = y/50
        y = round(y)
        y *= 50

        if button == arcade.MOUSE_BUTTON_LEFT:

            #AddObj function checks and sets object
            self.AddObj(x, y)

        elif button == arcade.MOUSE_BUTTON_RIGHT:
            [land.remove_from_sprite_lists() for land in self.Lands if land.center_x == x and land.center_y == y]
            [block.remove_from_sprite_lists() for block in self.Blocks if block.center_x == x and block.center_y == y]
    def AddObj(self, x, y):
        obj = dictionary[self.tile](x, y)
        if self.typ == "Land":
            self.Lands.append(obj)
        else:
            self.Blocks.append(obj)

        if self.num == self.numlist[0]:#if num == 1: basicly
            self.player.center_x = x
            self.player.center_y = y
        

        print(self.num, self.key, arcade.key.L)
        
        
Editor = MyEditor(1000, 1000, "MyEditor")
arcade.run()