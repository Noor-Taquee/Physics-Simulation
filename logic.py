"""
The logic for simulations
"""

from dataclasses import dataclass
from typing import Callable, Any, Literal
from math import sqrt

EventMap = dict[str, list[Callable]]

# MARK: i2d
@dataclass
class i2d:
  """A 2-dimensional identity"""
  x: float = 0
  y: float = 0

K = 9*(10**9)
"""**Electrostatic constant**"""

G = 50
"""**Gravitational constant**"""

RGBColor255 = tuple[int, int, int]

BodyEventType = Literal["update","reset"]
BodyEventMap = dict[BodyEventType, list[Callable]]

# MARK: body
class Body:
  """Simulation Body"""
  
  def __init__(self, name: str, mass: float, charge: float, x: float, y: float, color: RGBColor255 = (255, 255, 255)):
    self.name = name
    self.mass = mass
    """Mass of the body in *kilograms*"""
    self.charge = charge
    """Charge of the body in *quloumb*"""
    self.defaultPosition = i2d(x,y)
    self.color = color
    self.shape = "circle"
    self.size = 0
    """multipliyer of the default size"""

    self.position = i2d(self.defaultPosition.x, self.defaultPosition.y)
    self.velocity = i2d(0,0)
    """Velocity of the body in *m/s*"""
    self.acceleration = i2d(0,0);
    self.force = i2d(0,0)
    
    self.eventMap: BodyEventMap = {
      "update": [],
      "reset": []
    }

  def register(self):
    """Adds the body in the calculation loop"""
    if (simState.bodies.__contains__(self)): return;
    simState.bodies.append(self)

  def reset(self):
    self.position = i2d(self.defaultPosition.x, self.defaultPosition.y)
    self.velocity = i2d(0,0)
    self.acceleration = i2d(0,0);
    self.force = i2d(0,0)
    
    for i in self.eventMap["reset"]:
      i(self)

  def calculate(self, time: float|int):
    if (self.mass == 0): return
    
    # acceleration
    self.acceleration.x = self.force.x / self.mass
    self.acceleration.y = self.force.y / self.mass
    self.force = i2d(0,0)

    # velocity
    self.velocity.x += self.acceleration.x * time
    self.velocity.y += self.acceleration.y * time
    self.acceleration = i2d(0,0)

    # position
    self.position.x += self.velocity.x * time
    self.position.y += self.velocity.y * time

    for i in self.eventMap["update"]:
      i(self)

  def add_event_listener(self, name: BodyEventType, callback: Callable[['Body'], Any]):
    """Calls the passed `callback` function when the specified event is triggered."""
    if not name in self.eventMap.keys(): return;
  
    self.eventMap[name].append(callback);

  def remove_event_listener(self, name: BodyEventType, callback: Callable[['Body'], Any]):
    """Removes the `callback` function from the stack."""
    
    if not name in self.eventMap.keys(): return;
    callback_stack = self.eventMap[name];
    
    if not callback in callback_stack: return;
    callback_stack.remove(callback);

# MARK: state
@dataclass
class SimState:
  """Object for state of program"""

  bodies: list[Body];

  flowSwitch = False;
  """Toggle to control the mainloop"""

  min_dis_for_calc = 5;
  """Minimum distance to stop calculating the force."""

simState = SimState([])



def mainloop(time: float):
  if not simState.flowSwitch: return;
  
  for i in range(len(simState.bodies)):
    body = simState.bodies[i]
    
    for j in range(len(simState.bodies)):
      if (i == j): continue;
      body_2 = simState.bodies[j]
      
      # MARK: distance
      dx = body_2.position.x - body.position.x
      dy = body_2.position.y - body.position.y
      dis = sqrt(dx*dx + dy*dy)
      if (dis == 0 or dis <= simState.min_dis_for_calc): continue;
      
      # MARK: gravitational force
      force = G * body_2.mass * body.mass / (dis * dis)
      body.force.x += force * dx/dis
      body.force.y += force * dy/dis
      
      # MARK: electrostatic force
      force = K * body_2.charge * body.charge / (dis * dis)
      body.force.x += force * dx/dis
      body.force.y += force * dy/dis
    
    body.calculate(time);
