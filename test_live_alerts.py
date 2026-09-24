from simulator.spacecraft import Spacecraft
from simulator.simulation_loop import SimulationLoop
from telemetry.logger import TelemetryLogger
from anomaly.detector import AnomalyDetector
import time
import os

log_path = "telemetry/live_alert_demo.log"
if os.path.exists(log_path):
    os.remove(log_path)

def handle_anomaly(anomalies):
    """This function gets called automatically the instant anomalies are found."""
    for a in anomalies:
        print(f"  ?? ALERT [{a['subsystem']}/{a['severity']}] {a['reason']}")

craft = Spacecraft()
logger = TelemetryLogger(log_path=log_path)
detector = AnomalyDetector()

loop = SimulationLoop(
    craft,
    tick_rate=1.0,
    telemetry_logger=logger,
    anomaly_detector=detector,
    on_anomaly=handle_anomaly,
)

print("Starting simulation (normal operation)...")
loop.start()
time.sleep(3)

print("Triggering thermal + attitude anomalies...")
craft.thermal.set_anomaly(True)
craft.attitude.set_anomaly(True)
time.sleep(5)

print("Stopping simulation...")
loop.stop()
print("Stopped.")
