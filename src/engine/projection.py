from pygame.math import Vector2, Vector3

class Camera:
    position: Vector3
    screen_dist: float

    def __init__(self) -> None:
        self.position = Vector3(0, 0, 0)
        self.screen_dist = 1

def world_to_screen_space(camera: Camera, coord: Vector3) -> Vector2:
    rel_position = coord - camera.position

    return camera.screen_dist * rel_position.xy
