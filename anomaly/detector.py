class AnomalyDetector:
    """Detects anomalies across all spacecraft subsystems using thresholds and rate-of-change."""

    def __init__(self):
        self.previous_state = None

        # Power thresholds
        self.battery_percentage_min = 10.0
        self.battery_percentage_rate_limit = 0.5   # max allowed drop per tick

        # Thermal thresholds
        self.temperature_max = 30.0
        self.temperature_rate_limit = 0.3

        # Attitude thresholds
        self.angular_velocity_max = 0.3
        self.angular_velocity_rate_limit = 0.1

        # Communication thresholds
        self.signal_strength_rate_limit = 3.0      # max allowed drop per tick

    def check(self, current_state):
        """Compare current telemetry against thresholds and previous readings.
        Returns a list of anomaly dictionaries (empty list means all healthy)."""
        anomalies = []

        anomalies += self._check_power(current_state)
        anomalies += self._check_thermal(current_state)
        anomalies += self._check_attitude(current_state)
        anomalies += self._check_communication(current_state)

        # Remember this reading for next time's rate-of-change checks
        self.previous_state = current_state

        return anomalies

    def _check_power(self, current):
        anomalies = []
        percentage = current["battery_percentage"]

        if percentage < self.battery_percentage_min:
            anomalies.append({
                "subsystem": "power",
                "reading": percentage,
                "reason": f"Battery percentage {percentage}% below safe minimum {self.battery_percentage_min}%",
                "severity": "high",
            })

        if self.previous_state is not None:
            drop = self.previous_state["battery_percentage"] - percentage
            if drop > self.battery_percentage_rate_limit:
                anomalies.append({
                    "subsystem": "power",
                    "reading": percentage,
                    "reason": f"Battery draining too fast: -{round(drop, 2)}% per tick",
                    "severity": "medium",
                })

        return anomalies

    def _check_thermal(self, current):
        anomalies = []
        temperature = current["temperature"]

        if temperature > self.temperature_max:
            anomalies.append({
                "subsystem": "thermal",
                "reading": temperature,
                "reason": f"Temperature {temperature} exceeds safe maximum {self.temperature_max}",
                "severity": "high",
            })

        if self.previous_state is not None:
            change = temperature - self.previous_state["temperature"]
            if change > self.temperature_rate_limit:
                anomalies.append({
                    "subsystem": "thermal",
                    "reading": temperature,
                    "reason": f"Temperature rising too fast: +{round(change, 2)} per tick",
                    "severity": "medium",
                })

        return anomalies

    def _check_attitude(self, current):
        anomalies = []
        angular_velocity = abs(current["angular_velocity"])

        if angular_velocity > self.angular_velocity_max:
            anomalies.append({
                "subsystem": "attitude",
                "reading": angular_velocity,
                "reason": f"Angular velocity {angular_velocity} exceeds safe maximum {self.angular_velocity_max}",
                "severity": "high",
            })

        if self.previous_state is not None:
            previous_angular_velocity = abs(self.previous_state["angular_velocity"])
            change = angular_velocity - previous_angular_velocity
            if change > self.angular_velocity_rate_limit:
                anomalies.append({
                    "subsystem": "attitude",
                    "reading": angular_velocity,
                    "reason": f"Angular velocity increasing too fast: +{round(change, 3)} per tick",
                    "severity": "medium",
                })

        return anomalies

    def _check_communication(self, current):
        anomalies = []
        link_status = current["link_status"]
        signal_strength = current["signal_strength"]

        if link_status in ("degraded", "lost"):
            anomalies.append({
                "subsystem": "communication",
                "reading": link_status,
                "reason": f"Communication link status is '{link_status}'",
                "severity": "high" if link_status == "lost" else "medium",
            })

        if self.previous_state is not None:
            drop = self.previous_state["signal_strength"] - signal_strength
            if drop > self.signal_strength_rate_limit:
                anomalies.append({
                    "subsystem": "communication",
                    "reading": signal_strength,
                    "reason": f"Signal strength dropping too fast: -{round(drop, 2)} per tick",
                    "severity": "medium",
                })

        return anomalies
