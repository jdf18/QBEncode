
from pygame import Vector2, Vector3

from engine import Engine
from engine.cube import Cube

engine = Engine()
DIMS = (1280, 720)
engine.start(DIMS)

engine.camera.position = Vector3(0, 0, 10)
engine.camera.screen_dist = 100
engine.camera.screen_offset = Vector2(DIMS) / 2

engine.entities.append(Cube())
engine.run()
