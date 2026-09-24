from simulator.spacecraft import Spacecraft
from simulator.simulation_loop import SimulationLoop
import time

craft = Spacecraft()
loop = SimulationLoop(craft, tick_rate=1.0)

print("Starting simulation loop...")
loop.start()

for i in range(5):
    time.sleep(1)
    print(loop.get_latest_state())

print("Stopping simulation loop...")
loop.stop()
print("Stopped.")
