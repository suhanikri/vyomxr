from simulator.spacecraft import Spacecraft
from simulator.simulation_loop import SimulationLoop
from telemetry.logger import TelemetryLogger
import time

craft = Spacecraft()
logger = TelemetryLogger()
loop = SimulationLoop(craft, tick_rate=1.0, telemetry_logger=logger)

print("Starting simulation loop with telemetry logging...")
loop.start()

time.sleep(5)

print("Stopping simulation loop...")
loop.stop()
print("Stopped.")

print("--- Reading back logged telemetry ---")
readings = logger.read_all()
for r in readings:
    print(r)
