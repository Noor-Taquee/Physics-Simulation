"""
The logic for simulations
"""

from collections import defaultdict
from dataclasses import dataclass
from typing import Callable, Any, Literal
from math import atan2, degrees, sqrt

EventMap = defaultdict[str, list[Callable]]


@dataclass
class i2d:
  """A 2-dimensional identity"""

  x: float = 0
  y: float = 0


# MARK: vector 2d
class Vector2d(i2d):
  def __init__(self, x: float = 0, y: float = 0):
    super().__init__(x, y)

  def __call__(self) -> Any:
    return self.magnitude()

  def __add__(self, other: "Vector2d") -> "Vector2d":
    if not isinstance(other, Vector2d):
      return NotImplemented
    return Vector2d(self.x + other.x, self.y + other.y)

  def __iadd__(self, other: "Vector2d") -> "Vector2d":
    if not isinstance(other, Vector2d):
      return NotImplemented
    self.x += other.x
    self.y += other.y
    return self

  def __sub__(self, other: "Vector2d") -> "Vector2d":
    if not isinstance(other, Vector2d):
      return NotImplemented
    return Vector2d(self.x - other.x, self.y - other.y)

  def __isub__(self, other: "Vector2d") -> "Vector2d":
    if not isinstance(other, Vector2d):
      return NotImplemented
    self.x -= other.x
    self.y -= other.y
    return self

  def __mul__(self, scalar: int | float) -> "Vector2d":
    if not isinstance(scalar, (int, float)):
      return NotImplemented
    return Vector2d(self.x * scalar, self.y * scalar)

  def __imul__(self, scalar: int | float) -> "Vector2d":
    if not isinstance(scalar, (int, float)):
      return NotImplemented
    self.x *= scalar
    self.y *= scalar
    return self

  def __rmul__(self, scalar: int | float):
    if not isinstance(scalar, (int, float)):
      return NotImplemented
    return self.__mul__(scalar)

  def __truediv__(self, scalar: int | float) -> "Vector2d":
    if not isinstance(scalar, (int, float)):
      return NotImplemented
    if scalar == 0:
      raise ZeroDivisionError("Cannot divide a vector by 0.")
    reciprocal = 1 / scalar
    return Vector2d(self.x * reciprocal, self.y * reciprocal)

  def __itruediv__(self, scalar: int | float):
    if not isinstance(scalar, (int, float)):
      return NotImplemented
    if scalar == 0:
      raise ZeroDivisionError("Cannot divide a vector by 0.")
    reciprocal = 1 / scalar
    self.x *= reciprocal
    self.y *= reciprocal
    return self

  def magnitude(self):
    return sqrt(self.x**2 + self.y**2)

  def angle_in_radians(self) -> float:
    angle = atan2(self.y, self.x)
    return angle

  def angle_in_degrees(self) -> float:
    return degrees(self.angle_in_radians())


K = 9 * (10**9)
"""**Electrostatic constant**"""

G = 1
"""**Gravitational constant**"""

RGBColor255 = tuple[int, int, int]

BodyEventType = Literal["update", "reset"]
BodyEventMap = dict[BodyEventType, list[Callable[..., Any]]]


# MARK: eventTarget
class EventTarget:
  def __init__(self):
    self.eventMap: BodyEventMap = {}

  def add_event_listener(
    self, name: BodyEventType, callback: Callable[["PhysicsBody"], Any]
  ):
    """Calls the passed `callback` function when the specified event is triggered."""
    if name not in self.eventMap:
      self.eventMap[name] = []
    self.eventMap[name].append(callback)

  def remove_event_listener(
    self, name: BodyEventType, callback: Callable[["PhysicsBody"], Any]
  ):
    """Removes the `callback` function from the stack."""

    if name not in self.eventMap.keys():
      return
    callback_stack = self.eventMap[name]
    if callback not in callback_stack:
      return
    callback_stack.remove(callback)

  def dispatch_event(self, name: BodyEventType, detail: Any) -> None:
    if name not in self.eventMap:
      self.eventMap[name] = []
    for callback in self.eventMap[name]:
      callback(detail)


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
    super().__init__()
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

    self.dispatch_event("reset", self)

  def momentum(self) -> float:
    return self.velocity.magnitude() * self.mass

  def calculate(self, time: float | int) -> None:
    if self.mass == 0:
      return

    # acceleration
    self.acceleration += self.force / self.mass
    self.force = Vector2d(0, 0)

    # velocity
    self.velocity += self.acceleration * time
    self.acceleration = Vector2d(0, 0)

    # position
    self.position += self.velocity * time

    self.dispatch_event("update", self)


# MARK: Environment
class Environment:
  acceleration: Vector2d
  """Environment acceleration"""
  force: Vector2d
  """Environment force"""
  bodies: list[PhysicsBody]
  """list of bodies for the calculation"""
  min_dis_for_calc: float
  """Minimum distance to stop calculating the force."""
  height: float | None
  width: float | None
  boundary_collisions: bool
  """Switch to enable/disable boundary collisions"""
  top_boundary: float | None
  left_boundary: float | None
  bottom_boundary: float | None
  right_boundary: float | None

  def __init__(self):
    self.acceleration = Vector2d(0, 0)
    self.force = Vector2d(0, 0)
    self.bodies = []
    self.min_dis_for_calc = 2
    self.boundary_collisions = False
    self.top_boundary = None
    self.right_boundary = None
    self.bottom_boundary = None
    self.left_boundary = None

  def register(self, *bodies: PhysicsBody):
    """Adds the body in the calculation loop"""
    for body in bodies:
      if body not in self.bodies:
        self.bodies.append(body)

  def calculate(self, time: float):
    """Calculates forces between bodies."""
    number_of_bodies = len(self.bodies)
    for i in range(number_of_bodies):
      body = self.bodies[i]

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

      # Inject environment properties
      body.acceleration += self.acceleration
      body.force += self.force

      # boundary collisions
      if self.boundary_collisions:
        if self.right_boundary is not None:
          if body.position.x + body.radius >= self.right_boundary:
            body.position.x = self.right_boundary - body.radius
            body.velocity.x = -abs(body.velocity.x) * body.elastic_coefficient

        if self.left_boundary is not None:
          if body.position.x - body.radius <= self.left_boundary:
            body.position.x = self.left_boundary + body.radius
            body.velocity.x = abs(body.velocity.x) * body.elastic_coefficient

        if self.top_boundary is not None:
          if body.position.y + body.radius >= self.top_boundary:
            body.position.y = self.top_boundary - body.radius
            body.velocity.y = -abs(body.velocity.y) * body.elastic_coefficient

        if self.bottom_boundary is not None:
          if body.position.y - body.radius <= self.bottom_boundary:
            body.position.y = self.bottom_boundary + body.radius
            body.velocity.y = abs(body.velocity.y) * body.elastic_coefficient

      body.calculate(time)
