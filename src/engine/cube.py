from typing import TYPE_CHECKING

import pygame
from enum import Enum, auto

from engine import projection

if TYPE_CHECKING:
    from engine import Entity, Camera

# https://www.schemecolor.com/rubik-cube-colors.php
class CubeColour(Enum):
    WHITE = "0xff0000"
    RED = "0xB90000"
    GREEN = "0x009B48"
    YELLOW = "0xFFD500"
    ORANGE = "0xFF5900"
    BLUE = "0x0045AD"


def face_to_colour(face) -> CubeColour:
    match (face):
        case U:
            return CubeColour.WHITE


class Cube(Entity):
    def __init__(self) -> None:
        super().__init__()

        self.facelets = None

    def draw(self, surface: pygame.Surface, camera: Camera) -> None:
        for dir in range(6):
            self.draw_face(dir, surface, camera)
        return

    def draw_face(self, direction, surface: pygame.Surface, camera: Camera) -> None:
        for i in range(9):
            self.draw_facelet(direction + i, surface, camera)

    def draw_facelet(self, index, surface: pygame.Surface, camera: Camera) -> None:
        colour = face_to_colour()
        
        project = lambda x : projection.world_to_screen_space(camera, x)
        points = map(project, (pygame.Vector3()))
        pygame.draw.polygon(surface, colour.value(), tuple(points))
        return

        


