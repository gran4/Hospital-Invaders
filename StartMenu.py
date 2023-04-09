import arcade
from Components import *
from GameView import *
class StartMenu(arcade.View):
    """
    First Menu that loads in. Customize things outside of the world.
    """
    def __init__(self):
        super().__init__()
        self.uimanager = arcade.gui.UIManager()
        self.uimanager.enable()

        textures = arcade.load_spritesheet("resources/gui/Wooden Font.png", 14, 24, 12, 70, margin=1)
        self.Alphabet_Textures = {" ":None}
        string = "ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890abcdefghijklmnopqrstuvwxyz.:,%/-+_"
        for i in range(len(string)):
            self.Alphabet_Textures[string[i]] = textures[i]

            #self.texts.append(CustomTextSprite("SantaFest Destiny", self.Alphabet_Textures, scale=5, width=1000, center_x=250, center_y=600, text_margin=60))

      
        start_button = CustomUIFlatButton(self.Alphabet_Textures, click_sound = None, text="World1", width=140, height=50, x=0, y=50, text_offset_x = 10, text_offset_y=35, offset_x=75, offset_y=25)
        start_button.on_click = self.Start
        start_button.world_num = 1
        wrapper = arcade.gui.UIAnchorWidget(anchor_x="center_x",anchor_y="center_y",child=start_button, align_x=0, align_y=100)
        start_button.wrapper = wrapper
        self.uimanager.add(wrapper)
    
    def Start(self, event):
        game = MyGame(self, SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        window = arcade.get_window()
        self.uimanager.disable()
        self.window.show_view(game)
    def on_draw(self):
        arcade.start_render()
        self.uimanager.draw()


def main():
    """ Main function """
    window = arcade.Window(1440, 900, "Havoc Hospital", resizable=True)
    game = StartMenu()
    window.show_view(game)
    arcade.run()
if __name__ == "__main__":
    main()