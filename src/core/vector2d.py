from __future__ import annotations
from typing import Any
from math import atan2, degrees, sqrt


class Vector2d:
  def __init__(self, x: float = 0, y: float = 0):
    self.x = x
    self.y = y

  def magnitude(self) -> float:
    return sqrt(self.x**2 + self.y**2)

  def angle_in_radians(self) -> float:
    angle = atan2(self.y, self.x)
    return angle

  def angle_in_degrees(self) -> float:
    return degrees(self.angle_in_radians())

  def __call__(self) -> Any:
    return self.magnitude()

  def __add__(self, other: "Vector2d"):
    return Vector2d(self.x + other.x, self.y + other.y)

  def __iadd__(self, other: "Vector2d"):
    self.x += other.x
    self.y += other.y
    return self

  def __sub__(self, other: "Vector2d"):
    return Vector2d(self.x - other.x, self.y - other.y)

  def __isub__(self, other: "Vector2d"):
    self.x -= other.x
    self.y -= other.y
    return self

  def __mul__(self, scalar: int | float):
    return Vector2d(self.x * scalar, self.y * scalar)

  def __imul__(self, scalar: int | float):
    self.x *= scalar
    self.y *= scalar
    return self

  def __rmul__(self, scalar: int | float):
    return self.__mul__(scalar)

  def __truediv__(self, scalar: int | float):
    if scalar == 0:
      raise ZeroDivisionError("Cannot divide a vector by 0.")
    reciprocal = 1 / scalar
    return Vector2d(self.x * reciprocal, self.y * reciprocal)

  def __itruediv__(self, scalar: int | float):
    if scalar == 0:
      raise ZeroDivisionError("Cannot divide a vector by 0.")
    reciprocal = 1 / scalar
    self.x *= reciprocal
    self.y *= reciprocal
    return self
