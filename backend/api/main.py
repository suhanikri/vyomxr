from fastapi import FastAPI
from simulator.spacecraft import Spacecraft
from simulator.simulation_loop import SimulationLoop
from telemetry.logger import TelemetryLogger
from anomaly.detector import AnomalyDetector

app = FastAPI(title="VyomXR Backend")

craft = Spacecraft()
logger = TelemetryLogger(log_path="telemetry/live.log")
detector = AnomalyDetector()

# Shared storage for the most recently detected anomalies
latest_anomalies = []

def handle_anomaly(anomalies):
    """Store the latest anomalies so the API can serve them on request."""
    global latest_anomalies
    latest_anomalies = anomalies
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
    loop.start()


@app.on_event("shutdown")
def stop_simulation():
    loop.stop()


@app.get("/spacecraft/state")
def get_spacecraft_state():
    """Return the spacecraft's current state as JSON."""
    return loop.get_latest_state()


@app.get("/spacecraft/anomalies")
def get_anomalies():
    """Return the anomalies found on the most recent tick (empty list if none)."""
    return {"anomalies": latest_anomalies}


@app.get("/telemetry/history")
def get_telemetry_history(limit: int = 50):
    """Return the last `limit` telemetry readings."""
    readings = logger.read_all()
    return {"readings": readings[-limit:]}
