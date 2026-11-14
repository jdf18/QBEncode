from os import stat
from typing import TYPE_CHECKING, Union

import pygame
from pygame import Vector3
from enum import Enum, auto

from engine import projection
from engine import Entity

if TYPE_CHECKING:
    from typing import List
    from engine import Camera

from hkociemba_twophase.face import FaceCube
from hkociemba_twophase.enums import Color, Corner, Facelet

# https://www.schemecolor.com/rubik-cube-colors.php
class CubeColour(Enum):
    WHITE  = "0xff0000"
    RED    = "0xB90000"
    GREEN  = "0x009B48"
    YELLOW = "0xFFD500"
    ORANGE = "0xFF5900"
    BLUE   = "0x0045AD"


def face_to_colour(face) -> CubeColour:
    match (face):
        case Color.U:
            return CubeColour.WHITE
        case Color.R:
            return CubeColour.RED
        case Color.F:
            return CubeColour.GREEN
        case Color.D:
            return CubeColour.YELLOW
        case Color.L:
            return CubeColour.ORANGE
        case Color.B:
            return CubeColour.BLUE

    raise KeyError()


Quad = tuple[Vector3, Vector3, Vector3, Vector3]

class Cube(Entity):
    facelets: FaceCube

    def __init__(self) -> None:
        super().__init__()

        self.facelets = FaceCube()
        self.rotation

    @staticmethod
    def facelet_to_face_and_let(index: Facelet) -> tuple[Color, int]:
        return (Color(index // 9), index % 9)

    @staticmethod
    def get_face_points(index: Color) -> Quad:
        match index:
            case Color.U:
                return (
                    Vector3(-1,  1, -1),
                    Vector3( 1,  1, -1),
                    Vector3( 1,  1,  1),
                    Vector3(-1,  1,  1),
                )
            case Color.R:
                return (
                    Vector3( 1,  1,  1),
                    Vector3( 1,  1, -1),
                    Vector3( 1, -1, -1),
                    Vector3( 1, -1,  1),
                )
            case Color.F:
                return (
                    Vector3(-1,  1,  1),
                    Vector3( 1,  1,  1),
                    Vector3( 1, -1,  1),
                    Vector3(-1, -1,  1),
                )
            case Color.D:
                return (
                    Vector3(-1, -1,  1),
                    Vector3( 1, -1,  1),
                    Vector3( 1, -1, -1),
                    Vector3(-1, -1, -1),
                )
            case Color.L:
                return (
                    Vector3(-1,  1, -1),
                    Vector3(-1,  1,  1),
                    Vector3(-1, -1,  1),
                    Vector3(-1, -1, -1),
                )
            case Color.B:
                return (
                    Vector3( 1,  1, -1),
                    Vector3(-1,  1, -1),
                    Vector3(-1, -1, -1),
                    Vector3( 1, -1, -1),
                )

    @staticmethod
    def get_facelet_points(index: Facelet) -> Quad:
        colour, let = Cube.facelet_to_face_and_let(index)

        face_points = Cube.get_face_points(colour)

        abs = face_points[0]
        x = (face_points[1] - abs) / 3
        y = (face_points[3] - abs) / 3


        facelet_x = let % 3
        facelet_y = let // 3

        facelet_points = (
            abs + (facelet_x * x) + ((facelet_y) * y),
            abs + ((facelet_x+1) * x) + ((facelet_y) * y),
            abs + ((facelet_x+1) * x) + ((facelet_y+1) * y),
            abs + ((facelet_x) * x) + ((facelet_y+1) * y),
        )
        return facelet_points 

    def draw(self, surface: pygame.Surface, camera: Camera) -> None:
        for index in Facelet:
            self.draw_facelet(index, surface, camera)
        return

    # def draw_face(self, direction, surface: pygame.Surface, camera: Camera) -> None:
    #     for i in range(9):
    #         self.draw_facelet(direction + i, surface, camera)

    def draw_facelet(self, index: Facelet, surface: pygame.Surface, camera: Camera) -> None:
        facelets: List[Color] = self.facelets.f

        colour = face_to_colour(facelets[index])

        project = lambda x : projection.world_to_screen_space(camera, x)
        points = tuple(map(project, Cube.get_facelet_points(index)))

        if not projection.is_culled((points[0], points[1], points[2])):
            pygame.draw.polygon(surface, pygame.Color(colour.value), points)
        return

    def update(self, dt: float) -> None:
        _ = dt
        return 
        


