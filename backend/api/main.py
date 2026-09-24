from fastapi import FastAPI
from simulator.spacecraft import Spacecraft
from simulator.simulation_loop import SimulationLoop
from telemetry.logger import TelemetryLogger
from anomaly.detector import AnomalyDetector

app = FastAPI(title="VyomXR Backend")

# Create one shared spacecraft, telemetry logger, and detector when the server starts
craft = Spacecraft()
logger = TelemetryLogger(log_path="telemetry/live.log")
detector = AnomalyDetector()

def handle_anomaly(anomalies):
    for a in anomalies:
        print(f"ALERT [{a['subsystem']}/{a['severity']}] {a['reason']}")

loop = SimulationLoop(
    craft,
    tick_rate=1.0,
    telemetry_logger=logger,
    anomaly_detector=detector,
    on_anomaly=handle_anomaly,
)


@app.on_event("startup")
def start_simulation():
    """Start the simulation loop automatically when the server starts."""
    loop.start()


@app.on_event("shutdown")
def stop_simulation():
    """Stop the simulation loop cleanly when the server shuts down."""
    loop.stop()


@app.get("/spacecraft/state")
def get_spacecraft_state():
    """Return the spacecraft's current state as JSON."""
    return loop.get_latest_state()
