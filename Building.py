import arcade, random
from Components import *


class BaseBuilding(arcade.Sprite):
    def __init__(self, game, x: float, y: float, health: float, dmg: float, range: int, max_len: int, texture: str,
                 scale=1):
        super().__init__(texture, center_x=x, center_y=y, scale=scale)

        self.texture = arcade.load_texture(texture)
        self.center_x = x
        self.center_y = y
        self.hit_box = self.texture.hit_box_points
        self.path = False

        self.dmg = dmg
        self.health = health
        self.max_health = self.health
        self.health_bar = HealthBar(game, position=self.position)
        self.health_bar.fullness = self.health / self.max_health
        self.range = range

        self.list_of_people = []
        self.max_length = max_len

        self.check_timer = 0
        self.enemy = None
        self.fire = None
        self.fire_resistence = .9
        self.vars = {}

    def add(self, sprite):
        if len(self.list_of_people) == self.max_length:
            return True
        self.list_of_people.append(sprite)
        sprite.health_bar.visible = False
        sprite.remove_from_sprite_lists()
        return False

    def remove(self):
        if len(self.list_of_people) == 0:
            return
        sprite = self.list_of_people[0]
        sprite.health_bar.visible = True
        self.list_of_people.pop(0)
        return sprite

    def destroy(self, game, menu_destroy=False):
        if menu_destroy:
            while len(self.list_of_people) > 0:
                person = self.remove()
                game.People.append(person)
        else:
            game.population -= len(self.list_of_people)
            for person in self.list_of_people:
                person.health_bar.remove_from_sprite_lists
                person.remove_from_sprite_lists()
        if self is game.last:
            game.clear_uimanager()
            game.last = Bad_Cannoe(game, 10000000, 1000000)
            game.selection_rectangle.position = (-1000000, -1000000)
        game.BuildingChangeEnemySpawner(self.center_x, self.center_y, placing=-1, min_dist=150, max_dist=200)
        self.remove_from_sprite_lists()
        self.health_bar.remove_from_sprite_lists()

        if self.fire: self.fire.destroy(game)

        self.health = -100

    def on_destroy(self, source):
        self.destroy(source.game, source.menu_destroy)

    def clicked(self, game):
        game.clear_uimanager()
        if game.last == self:
            game.last = None
            return
        game.last = self

        button = CustomUIFlatButton(game.Alphabet_Textures, text="Leave", width=140, height=50, x=0, y=50,
                                    text_offset_x=16, text_offset_y=35, offset_x=75, offset_y=25)
        button.on_click = game.leave
        button.obj = self
        wrapper = arcade.gui.UIAnchorWidget(anchor_x="center_x", anchor_y="center_y",
                                            child=button, align_x=-300, align_y=-200)
        game.uimanager.add(wrapper)
        game.extra_buttons.append(wrapper)

        button = CustomUIFlatButton(game.Alphabet_Textures, text="Print  Attrs", width=140, height=50, x=0, y=50,
                                    text_offset_x=16, text_offset_y=35, offset_x=75, offset_y=25)
        button.on_click = game.print_attr
        button.obj = self
        wrapper = arcade.gui.UIAnchorWidget(anchor_x="center_x", anchor_y="center_y",
                                            child=button, align_x=-100, align_y=-200)
        game.uimanager.add(wrapper)
        game.extra_buttons.append(wrapper)

        button = CustomUIFlatButton(game.Alphabet_Textures, text="Destroy", width=140, height=50, x=0, y=50,
                                    text_offset_x=10, text_offset_y=35, offset_x=65, offset_y=25)
        button.on_click = game.destroy
        button.obj = self
        wrapper = arcade.gui.UIAnchorWidget(anchor_x="center_x", anchor_y="center_y",
                                            child=button, align_x=100, align_y=-200)
        game.uimanager.add(wrapper)
        game.extra_buttons.append(wrapper)

        self.clicked_override(game)

    def clicked_override(self, game):
        pass

    def update(self, delta_time, game):
        for resource, amount in self.vars.items():
            vars(game)[resource] += amount * delta_time * vars(game)[resource + "_multiplier"] / self.max_length * len(
                self.list_of_people) * game.overall_multiplier
        self.on_update(delta_time, game)

    def on_update(self, delta_time, game):
        if self.health <= 0:
            self.destroy(game)
        self.health_bar.fullness = self.health / self.max_health

        if self.enemy:
            if arcade.get_distance_between_sprites(self, self.enemy) < self.range:
                self.on_attack(delta_time, game)
        else:
            self.check_timer += delta_time
            if self.check_timer < 1:
                return
            self.check_timer -= 1
            enemy, distance = arcade.get_closest_sprite(self, game.Enemies)
            self.enemy = enemy

    def on_attack(self, delta_time, game):
        self.enemy.health -= self.dmg
        if self.enemy.health < 0:
            game.Enemies.remove(self.enemy)
            self.enemy = None

    def save(self, game):
        if self.enemy:
            self.enemy = game.Enemies.index(self.enemy)
        self.health_bar.remove_from_sprite_lists()

    def load(self, game):
        if self.enemy:
            self.enemy = game.Enemies[self.enemy]
        game.health_bars.append(self.health_bar._background_box)
        game.health_bars.append(self.health_bar._full_box)


class SnowTower(BaseBuilding):
    def __init__(self, game, x: float, y: float):
        super().__init__(game, x, y, 20, .5, 250, 1, "resources/Sprites/SnowTower.png")
        self.vars = {}
        self.Updates = False
        self.canAttack = True

        self.snowballs = arcade.SpriteList()
        self.focused_on = None

    def update(self, game, delta_time):
        if self.health <= 0:
            self.destroy(game)
            return
        self.on_update(game, delta_time)

        for snowball in self.snowballs:
            snowball.forward(speed=delta_time * 50)
            snowball.update()
            snowball.time += delta_time
            if snowball.time > 15:
                snowball.remove_from_sprite_lists()
            elif not self.focused_on:
                break
            elif arcade.get_distance(snowball.center_x, snowball.center_y, self.focused_on.center_x,
                                     self.focused_on.center_y) < 25:
                self.focused_on.health -= self.damage * random.random() * random.random() * 4
                snowball.remove_from_sprite_lists()

        self.timer += delta_time
        if self.timer < self.WaitToAttack:
            return
        self.timer -= self.bow.WaitToAttack
        self.canAttack = True

    def on_attack(self, game, delta_time):
        if not self.canAttack:
            return
        angle = rotation(self.center_x, self.center_y, self.focused_on.center_x, self.focused_on.center_y,
                         max_turn=360) + random.randrange(-5, 5)
        snowball = arcade.Sprite("resources/Sprites/Snowball.png", scale=1, center_x=self.center_x,
                                 center_y=self.center_y, angle=angle)
        snowball.time = 0
        self.snowballs.append(snowball)
        game.overParticles.append(snowball)
        snowball.forward()
        snowball.update()
