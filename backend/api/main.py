from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from simulator.spacecraft import Spacecraft
from simulator.simulation_loop import SimulationLoop
from telemetry.logger import TelemetryLogger
from anomaly.detector import AnomalyDetector
from mentor.ai_mentor import AIMentor

app = FastAPI(title="VyomXR Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

craft = Spacecraft()
logger = TelemetryLogger(log_path="telemetry/live.log")
detector = AnomalyDetector()
mentor = AIMentor()

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


class MentorQuestion(BaseModel):
    question: str


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


@app.post("/mentor/ask")
def ask_mentor(payload: MentorQuestion):
    """Ask the AI Mentor a question, automatically grounded in live spacecraft data."""
    state = loop.get_latest_state()
    answer = mentor.ask(payload.question, state, latest_anomalies)
    return {"answer": answer}


@app.post("/test/trigger-anomaly/{subsystem}")
def trigger_anomaly(subsystem: str):
    if subsystem == "thermal":
        craft.thermal.set_anomaly(True)
    elif subsystem == "power":
        craft.power.set_anomaly(True)
    elif subsystem == "attitude":
        craft.attitude.set_anomaly(True)
    elif subsystem == "communication":
        craft.communication.set_anomaly(True)
    else:
        return {"error": f"Unknown subsystem: {subsystem}"}
    return {"message": f"Anomaly triggered on {subsystem}"}


@app.post("/test/clear-anomaly/{subsystem}")
def clear_anomaly(subsystem: str):
    if subsystem == "thermal":
        craft.thermal.set_anomaly(False)
    elif subsystem == "power":
        craft.power.set_anomaly(False)
    elif subsystem == "attitude":
        craft.attitude.set_anomaly(False)
    elif subsystem == "communication":
        craft.communication.set_anomaly(False)
    else:
        return {"error": f"Unknown subsystem: {subsystem}"}
    return {"message": f"Anomaly cleared on {subsystem}"}
