import pygame
import sys
from core.logic import Environment, Vector2d, PhysicsBody

pygame.init()
HEIGHT, WIDTH = 600, 900

space_color = (20, 20, 30)

screen = pygame.display.set_mode((WIDTH, HEIGHT))

fade_surface = pygame.Surface((WIDTH, HEIGHT))
fade_surface.set_alpha(100)
fade_surface.fill(space_color)

FPS = 60
clock = pygame.time.Clock()

space = Environment(height=HEIGHT, width=WIDTH)
space.acceleration = Vector2d(0, -10)
space.boundary_collisions = True

body1 = PhysicsBody("name-1", mass=50000, charge=0.0, x=550, y=300)
body1.velocity = Vector2d(0, 20)
body1.radius = 10

body2 = PhysicsBody("name-2", mass=50000, charge=0.0, x=600, y=300)
body2.velocity = Vector2d(0, -20)
body2.radius = 10

body3 = PhysicsBody("name-3", mass=1000, charge=0.0, x=500, y=300)
body3.radius = 10
body3.velocity = Vector2d(-0.9324, -0.8648)

space.register(body1, body2)

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

    # region vector line
    # -body.velocity.y because the Y-axis is flipped on screen
    vector_scale = 0.5
    end_x = screen_x + (body.velocity.x * vector_scale)
    end_y = screen_y - (body.velocity.y * vector_scale)

    pygame.draw.line(
      screen,
      color=(0, 255, 0),
      start_pos=(screen_x, screen_y),
      end_pos=(int(end_x), screen_y),
      width=1,
    )
    pygame.draw.line(
      screen,
      color=(0, 255, 0),
      start_pos=(screen_x, screen_y),
      end_pos=(screen_x, int(end_y)),
      width=1,
    )
    pygame.draw.line(
      screen,
      color=(255, 0, 0),
      start_pos=(screen_x, screen_y),
      end_pos=(int(end_x), int(end_y)),
      width=1,
    )
    # endregion vector line

  time_period = 5 / FPS
  space.calculate(time_period)
  pygame.display.flip()
  clock.tick(FPS)
