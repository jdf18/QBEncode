from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from engine import Camera

from pygame import Vector2


class Responsive2D:
    def __init__(self, mult: Vector2, offset: Vector2) -> None:
        self.mult = mult
        self.offset = offset

    def value(self, camera: Camera) -> Vector2:
        return Vector2(camera.screen_dims[0] * self.mult[0],
                       camera.screen_dims[1] * self.mult[1],) + self.offset
