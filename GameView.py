import arcade

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
