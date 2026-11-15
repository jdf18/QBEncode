from engine import Entity, Camera
from engine.ui.responsive import Responsive2D

from typing import TYPE_CHECKING, Optional
import pygame

if TYPE_CHECKING:
    from pygame import Surface
    from typing import Callable

class UIText(Entity):
    rect: pygame.Rect

    text_surface: Surface

    def __init__(self, position: Responsive2D, size: Responsive2D, colour: pygame.Color, 
                 font=pygame.font.get_default_font(), text: str="") -> None:
        self.pos = position
        self.size = size
        self.callback = None
        self.colour = colour

        self.rect = pygame.Rect(0, 0, 0, 0)

        self.font = pygame.Font(font)
        self.text = text

        self.render()

    def update_rect(self, camera: Camera):
        self.rect = pygame.Rect(self.pos.value(camera), self.size.value(camera))

    def render(self):
        self.text_surface = self.font.render(self.text, True, self.colour)

    def draw(self, surface: Surface, camera: Camera) -> None:
        self.update_rect(camera)

        surface.blit(self.text_surface, self.rect)
        return 

    def update(self, dt: float) -> None:
        _ = dt
        return 

    def handle_event(self, event: pygame.Event) -> None:
        _ = event
        return 
