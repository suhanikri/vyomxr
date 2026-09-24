from simulator.spacecraft import Spacecraft
from simulator.simulation_loop import SimulationLoop
from telemetry.logger import TelemetryLogger
from anomaly.detector import AnomalyDetector
import time
import os

# Fresh log for this test
log_path = "telemetry/full_anomaly_demo.log"
if os.path.exists(log_path):
    os.remove(log_path)

craft = Spacecraft()
logger = TelemetryLogger(log_path=log_path)
loop = SimulationLoop(craft, tick_rate=1.0, telemetry_logger=logger)

print("Starting simulation (normal operation)...")
loop.start()
time.sleep(3)

print("Triggering ALL FOUR anomalies...")
craft.power.percentage = 15.0  # push battery low so it crosses threshold soon
craft.thermal.set_anomaly(True)
craft.attitude.set_anomaly(True)
craft.communication.set_anomaly(True)
time.sleep(5)

print("Stopping simulation...")
loop.stop()
print("Stopped.")

print("--- Running anomaly detector over full log ---")
detector = AnomalyDetector()
readings = logger.read_all()

for i, reading in enumerate(readings):
    anomalies = detector.check(reading)
    if anomalies:
        print(f"Tick {i}: {len(anomalies)} anomaly(ies)")
        for a in anomalies:
            print(f"   - [{a['subsystem']}/{a['severity']}] {a['reason']}")
    else:
        print(f"Tick {i}: OK")
