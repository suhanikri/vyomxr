import random

class ThermalSubsystem:
    """Simulates a spacecraft's thermal subsystem: internal temperature."""

    def __init__(self):
        self.temperature = 25.0      # degrees Celsius, normal operating temp
        self.anomaly_active = False  # whether a thermal fault is currently happening

    def set_anomaly(self, active: bool):
        """Turn the thermal anomaly on or off (used by scenarios later)."""
        self.anomaly_active = active

    def update(self):
        """Advance the simulation by one time step."""
        if self.anomaly_active:
            # Temperature climbs steadily during a fault, plus noise
            self.temperature += random.uniform(0.3, 0.6)
        else:
            # Normal operation: small random fluctuation around 25 degrees
            self.temperature += random.uniform(-0.1, 0.1)
            # Gently pull temperature back toward 25 if it drifts
            self.temperature += (25.0 - self.temperature) * 0.05

    def get_state(self):
        """Return the current thermal subsystem readings as a dictionary."""
        return {
            "temperature": round(self.temperature, 2),
        }
