import arcade, math, numba

from collections import ChainMap
from typing import Optional, Tuple, Union

from pyglet.event import EVENT_UNHANDLED

import arcade
from arcade.experimental.uistyle import UISliderStyle
from arcade.gui import UIWidget, Surface, UIEvent, UIMouseMovementEvent, UIMouseDragEvent, UIMousePressEvent, \
    UIMouseReleaseEvent
from arcade.gui._property import _Property, _bind
from arcade.gui.events import UIOnChangeEvent

from pathlib import Path
from typing import Optional, Union
import pyglet.media as media


class HealthBar:
    """
    Represents a bar which can display information about a sprite.

    :param MyGame Game: Game
    :param Tuple[float, float] position: The initial position of the bar.
    :param arcade.Color full_color: The color of the bar.
    :param arcade.Color background_color: The background color of the bar.
    :param int width: The width of the bar.
    :param int height: The height of the bar.
    :param int border_size: The size of the bar's border.
    """

    def __init__(
        self,
        game,
        position: Tuple[float, float] = (0, 0),
        full_color: arcade.Color = arcade.color.GREEN,
        background_color: arcade.Color = arcade.color.BLACK,
        width: int = 40,
        height: int = 4,
        border_size: int = 4,
    ) -> None:
        # Store the reference to the owner and the sprite list


        # Set the needed size variables
        self._box_width: int = width
        self._box_height: int = height
        self._half_box_width: int = self._box_width // 2
        self._center_x: float = 0.0
        self._center_y: float = 0.0
        self._fullness: float = 0.0

        # Create the boxes needed to represent the indicator bar
        self._background_box: arcade.SpriteSolidColor = arcade.SpriteSolidColor(
            self._box_width + border_size,
            self._box_height + border_size,
            background_color,
        )
        self._full_box: arcade.SpriteSolidColor = arcade.SpriteSolidColor(
            self._box_width,
            self._box_height,
            full_color,
        )
        game.health_bars.append(self._background_box)
        game.health_bars.append(self._full_box)

        # Set the fullness and position of the bar
        self.fullness: float = 1.0
        self.visible: bool = True
        self.position: Tuple[float, float] = position
    def remove_from_sprite_lists(self):
        self._background_box.remove_from_sprite_lists()
        self._full_box.remove_from_sprite_lists()

    @property
    def background_box(self) -> arcade.SpriteSolidColor:
        """Returns the background box of the indicator bar."""
        return self._background_box

    @property
    def full_box(self) -> arcade.SpriteSolidColor:
        """Returns the full box of the indicator bar."""
        return self._full_box

    @property
    def fullness(self) -> float:
        """Returns the fullness of the bar."""
        return self._fullness

    @fullness.setter
    def fullness(self, new_fullness: float) -> None:
        """Sets the fullness of the bar."""
        # Check if new_fullness if valid
        if 0.0 > new_fullness:
            new_fullness = 0
        elif 1.0 < new_fullness:
            new_fullness = 1

        # Set the size of the bar
        self._fullness = new_fullness

        self.full_box.width = self._box_width * new_fullness
        self.full_box.left = self._center_x - (self._box_width // 2)
    
    @property
    def visible(self) -> float:
        """Returns the visibility"""
        return self.visible
    @visible.setter
    def visible(self, visible) -> None:
        self._full_box.visible = visible
        self._background_box.visible = visible

    @property
    def position(self) -> Tuple[float, float]:
        """Returns the current position of the bar."""
        return self._center_x, self._center_y

    @position.setter
    def position(self, new_position: Tuple[float, float]) -> None:
        """Sets the new position of the bar."""
        # Check if the position has changed. If so, change the bar's position
        if new_position != self.position:
            new_position = new_position[0], new_position[1]-20
            self._center_x, self._center_y = new_position
            self.background_box.position = new_position
            self.full_box.position = new_position

            # Make sure full_box is to the left of the bar instead of the middle
            self.full_box.left = self._center_x - (self._box_width // 2)
