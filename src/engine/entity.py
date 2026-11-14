from typing import TYPE_CHECKING

from abc import ABC, abstractmethod

if TYPE_CHECKING:
    from pygame import Surface
    from engine import Camera


class Entity(ABC):
    @abstractmethod
    def draw(self, surface: Surface, camera: Camera) -> None:
        raise NotImplementedError

    @abstractmethod
    def update(self, dt: float) -> None:
        raise NotImplementedError
