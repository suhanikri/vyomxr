from simulator.spacecraft import Spacecraft
from simulator.simulation_loop import SimulationLoop
from telemetry.logger import TelemetryLogger
import time
import os

# Start fresh: remove old log file so this demo is easy to read
log_path = "telemetry/anomaly_demo.log"
if os.path.exists(log_path):
    os.remove(log_path)

craft = Spacecraft()
logger = TelemetryLogger(log_path=log_path)
loop = SimulationLoop(craft, tick_rate=1.0, telemetry_logger=logger)

print("Starting simulation loop (normal operation)...")
loop.start()

time.sleep(4)

print("Triggering thermal anomaly...")
craft.thermal.set_anomaly(True)

time.sleep(4)

print("Stopping simulation loop...")
loop.stop()
print("Stopped.")

print("--- Reading back logged telemetry (temperature only) ---")
readings = logger.read_all()
for r in readings:
    print(f"{r['timestamp']}  temperature={r['temperature']}")
