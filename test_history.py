from simulator.spacecraft import Spacecraft
from simulator.simulation_loop import SimulationLoop
import time

# Small memory (5) and fast ticks so the test takes about 2 seconds.
loop = SimulationLoop(Spacecraft(), tick_rate=0.1, history_size=5)

# Before starting, there is no history.
assert loop.get_recent_states() == []
print("Before start: history is empty")

loop.start()
time.sleep(1.5)   # about 15 ticks, far more than the memory of 5
loop.stop()

states = loop.get_recent_states()
print("Stored readings:", len(states), "(memory cap is 5)")
assert len(states) == 5

# Oldest first means timestamps only go up.
timestamps = [s["timestamp"] for s in states]
assert timestamps == sorted(timestamps)
print("Order is oldest to newest")

# Asking for the newest 2.
last_two = loop.get_recent_states(2)
assert len(last_two) == 2
assert last_two[-1] == states[-1]
print("get_recent_states(2) returned the newest 2")

print("\nAll history tests passed.")
