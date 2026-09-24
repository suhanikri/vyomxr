from telemetry.logger import TelemetryLogger
from anomaly.detector import AnomalyDetector

logger = TelemetryLogger(log_path="telemetry/anomaly_demo.log")
readings = logger.read_all()

detector = AnomalyDetector()

for i, reading in enumerate(readings):
    anomalies = detector.check(reading)
    if anomalies:
        print(f"Tick {i} (temperature={reading['temperature']}): {len(anomalies)} anomaly(ies) found")
        for a in anomalies:
            print(f"   - [{a['severity']}] {a['reason']}")
    else:
        print(f"Tick {i} (temperature={reading['temperature']}): OK")
