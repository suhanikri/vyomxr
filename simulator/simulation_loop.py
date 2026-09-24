import threading
import time

class SimulationLoop:
    """Runs a Spacecraft continuously in the background at a fixed tick rate,
    optionally logging telemetry and detecting anomalies in real time."""

    def __init__(self, spacecraft, tick_rate=1.0, telemetry_logger=None,
                 anomaly_detector=None, on_anomaly=None):
        self.spacecraft = spacecraft
        self.tick_rate = tick_rate
        self.telemetry_logger = telemetry_logger
        self.anomaly_detector = anomaly_detector
        self.on_anomaly = on_anomaly   # a function to call when anomalies are found
        self.running = False
        self._thread = None

    def _run(self):
        """Internal loop that keeps updating the spacecraft until stopped."""
        while self.running:
            self.spacecraft.update()
            state = self.spacecraft.get_state()

            if self.telemetry_logger is not None:
                self.telemetry_logger.log(state)

            if self.anomaly_detector is not None:
                anomalies = self.anomaly_detector.check(state)
                if anomalies and self.on_anomaly is not None:
                    self.on_anomaly(anomalies)

            time.sleep(self.tick_rate)

    def start(self):
        """Start the simulation loop in the background."""
        if self.running:
            return
        self.running = True
        self._thread = threading.Thread(target=self._run, daemon=True)
        self._thread.start()

    def stop(self):
        """Stop the simulation loop cleanly."""
        self.running = False
        if self._thread is not None:
            self._thread.join()

    def get_latest_state(self):
        """Return the spacecraft's current state at this moment."""
        return self.spacecraft.get_state()
