"""
The logic for simulations
"""

from dataclasses import dataclass
from typing import Callable, Any, Literal

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

BodyEventType = Literal["update","reset"]
BodyEventMap = dict[BodyEventType, list[Callable]]

# MARK: body
class Body:
  """Simulation Body"""
  
  def __init__(self, name: str, mass: float, x: float, y: float, color = "white"):
    self.name = name
    self.mass = mass
    self.charge = 0
    self.defaultPosition = i2d(x,y)
    self.color = "white"
    self.shape = "circle"
    self.size = 0
    
    self.eventMap: BodyEventMap = {
      "update": [],
      "reset": []
    }
    
    simState.bodies.append(self)
    self.reset()

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
    if not name in self.eventMap.keys(): return;
  
    self.eventMap[name].append(callback);

  def remove_event_listener(self, name: BodyEventType, callback: Callable[['Body'], Any]):
    if not name in self.eventMap.keys(): return;
    callback_stack = self.eventMap[name];
    
    if not callback in callback_stack: return;
    callback_stack.remove(callback);

def calc(p):
  if (5-5 == 0): tr = True
  else: tr = False
  return tr

# MARK: state
@dataclass
class SimState:
  """Object for state of program"""

  bodies: list[Body];

  flowSwitch = False;
  """Toggle to control the mainloop"""

simState = SimState([])

def mainloop(time: float):
  if not simState.flowSwitch: return;
  
  for i in range(len(simState.bodies)):
    o_body = simState.bodies[i]
    
    for j in range(len(simState.bodies)):
      if (i == j): continue;
      c_body = simState.bodies[j]
      
      # MARK: distance
      dx = c_body.position.x - o_body.position.x
      dy = c_body.position.y - o_body.position.y

      if (dx == 0 or dy == 0): continue;
      
      # MARK: gravitational force
      o_body.force.x += G * c_body.mass * o_body.mass / (dx * dx)
      o_body.force.y += G * c_body.mass * o_body.mass / (dy * dy)
    
    o_body.calculate(time);
