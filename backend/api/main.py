from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from simulator.spacecraft import Spacecraft
from simulator.simulation_loop import SimulationLoop
from telemetry.logger import TelemetryLogger
from anomaly.detector import AnomalyDetector

app = FastAPI(title="VyomXR Backend")

# Allow the Next.js frontend (running on a different port) to call this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

craft = Spacecraft()
logger = TelemetryLogger(log_path="telemetry/live.log")
detector = AnomalyDetector()

latest_anomalies = []

def handle_anomaly(anomalies):
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
    return loop.get_latest_state()


@app.get("/spacecraft/anomalies")
def get_anomalies():
    return {"anomalies": latest_anomalies}


@app.get("/telemetry/history")
def get_telemetry_history(limit: int = 50):
    readings = logger.read_all()
    return {"readings": readings[-limit:]}
