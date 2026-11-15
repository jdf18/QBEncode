from typing import TYPE_CHECKING

import pygame

from engine.projection import Camera

if TYPE_CHECKING:
    from typing import List
    from pygame  import Surface, Clock
    from engine import Entity

class Engine:
    screen: Surface
    clock: Clock
    running: bool
    dt: float
    screen_dims: pygame.Vector2

    camera: Camera
    entities: List[Entity]

    font: pygame.Font

    def __init__(self) -> None:
        pass

    def start(self, screen_dims) -> None:
        # pygame setup
        pygame.init()
        pygame.font.init()
        self.screen = pygame.display.set_mode(screen_dims)
        self.clock = pygame.time.Clock()
        self.running = True
        self.screen_dims = pygame.Vector2(screen_dims)

        self.dt = 1e-10

        self.camera = Camera()
        self.camera.screen_offset = self.screen_dims / 2
        self.camera.screen_dims = self.screen_dims
        self.entities = []

    def shutdown(self) -> None:
        pygame.font.quit()
        pygame.quit()

    def run(self) -> None:
        self.running = True

        while self.running:
            self.poll_events()

            for entity in self.entities:
                entity.update(self.dt)

            # fill the screen with a color to wipe away anything from last frame
            self.screen.fill("0x222222")

            for entity in self.entities:
                entity.draw(self.screen, self.camera)

            # flip() the display to put your work on screen
            pygame.display.flip()

            # limits FPS to 60
            # dt is delta time in seconds since last frame, used for framerate-
            # independent physics.
            self.dt = self.clock.tick(60) / 1000

        self.shutdown()


    def poll_events(self):
        # poll for events
        # pygame.QUIT event means the user clicked X to close your window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            for entity in self.entities:
                entity.handle_event(event)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            pass
        if keys[pygame.K_s]:
            pass
        if keys[pygame.K_a]:
            pass
        if keys[pygame.K_d]:
            pass



