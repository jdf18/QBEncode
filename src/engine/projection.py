from pygame.math import Vector2, Vector3

class Camera:
    position: Vector3
    screen_dist: float
    screen_offset: Vector2
    screen_dims: Vector2

    def __init__(self) -> None:
        self.position = Vector3(0, 0, 0)
        self.screen_dist = 1

def is_culled(points: tuple[Vector2, Vector2, Vector2]) -> bool:
    E1 = points[1] - points[0]
    E2 = points[2] - points[0]

    return E1.cross(E2) <= 0

def world_to_screen_space(camera: Camera, coord: Vector3) -> Vector2:
    rel_position = coord - camera.position

    return camera.screen_offset + (camera.screen_dist * rel_position.xy)

def point_in_quad(point, quad):
    px, py = point
    signs = []

    for i in range(4):
        x1, y1 = quad[i]
        x2, y2 = quad[(i + 1) % 4]

        # 2D cross product
        cross = (x2 - x1) * (py - y1) - (y2 - y1) * (px - x1)
        if cross != 0:
            signs.append(cross > 0)

    # True if all non-zero cross products have the same sign
    return len(set(signs)) <= 1
