import pygame
import sys
from core.logic import i2d, Body, simState, mainloop

pygame.init()
HEIGHT, WIDTH = 700, 1300

space_color = (20, 20, 30)

screen = pygame.display.set_mode((WIDTH, HEIGHT))

fade_surface = pygame.Surface((WIDTH, HEIGHT))
fade_surface.set_alpha(100)  # Lower = longer trails (0-255)
fade_surface.fill(space_color)

FPS = 60
clock = pygame.time.Clock()

simState.flowSwitch = True
body1 = Body("name-1", 550, 0.0006, 350, 60)
body1.velocity = i2d(0, 10)
body1.register()

body2 = Body("name-2", 750, 0.0006, 710, 260)
body2.velocity = i2d(0, 0)
body2.register()

body3 = Body("name-3", 750, 0.0006, 510, 560)
body3.velocity = i2d(0, -10)
body3.register()

ex_btn = pygame.Rect(100, 200, 40, 50)

while True:
  # Handle closing the window
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      pygame.quit()
      sys.exit()

  # screen.fill(space_color);
  screen.blit(fade_surface, (0, 0))

  for body in simState.bodies:
    screen_x = body.position.x
    screen_y = HEIGHT - body.position.y

    pygame.draw.circle(screen, body.color, (screen_x, screen_y), 5)

    # We scale the velocity (e.g., * 0.5) so the line isn't too long
    # We use -body.velocity.y because the Y-axis is flipped on screen
    vector_scale = 5
    end_x = screen_x + (body.velocity.x * vector_scale)
    end_y = screen_y - (body.velocity.y * vector_scale)

    pygame.draw.line(
      screen, (0, 255, 0), (screen_x, screen_y), (int(end_x), screen_y), 1
    )
    pygame.draw.line(
      screen, (0, 255, 0), (screen_x, screen_y), (screen_x, int(end_y)), 1
    )

  mainloop(0.1)
  pygame.display.flip()
  clock.tick(FPS)
