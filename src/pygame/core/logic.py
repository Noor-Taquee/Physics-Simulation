"""
The logic for simulations
"""

from collections import defaultdict
from dataclasses import dataclass
from typing import Callable, Any, Literal
from math import sqrt

from core.eventSystem import EventTarget
from core.vector2d import Vector2d

EventMap = defaultdict[str, list[Callable[..., Any]]]


@dataclass
class i2d:
  """A 2-dimensional identity"""

  x: float = 0
  y: float = 0


K = 9 * (10**9)
"""**Electrostatic constant**"""

G = 1
"""**Gravitational constant**"""

RGBColor255 = tuple[int, int, int]

BodyEventType = Literal["update", "reset"]
BodyEventMap = dict[BodyEventType, list[Callable[..., Any]]]


# MARK: PhysicsBody
class PhysicsBody(EventTarget):
  """
  Simulation Body
  Using bottom left corner as *origin*.
  """

  name: str

  mass: float
  """Mass of the body in *kilograms*"""

  charge: float
  """Charge of the body in *quloumb*"""

  radius: float

  elastic_coefficient: float

  kinetic_friction_coefficient: float
  static_friction_coefficient: float

  defaultPosition: Vector2d
  position: Vector2d

  velocity: Vector2d
  """Velocity of the body in *m/s*"""

  acceleration: Vector2d

  force: Vector2d

  def __init__(
    self,
    name: str,
    x: float,
    y: float,
    mass: float,
    charge: float = 0,
    color: RGBColor255 = (255, 255, 255),
  ) -> None:
    EventTarget().__init__()
    self.name = name
    self.mass = mass
    self.charge = charge
    self.defaultPosition = Vector2d(x, y)
    self.color = color
    self.shape = "circle"
    self.radius = 15
    self.elastic_coefficient = 0.95

    self.position = Vector2d(self.defaultPosition.x, self.defaultPosition.y)
    self.velocity = Vector2d(0, 0)
    self.acceleration = Vector2d(0, 0)
    self.force = Vector2d(0, 0)
    self.eventMap = {"update": [], "reset": []}

  def reset(self):
    self.position = Vector2d(self.defaultPosition.x, self.defaultPosition.y)
    self.velocity = Vector2d(0, 0)
    self.acceleration = Vector2d(0, 0)
    self.force = Vector2d(0, 0)

    self.dispatch_event("reset", {"target": self})

  def momentum(self) -> float:
    return self.velocity.magnitude() * self.mass

  def resolve_forces(self, time: float | int) -> None:
    if self.mass == 0:
      return

    # acceleration
    self.acceleration = self.force / self.mass

    # velocity
    self.velocity += self.acceleration * time

    # position
    self.position += self.velocity * time

    self.dispatch_event("update", {"target": self})


# MARK: Environment
class Environment:
  forces: list[Callable[[PhysicsBody], Vector2d]]
  """Environment forces"""

  bodies: list[PhysicsBody]
  """list of bodies for the calculation"""

  min_dis_for_calc: float
  """Minimum distance to stop calculating the force."""

  height: float | None
  width: float | None

  boundary_collisions: bool
  """Switch to enable/disable boundary collisions"""

  top: float | None
  left: float | None
  bottom: float | None
  right: float | None

  def __init__(self, height: float | None = None, width: float | None = None):
    self.forces = []
    self.bodies = []
    self.min_dis_for_calc = 2
    self.boundary_collisions = False
    self.height = height
    self.width = width
    self.top = self.height
    self.right = self.width
    self.bottom = 0
    self.left = 0

  def register(self, *bodies: PhysicsBody):
    """Adds the body in the calculation loop"""
    for body in bodies:
      if body not in self.bodies:
        self.bodies.append(body)

  def check_boundary_collisions(self, body: PhysicsBody):
    if not self.boundary_collisions:
      return

    if self.right is not None:
      if body.position.x + body.radius >= self.right:
        body.position.x = self.right - body.radius
        body.velocity.x = -abs(body.velocity.x) * body.elastic_coefficient

    if self.left is not None:
      if body.position.x - body.radius <= self.left:
        body.position.x = self.left + body.radius
        body.velocity.x = abs(body.velocity.x) * body.elastic_coefficient

    if self.top is not None:
      if body.position.y + body.radius >= self.top:
        body.position.y = self.top - body.radius
        body.velocity.y = -abs(body.velocity.y) * body.elastic_coefficient

    if self.bottom is not None:
      if body.position.y - body.radius <= self.bottom:
        body.position.y = self.bottom + body.radius
        body.velocity.y = abs(body.velocity.y) * body.elastic_coefficient

  def calculate(self, time: float):
    """Calculates forces between bodies."""
    number_of_bodies = len(self.bodies)

    for i in range(number_of_bodies):
      body = self.bodies[i]

      # Inject environment properties
      for force in self.forces:
        body.force += force(body)

      for j in range(i + 1, number_of_bodies):
        if i == j:
          continue

        body_2 = self.bodies[j]

        # distance
        dx = body_2.position.x - body.position.x
        dy = body_2.position.y - body.position.y
        dis = sqrt(dx * dx + dy * dy)

        if dis == 0 or dis <= self.min_dis_for_calc:
          continue

        # angles
        sin = dy / dis
        cos = dx / dis

        # gravitational force
        force = G * body_2.mass * body.mass / (dis * dis)
        body.force.x += force * cos
        body.force.y += force * sin
        body_2.force.x += -force * cos
        body_2.force.y += -force * sin

        # electrostatic force
        force = -K * body_2.charge * body.charge / (dis * dis)
        body.force.x += force * cos
        body.force.y += force * sin
        body_2.force.x += -force * cos
        body_2.force.y += -force * sin

        # body body collisions

        if dis <= body.radius + body_2.radius:
          overlap = (body.radius + body_2.radius) - dis

          body.position.x -= (overlap / 2) * cos
          body.position.y -= (overlap / 2) * sin
          body_2.position.x += (overlap / 2) * cos
          body_2.position.y += (overlap / 2) * sin

          v1n = body.velocity.x * cos + body.velocity.y * sin
          v1t = -body.velocity.x * sin + body.velocity.y * cos

          v2n = body_2.velocity.x * cos + body_2.velocity.y * sin
          v2t = -body_2.velocity.x * sin + body_2.velocity.y * cos

          m1, m2 = body.mass, body_2.mass

          v1n_new = (v1n * (m1 - m2) + 2 * m2 * v2n) / (m1 + m2)
          v2n_new = (v2n * (m2 - m1) + 2 * m1 * v1n) / (m1 + m2)

          elasticity = min(body.elastic_coefficient, body_2.elastic_coefficient)
          v1n_new *= elasticity
          v2n_new *= elasticity

          body.velocity.x = v1n_new * cos - v1t * sin
          body.velocity.y = v1n_new * sin + v1t * cos

          body_2.velocity.x = v2n_new * cos - v2t * sin
          body_2.velocity.y = v2n_new * sin + v2t * cos

      # boundary collisions
      self.check_boundary_collisions(body)

    for body in self.bodies:
      body.resolve_forces(time)
      body.force = Vector2d(0, 0)
