"""
Starting Template

Once you have learned how to use classes, you can begin your program with this
template.

If Python and Arcade are installed, this example can be run from the command line with:
python -m arcade.examples.starting_template
"""
import arcade
from player import *

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Better Move Sprite with Keyboard Example"
SPRITE_SCALING = 0.5
MOVEMENT_SPEED = 5

SIZE_X = 5000
SIZE_Y = 5000
class MyGame(arcade.Window):
    """
    Main application class.

    NOTE: Go ahead and delete the methods you don't need.
    If you do need a method, delete the 'pass' and replace it
    with your own code. Don't leave 'pass' in this program.
    """

    def __init__(self, width, height, title):
        """
        Initializer
        """

        # Call the parent class initializer
        super().__init__(width, height, title)

        # Variables that will hold sprite lists
        self.player_list = None

        # Set up the player info
        self.player_sprite = None

        # Track the current state of what key is pressed
        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False


        self.Enemies = arcade.SpriteList()
        self.OpenToEnemies = []
        self.EnemyMap = {}

        # Set the background color
        arcade.set_background_color(arcade.color.AMAZON)

    def setup(self):
        """ Set up the game and initialize the variables. """

        # Sprite lists
        self.player_list = arcade.SpriteList()

        # Set up the player
        self.player_sprite = Player(":resources:images/animated_characters/female_person/femalePerson_idle.png",
                                    SPRITE_SCALING)
        self.player_sprite.center_x = 50
        self.player_sprite.center_y = 50
        self.player_list.append(self.player_sprite)

    def on_draw(self):
        """ Render the screen. """

        # Clear the screen
        arcade.start_render()

        # Draw all the sprites.
        self.player_list.draw()

        # Call draw() on all your sprite lists below
    def update_player_speed(self):

        # Calculate speed based on the keys pressed
        self.player_sprite.change_x = 0
        self.player_sprite.change_y = 0

        if self.up_pressed and not self.down_pressed:
            self.player_sprite.change_y = MOVEMENT_SPEED
        elif self.down_pressed and not self.up_pressed:
            self.player_sprite.change_y = -MOVEMENT_SPEED
        if self.left_pressed and not self.right_pressed:
            self.player_sprite.change_x = -MOVEMENT_SPEED
        elif self.right_pressed and not self.left_pressed:
            self.player_sprite.change_x = MOVEMENT_SPEED

    def on_update(self, delta_time):
        """
        All the logic to move, and the game logic goes here.
        Normally, you'll call update() on the sprite lists that
        need it.
        """
        self.player_list.update()

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. """

        if key == arcade.key.UP:
            self.up_pressed = True
            self.update_player_speed()
        elif key == arcade.key.DOWN:
            self.down_pressed = True
            self.update_player_speed()
        elif key == arcade.key.LEFT:
            self.left_pressed = True
            self.update_player_speed()
        elif key == arcade.key.RIGHT:
            self.right_pressed = True
            self.update_player_speed()

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key. """

        if key == arcade.key.UP:
            self.up_pressed = False
            self.update_player_speed()
        elif key == arcade.key.DOWN:
            self.down_pressed = False
            self.update_player_speed()
        elif key == arcade.key.LEFT:
            self.left_pressed = False
            self.update_player_speed()
        elif key == arcade.key.RIGHT:
            self.right_pressed = False
            self.update_player_speed()

    def on_mouse_motion(self, x, y, delta_x, delta_y):
        """
        Called whenever the mouse moves.
        """
        pass

    def on_mouse_press(self, x, y, button, key_modifiers):
        """
        Called when the user presses a mouse button.
        """
        pass

    def on_mouse_release(self, x, y, button, key_modifiers):
        """
        Called when a user releases a mouse button.
        """
        pass

    def generateEnemySpawner(self, width, length):

        width *= 50
        length *= 50
        self.EnemyMap = {}

        #NOTE: UNCOMMENT everything with SnowMap to visualize where enemies spawn
        #self.SnowMap = {}
        self.OpenToEnemies = []
        x = 0
        y = 0
        while x <= width:
            self.EnemyMap[x] = {}
            #self.SnowMap[x] = {}
            while y <= length:
                self.EnemyMap[x][y] = 0
                #self.SnowMap[x][y] = 0
                y += 50

            y = 0
            x += 50
    def EnemySpawnPos(self):
        if len(self.OpenToEnemies) > 0:
            random_num = random.randrange(0, len(self.OpenToEnemies))
            return self.OpenToEnemies[random_num][0], self.OpenToEnemies[random_num][1]
        elif len(self.People) > 0:
            person = self.People[random.randrange(0, len(self.People))]
            return person.center_x, person.center_y
        elif self.population == 0:
            self.End()
        #elif len(self.Boats) > 0:
        #    boat = self.Boats[random.randrange(0, len(self.Boats))]
        #    return boat.center_x, boat.center_y
        raise ReferenceError("BUG: Either no People in Spritelist or No place open to enemies")
    def BuildingChangeEnemySpawner(self, x, y, placing=1, min_dist=100, max_dist= 300):
        #NOTE: Placing=-1 is for destroying, keep at 1 if placing
        x = round(x/50)*50
        y = round(y/50)*50

        for x2 in range(-max_dist, max_dist, 50):
            if not 0 <= x2+x < SIZE_X:
                continue
            for y2 in range(-max_dist, max_dist, 50):
                if not 0 <= y2+y < SIZE_Y:
                    continue

                x1 = x2+x
                y1 = y2+y
                
                
                if abs(x2)<=min_dist and abs(y2)<=min_dist:
                    self.EnemyMap[x1][y1] -= placing
                    #self.SnowMap[x1][y1] += placing
                else:
                    self.EnemyMap[x1][y1] += placing
    
                #NOTE: UPDATE open to Enemies list
                if self.EnemyMap[x1][y1] > 0:
                    if not (x1, y1) in self.OpenToEnemies:
                        self.OpenToEnemies.append((x1, y1))
                elif (x1, y1) in self.OpenToEnemies:
                    self.OpenToEnemies.remove((x1, y1))
                
                
                """ 
                Snow = self.SnowMap[x1][y1]

                land = arcade.get_sprites_at_point((x1, y1), self.Lands)
                if not land:
                    pass
                elif Snow < 1 and land[0].typ == "Snow":
                    land[0].texture = land[0].prev_texture
                    land[0].typ = land[0].prev_typ
                elif Snow >= 1 and land[0].typ != "Snow":
                    land[0].prev_texture = land[0].texture
                    land[0].prev_typ = land[0].typ
                    land[0].typ = "Snow"
                    #gul-li-ble person
                    land[0].texture = arcade.load_texture("resources/Sprites/Snow.png")
                 """



def main():
    """ Main function """
    game = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()