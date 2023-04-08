import arcade


class StartMenu(arcade.View):
    """
    First Menu that loads in. Customize things outside of the world.
    """
    def __init__(self):
      super().__init__()
    def generate_world(self):
      pass
class MyGame(arcade.View):
    """
    The Game itself
    """
    def __init__(self, menu):

        # Call the parent class and set up the window
        super().__init__()#750, 500, "SCREEN_TITLE")

        arcade.set_background_color(arcade.csscolor.CORNFLOWER_BLUE)

        self.time_alive = 0        
        self.setup()

        window = arcade.get_window()
        self.on_resize(window.width, window.height)

    def setup(self):
      pass
    def on_update(self, delta_time):
      pass

def main():
    """Main method"""
    window = arcade.Window(1440, 900, "SantaFest Destiny", resizable=True)
    startmenu = StartMenu()#MyGame()#StartMenu()
    window.show_view(startmenu)
    arcade.run()
def foo():
    print("NJJNJNDEEDDE")

if __name__ == "__main__":
    atexit.register(foo)
    main()

