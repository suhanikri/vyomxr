class AnomalyDetector:
    """Detects anomalies in spacecraft telemetry using thresholds and rate-of-change."""

    def __init__(self):
        self.previous_state = None

        # Fixed safe-range thresholds
        self.temperature_max = 30.0          # degrees C, above this is a hard anomaly
        self.temperature_rate_limit = 0.3    # max allowed change per tick before flagging

    def check(self, current_state):
        """Compare current telemetry against thresholds and previous readings.
        Returns a list of anomaly dictionaries (empty list means all healthy)."""
        anomalies = []

        temperature = current_state["temperature"]

        # --- Threshold check ---
        if temperature > self.temperature_max:
            anomalies.append({
                "subsystem": "thermal",
                "reading": temperature,
                "reason": f"Temperature {temperature} exceeds safe maximum {self.temperature_max}",
                "severity": "high",
            })

        # --- Rate-of-change check (only possible if we have a previous reading) ---
        if self.previous_state is not None:
            previous_temperature = self.previous_state["temperature"]
            change = temperature - previous_temperature

            if change > self.temperature_rate_limit:
                anomalies.append({
                    "subsystem": "thermal",
                    "reading": temperature,
                    "reason": f"Temperature rising too fast: +{round(change, 2)} per tick",
                    "severity": "medium",
                })

        # Remember this reading for next time
        self.previous_state = current_state

        return anomalies
