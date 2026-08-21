import random
import sys

from core.logic import Environment, PhysicsBody, Vector2d

import pygame

pygame.init()
WIDTH, HEIGHT = 900, 600

space_color = (20, 20, 30)

screen = pygame.display.set_mode((WIDTH, HEIGHT))

fade_surface = pygame.Surface((WIDTH, HEIGHT))
fade_surface.set_alpha(100)
fade_surface.fill(space_color)

FPS = 60
clock = pygame.time.Clock()

space = Environment(HEIGHT, WIDTH)


def mg(body: PhysicsBody):
  return Vector2d(0, body.mass * -15)


def air_resistance(body: PhysicsBody):
  return -0.5 * body.velocity


space.forces.extend([mg, air_resistance])
space.boundary_collisions = True

body_count = random.randint(2, 20)
bodies: list[PhysicsBody] = []

for index in range(body_count):
  body = PhysicsBody(
    f"name-{index + 1}",
    random.randint(80, WIDTH - 80),
    random.randint(80, HEIGHT - 80),
    500,
    0.0,
    (
      random.randint(80, 255),
      random.randint(80, 255),
      random.randint(80, 255),
    ),
  )
  body.velocity = Vector2d(random.uniform(-80, 80), random.uniform(-80, 80))
  body.radius = random.randint(8, 15)
  body.elastic_coefficient = random.uniform(0.05, 0.08)
  bodies.append(body)

space.register(*bodies)

while True:
  # Handle closing the window
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      pygame.quit()
      sys.exit()

  screen.fill(space_color)
  # screen.blit(fade_surface, (0, 0))

  for body in space.bodies:
    screen_x = body.position.x
    # Convert bottom-left origin to top-left origin
    screen_y = HEIGHT - body.position.y

    pygame.draw.circle(screen, body.color, (screen_x, screen_y), body.radius)

    # region vector line for velocity
    # -body.velocity.y because the Y-axis is flipped on screen
    vector_scale = 0.5
    end_x = screen_x + (body.velocity.x * vector_scale)
    end_y = screen_y - (body.velocity.y * vector_scale)

    pygame.draw.line(
      screen,
      (0, 255, 0),
      (screen_x, screen_y),
      (int(end_x), screen_y),
      1,
    )
    pygame.draw.line(
      screen,
      (0, 255, 0),
      (screen_x, screen_y),
      (screen_x, int(end_y)),
      1,
    )
    pygame.draw.line(
      screen,
      (255, 0, 0),
      (screen_x, screen_y),
      (int(end_x), int(end_y)),
      1,
    )
    # endregion vector line

  time_period = 4 / FPS
  space.calculate(time_period)
  pygame.display.flip()
  clock.tick(FPS)
