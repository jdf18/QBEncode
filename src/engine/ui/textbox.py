
from engine import Entity, Camera
from engine.ui.responsive import Responsive2D
from engine.ui.button import UIButton
from engine.ui.text import UIText

from typing import TYPE_CHECKING, Optional
import pygame

if TYPE_CHECKING:
    from pygame import Surface
    from typing import Callable

class Toggle:
    value = False
    def toggle(self):
        self.value = not self.value

class UITextbox(Entity):
    clicked: Callable
    callback: Optional[Callable]

    def __init__(self, position: Responsive2D, size: Responsive2D, bg_colour: pygame.Color, text_colour: pygame.Color,
                 font=pygame.font.get_default_font(), text: str="") -> None:
        self.pos = position
        self.size = size
        self.callback = None
        self.bg_colour = bg_colour
        self.bg_colour_active = pygame.Color("0x555555")
        self.text_colour = text_colour

        self.button = UIButton(self.pos, self.size, self.bg_colour)

        def clicked() -> None:
            self.active.toggle()
        self.clicked = clicked
        self.button.callback = self.clicked

        self.text = UIText(self.pos + Responsive2D(pygame.Vector2(), pygame.Vector2(size.offset.y/2, size.offset.y/3)), 
                           self.size, self.text_colour, font, text)
        
        self.active = Toggle()

    def draw(self, surface: Surface, camera: Camera) -> None:
        self.button.draw(surface, camera)
        self.text.draw(surface, camera)
        return 

    def update(self, dt: float) -> None:
        self.button.update(dt)
        self.text.update(dt)

        if self.active.value:
            self.button.colour = self.bg_colour_active
        else:
            self.button.colour = self.bg_colour
        return 

    def handle_event(self, event: pygame.Event) -> None:
        self.button.handle_event(event)
        self.text.handle_event(event)

        match event.type:
            case pygame.KEYDOWN:
                if not self.active.value: return
                if event.key == pygame.K_BACKSPACE:
                    if len(self.text.text) <= 0: return
                    self.text.text = self.text.text[:-1]

                elif event.key == pygame.K_RETURN:
                    if self.callback is not None:
                        self.callback()
                else:
                    char = str(event.unicode)
                    if (char.isalpha() or (char in " -!")) and char.islower():
                        self.text.text = self.text.text + char
                    else: 
                        return
                
                self.text.render()
        return 
