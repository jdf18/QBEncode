from engine import Entity, Camera
from engine.ui.responsive import Responsive2D

from typing import TYPE_CHECKING, Optional
import pygame

if TYPE_CHECKING:
    from pygame import Surface
    from typing import Callable

class UIQuad(Entity):
    rect: pygame.Rect

    def __init__(self, position: Responsive2D, size: Responsive2D, colour: pygame.Color) -> None:
        self.pos = position
        self.size = size
        self.colour = colour

        self.rect = pygame.Rect(0, 0, 0, 0)

    def update_rect(self, camera: Camera):
        self.rect = pygame.Rect(self.pos.value(camera), self.size.value(camera))

    def draw(self, surface: Surface, camera: Camera) -> None:
        self.update_rect(camera)

        pygame.draw.rect(surface, self.colour, self.rect)
        return 

    def update(self, dt: float) -> None:
        _ = dt
        return 

    def handle_event(self, event: pygame.Event) -> None:
        _ = event
        return 
