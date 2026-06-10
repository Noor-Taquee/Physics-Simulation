from src.pygame.core.logic import Environment, PhysicsBody


def log_position(body: PhysicsBody):
  print(f"{body.name} position: ({body.position.x:.2f}, {body.position.y:.2f})")


space = Environment()

# 2. Setup bodies
body1 = PhysicsBody("name-1", 1e15, 100, 50)
body1.add_event_listener("update", log_position)

body2 = PhysicsBody("name-2", 1e15, 200, 78)
body2.add_event_listener("update", log_position)
space.register(body1, body2)

# 4. Run simulation
print("Starting simulation...")
for i in range(500):
  space.calculate(1)
