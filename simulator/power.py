import random

class PowerSubsystem:
    """Simulates a spacecraft's power subsystem: battery voltage, current, and charge."""

    def __init__(self):
        self.voltage = 12.6          # volts, starts fully charged
        self.current = 2.0           # amps, positive = discharging
        self.percentage = 100.0      # battery charge percent
        self.anomaly_active = False  # whether a power fault is currently happening

    def set_anomaly(self, active: bool):
        """Turn the power anomaly (fast drain) on or off (used by scenarios later)."""
        self.anomaly_active = active

    def update(self):
        """Advance the simulation by one time step."""
        if self.anomaly_active:
            # Battery drains much faster during a fault
            self.percentage -= random.uniform(1.0, 2.0)
            # Current spikes higher, simulating excess draw
            self.current = 4.0 + random.uniform(-0.2, 0.2)
        else:
            # Normal operation: battery slowly discharges over time
            self.percentage -= 0.05
            # Current fluctuates slightly around 2.0 amps
            self.current = 2.0 + random.uniform(-0.1, 0.1)

        # Voltage drops as percentage drops, plus small random noise
        self.voltage = 10.0 + (self.percentage / 100.0) * 2.6 + random.uniform(-0.05, 0.05)

        # Keep percentage from going below 0
        if self.percentage < 0:
            self.percentage = 0

    def get_state(self):
        """Return the current power subsystem readings as a dictionary."""
        return {
            "battery_voltage": round(self.voltage, 2),
            "battery_current": round(self.current, 2),
            "battery_percentage": round(self.percentage, 2),
        }
