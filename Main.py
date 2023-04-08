import arcade
from StartMenu import *
from GameView import *

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

