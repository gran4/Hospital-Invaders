from Buildings import *
from Player import *
from BackGround import *


"""
Different types are coded in diff ways()
Put name in list
"""
ui_obj_info = {"Buildings":["Factory"],
"People":["Person"],
"Boats":["Cannoe"]}


#for Placing
unlocked = {None:False, "Factory":False}
objects = {"Factory": Factory}
requirements = {"Factory":{"metal":5}}
tiles = {"Factory": Land}
times = {"Factory":20}
max_people = {"Factory":2}


#for GUI
items_to_show = ["food", "wood", "stone", "metal", "science"]
item_weight = {"food":1, "wood":1, "stone":2, "metal":4}

#make each have alot so you can defualt to creative mode
prev_frame = {"food":1000, "wood":0, "stone":0, "metal":0}
descriptions = {
    "Bad Gifter":"Gives bad gifts      ",
    "Bad Reporter":"Gives bad reports      "
    }