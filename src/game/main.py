import pygame
from Box2D import b2PolygonShape, b2World
from pygame.locals import K_ESCAPE, KEYDOWN, QUIT

PPM = 20.0  # Pixels per meter
TARGET_FPS = 60
TIME_STEP = 1.0 / TARGET_FPS
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480

# PyGame Setup
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
pygame.display.set_caption("We need to build a wall!")
clock = pygame.time.Clock()

# PyBox World
world = b2World(gravity=(0, -10), doSleep=True)

ground_body = world.CreateStaticBody(
    position=(0, 1), shapes=b2PolygonShape(box=(50, 5))
)

dynamic_body = world.CreateDynamicBody(position=(10, 15), angle=15)
dynamic_body_2 = world.CreateDynamicBody(position=(10, 20), angle=15)

box = dynamic_body.CreatePolygonFixture(box=(2, 1), density=1, friction=0.3)
box_2 = dynamic_body_2.CreatePolygonFixture(box=(2, 1), density=1, friction=0.3)

colors = {
    0: (255, 255, 255, 255),
    2: (127, 127, 127, 255),
}

# Game Loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            running = False

    screen.fill((0, 0, 0, 0))

    for body in (ground_body, dynamic_body, dynamic_body_2):
        for fixture in body.fixtures:
            shape = fixture.shape
            vertices = [(body.transform * v) * PPM for v in shape.vertices]

            # Flipping the sign for the y component (pygame does it upside down)
            vertices = [(v[0], SCREEN_HEIGHT - v[1]) for v in vertices]

            pygame.draw.polygon(screen, (255, 255, 255, 255), vertices)

    world.Step(TIME_STEP, 10, 10)

    pygame.display.flip()
    clock.tick(TARGET_FPS)

pygame.quit()
print("Done!")
