from logic import Body, mainloop, simState

# 1. Define a callback
def log_position(body: Body):
    print(f"{body.name} position: ({body.position.x:.2f}, {body.position.y:.2f})")

# 2. Setup bodies
body1 = Body("name-1", 1e15, 100, 50) # Increased mass to see movement
body1.add_event_listener("update", log_position)

body2 = Body("name-2", 1e15, 200, 78)
body2.add_event_listener("update", log_position)

# 3. Add them to the state and Flip the switch
simState.bodies = [body1, body2]
simState.flowSwitch = True

# 4. Run simulation
print("Starting simulation...")
for i in range(500):
    mainloop(0.01) # Using a slightly larger dt to see results faster