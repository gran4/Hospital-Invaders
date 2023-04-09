"""
Starting Template

Once you have learned how to use classes, you can begin your program with this
template.

If Python and Arcade are installed, this example can be run from the command line with:
python -m arcade.examples.starting_template
"""
import arcade
from player import *
from Enemy import *
from Components import *
from MyPathfinding import *

SCREEN_WIDTH = 1440
SCREEN_HEIGHT = 800
SCREEN_TITLE = "Better Move Sprite with Keyboard Example"
SPRITE_SCALING = 0.5
MOVEMENT_SPEED = 5

SIZE_X = 5000
SIZE_Y = 5000
class MyGame(arcade.View):
    """
    Main application class.

    NOTE: Go ahead and delete the methods you don't need.
    If you do need a method, delete the 'pass' and replace it
    with your own code. Don't leave 'pass' in this program.
    """

    def __init__(self, menu, width, height, title):
        """
        Initializer
        """

        # Call the parent class initializer
        super().__init__()
        self.menu = menu

        # Variables that will hold sprite lists
        self.player_list = None

        # Set up the player info
        self.player_sprite = None

        # Track the current state of what key is pressed
        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False
        self.hospital = arcade.Sprite(filename="hospital.png", center_x=1440, center_y=800, scale=2)



         # Set the background color
        arcade.set_background_color(arcade.color.AMAZON)
        self.population = 2000

        self.generate_world()

        self.setup()
    def setup(self):
        """ Set up the game and initialize the variables. """

        # Sprite lists
        self.player_list = arcade.SpriteList()


        self.Enemies = arcade.SpriteList()
        self.OpenToEnemies = [(0, 0)]
        self.EnemyMap = {}

        self.hardness_multiplier = 1

        self.health_bars = arcade.SpriteList()
        self.Buildings = arcade.SpriteList()
        self.People = arcade.SpriteList()

        self.uimanager = arcade.gui.UIManager()
        self.uimanager.enable()

        # Set up the player
        self.player_sprite = Player(self, ":resources:images/animated_characters/female_person/femalePerson_idle.png", 50, 50)
        self.player_sprite.center_x = 50
        self.player_sprite.center_y = 50
        self.player_list.append(self.player_sprite)

        self.spawn_enemy()
    def on_draw(self):
        """ Render the screen. """

        # Clear the screen
        arcade.start_render()
        self.camera.use()

        self.hospital.draw()
        self.Buildings.draw()

        # Call draw() on all your sprite lists below
        self.Enemies.draw()

        self.health_bars.draw()
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

        #print(delta_time)
        self.player_list.update()
        [enemy.update(self, delta_time) for enemy in self.Enemies]

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

    def check_sprite_with_enemies(self, obj):
        for enemy in self.Enemies:
            dist_to_object = arcade.get_distance_between_sprites(enemy, obj)
            if dist_to_object > 1500:
                continue
            if enemy.focused_on:
                dist_to_orig = arcade.get_distance_between_sprites(enemy, enemy.focused_on)
            else:
                dist_to_orig = 0
            if dist_to_object < dist_to_orig:
                enemy.focuse_on = obj
                self.calculate_enemy_path(enemy)
    def spawn_enemy(self):
        x, y = self.EnemySpawnPos()
        enemy_pick = random.choice(["Enemy Slinger"])
        #while not self.unlocked[enemy_pick]:
        #    enemy_pick = random.choice(["Basic Enemy", "Privateer", "Enemy Swordsman", "Enemy Archer", "Enemy Arsonist", "Enemy Wizard"])
        enemy_class = {"Enemy Slinger":Enemy_Slinger}[enemy_pick]
        enemy = enemy_class(self, x, y, difficulty=self.hardness_multiplier)
        enemy.focused_on = None
        


        max_i = 100
        if len(self.OpenToEnemies) == 0:
            max_i = 1
        i = 0
        while not self.graph[x/50][y/50] in enemy.movelist:
            pos = self.EnemySpawnPos()
            if pos is not None:
                x, y = pos
            i += 1
            if i >= max_i:
                enemy.destroy(self)
                enemy_pick = random.choice(["Enemy Slinger"])
                #while not self.unlocked[enemy_pick]:
                #    enemy_pick = random.choice(["Basic Enemy", "Privateer", "Enemy Swordsman", "Enemy Archer", "Enemy Arsonist", "Enemy Wizard"])
                enemy_class = {"Enemy Slinger":Enemy_Slinger}[enemy_pick]
                enemy = enemy_class(self, x, y, difficulty=self.hardness_multiplier)
                enemy.focused_on = None
                i = 0



        enemy.center_x = x
        enemy.center_y = y
        
        self.calculate_enemy_path(enemy)
        enemy.check = True
        self.Enemies.append(enemy)
        
        for person in self.People:
            person.check = True

    def calculate_enemy_path(self, enemy):
        enemy.check = False
        enemy.path = []
        #return 
        building, distance = arcade.get_closest_sprite(enemy, self.Buildings)
        person, distance2 = arcade.get_closest_sprite(enemy, self.People)
        player, distance3 = self.player_sprite, arcade.get_distance_between_sprites(enemy, self.player_sprite)

        
        bias1 = (distance+5)*enemy.building_bias
        bias2 = (distance2+5)*enemy.people_bias
        bias3 = (distance3+5)*enemy.player_bias

        if distance > 1500:
            bias1 = float("inf")
        if distance2 > 1500:
            bias2 = float("inf")
        if distance3 > 1500:
            bias3 = float("inf")
        

        if bias1 == float("inf") and bias2  == float("inf") and bias3 == float("inf"):
            return

        num = min(bias1, bias2, bias3)
        if num == bias1:
            obj2 = building
        elif num == bias2:
            obj2 = person
        elif num == bias3:
            obj2 = player


        path = AStarSearch(self.graph, enemy.position, obj2.position, allow_diagonal_movement=True, movelist=enemy.movelist, min_dist=enemy.range)
        if not path:
            pass
        elif arcade.get_distance_between_sprites(enemy, obj2) > enemy.range:        
            pass
        if num == bias1:
            enemy.focused_on = building
        elif num == bias2:
            enemy.focused_on = person
        elif num == bias3:
            enemy.focused_on = player
            
        if len(path) > 1:
            path.pop(0)
            enemy.path = path
            enemy.check = True
            enemy.idle = False
        elif len(path) == 1:
            enemy.path = path
            enemy.check = True
            enemy.idle = False
        else:
            enemy.check = False
    def calculate_path(self, obj, SpriteList, max_distance=1500):
        if len(SpriteList) == 0:
            return
        obj.check = False
        obj.path = []
        #return 
        
        obj2, distance = arcade.get_closest_sprite(obj, SpriteList)
        if obj2 == [] or distance > max_distance:
            return


        path = AStarSearch(self.graph, obj.position, obj2.position, allow_diagonal_movement=True, movelist=obj.movelist, min_dist=obj.range)
        if path or arcade.get_distance_between_sprites(obj, obj2) <= obj.range: 
            obj.focused_on = obj2
            
        if len(path) > 1:
            path.pop(0)
            obj.path = path
            obj.check = True
            obj.idle = False
        elif len(path) == 1:
            obj.path = path
            obj.check = True
            obj.idle = False
        else:
            obj.check = False
    

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
    def End(self):
        self.uimanager.disable()
        self.menu.uimanager.enable()
        window = arcade.get_window()
        window.show_view(self.menu)

    def generate_world(self):
        self.graph = LivingMap(5000, 5000, 25000)

def main():
    """ Main function """
    window = arcade.Window(width=1440, height=900, title="Havoc Hospital")
    game = MyGame(None, SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()