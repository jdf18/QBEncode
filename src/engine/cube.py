from typing import TYPE_CHECKING, Optional, cast

import pygame
from pygame import Vector2, Vector3
from enum import Enum

from engine import projection
from engine import Entity

import numpy as np
import quaternion

if TYPE_CHECKING:
    from typing import List
    from engine import Camera

from hkociemba_twophase.face import FaceCube
from hkociemba_twophase.enums import Color, Facelet

# https://www.schemecolor.com/rubik-cube-colors.php
class CubeColour(Enum):
    WHITE  = "0xffffff"
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
Quad2d = tuple[Vector2, Vector2, Vector2, Vector2]

class Cube(Entity):
    facelets: FaceCube

    facelet_quads: list[Quad2d]

    def __init__(self) -> None:
        super().__init__()

        self.facelets = FaceCube()
        self.rotation = np.quaternion(0.920177575008573, -0.13131837213796, -0.364919066736363, 0.0535050495060538)

        self.facelet_quads = list(
            (Vector2(), Vector2(), Vector2(), Vector2())
            for _ in range(len(Facelet))
        )

    def update_rotation(self, dx: int ,dy: int, sensitivity: float=0.005) -> None:
        angle_y = -dy * sensitivity
        angle_x =  dx * sensitivity

        q_y = quaternion.from_rotation_vector([angle_y, 0, 0])
        q_x = quaternion.from_rotation_vector([0, angle_x, 0])

        self.rotation = q_y * q_x * self.rotation

        print(self.rotation)

    @staticmethod
    def facelet_to_face_and_let(index: Facelet) -> tuple[Color, int]:
        return (Color(index // 9), index % 9)

    def get_face_points(self, index: Color) -> Quad:
        match index:
            case Color.U:
                points = (
                    Vector3(-1, -1, -1),
                    Vector3( 1, -1, -1),
                    Vector3( 1, -1,  1),
                    Vector3(-1, -1,  1),
                )
            case Color.R:
                points = (
                    Vector3( 1, -1,  1),
                    Vector3( 1, -1, -1),
                    Vector3( 1,  1, -1),
                    Vector3( 1,  1,  1),
                )
            case Color.F:
                points = (
                    Vector3(-1, -1,  1),
                    Vector3( 1, -1,  1),
                    Vector3( 1,  1,  1),
                    Vector3(-1,  1,  1),
                )
            case Color.D:
                points = (
                    Vector3(-1,  1,  1),
                    Vector3( 1,  1,  1),
                    Vector3( 1,  1, -1),
                    Vector3(-1,  1, -1),
                )
            case Color.L:
                points = (
                    Vector3(-1, -1, -1),
                    Vector3(-1, -1,  1),
                    Vector3(-1,  1,  1),
                    Vector3(-1,  1, -1),
                )
            case Color.B:
                points = (
                    Vector3( 1, -1, -1),
                    Vector3(-1, -1, -1),
                    Vector3(-1,  1, -1),
                    Vector3( 1,  1, -1),
                )
        points = tuple(map(Vector3, iter(quaternion.rotate_vectors(self.rotation, np.array(points)))))
        return cast(Quad, points)

    def get_facelet_points(self, index: Facelet) -> Quad:
        colour, let = Cube.facelet_to_face_and_let(index)

        face_points = self.get_face_points(colour)

        abs = face_points[0]
        x = (face_points[1] - abs) / 3
        y = (face_points[3] - abs) / 3


        facelet_x = let % 3
        facelet_y = let // 3

        facelet_zero = 0.1
        facelet_one = 0.9

        facelet_points = (
            abs + ((facelet_x+facelet_zero) * x) + ((facelet_y+facelet_zero) * y),
            abs + ((facelet_x+facelet_one)  * x) + ((facelet_y+facelet_zero) * y),
            abs + ((facelet_x+facelet_one)  * x) + ((facelet_y+facelet_one)  * y),
            abs + ((facelet_x+facelet_zero) * x) + ((facelet_y+facelet_one)  * y),
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
        points: Quad2d = cast(Quad2d, tuple(map(project, self.get_facelet_points(index))))

        self.facelet_quads[index] = points
        if not projection.is_culled((points[0], points[1], points[2])):
            pygame.draw.polygon(surface, pygame.Color(colour.value), points)
        return

    def update(self, dt: float) -> None:
        _ = dt
        return 

    def raycast(self, x: int, y: int) -> Optional[Facelet]:
        for i, quad in enumerate(self.facelet_quads):
            if projection.is_culled(cast(
                tuple[Vector2, Vector2, Vector2],
                tuple([quad[0], quad[1], quad[2]]))): continue

            if projection.point_in_quad(Vector2(x, y), quad):
                return Facelet(i)
        return None


    def handle_event(self, event: pygame.Event) -> None:
        match event.type:
            case pygame.MOUSEMOTION:
                if pygame.mouse.get_pressed()[pygame.BUTTON_RIGHT-1] == 1:
                    rel_x, rel_y = pygame.mouse.get_rel()
                    if rel_x**2 + rel_y**2 > 15**2:
                        return
                    self.update_rotation(rel_x, rel_y)
            case pygame.MOUSEBUTTONDOWN:
                if event.button == pygame.BUTTON_RIGHT:
                    pygame.mouse.get_rel()
                elif event.button == pygame.BUTTON_LEFT:
                    x, y = event.pos
                    facelet = self.raycast(x, y)
                    if facelet is None: return

                    self.cycle_facelet(facelet)
            case pygame.MOUSEBUTTONUP:
                if event.button == pygame.BUTTON_RIGHT:
                    pygame.mouse.get_rel()


    def cycle_facelet(self, index: Facelet) -> None:
        _, let = self.facelet_to_face_and_let(index)
        if let == 4: return

        c = self.facelets.f[index]
        c = (c + 1) % 6
        self.facelets.f[index] = c
        return
