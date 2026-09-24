import random

class CommunicationSubsystem:
    """Simulates a spacecraft's communication link: signal strength and packet loss."""

    def __init__(self):
        self.signal_strength = 95.0   # percent, higher is better
        self.packet_loss = 0.01       # fraction, 0.0 = none, 1.0 = all lost
        self.anomaly_active = False   # whether a comms fault is currently happening

    def set_anomaly(self, active: bool):
        """Turn the communication anomaly on or off (used by scenarios later)."""
        self.anomaly_active = active

    def update(self):
        """Advance the simulation by one time step."""
        if self.anomaly_active:
            # Signal degrades steadily during a fault, packet loss rises
            self.signal_strength -= random.uniform(2.0, 5.0)
            self.packet_loss += random.uniform(0.02, 0.05)
        else:
            # Normal operation: signal stays high with small noise
            self.signal_strength += random.uniform(-1.0, 1.0)
            self.packet_loss += random.uniform(-0.005, 0.005)

        # Keep values within realistic bounds
        self.signal_strength = max(0.0, min(100.0, self.signal_strength))
        self.packet_loss = max(0.0, min(1.0, self.packet_loss))

    def _compute_link_status(self):
        """Derive a simple link status label from current readings."""
        if self.signal_strength < 20 or self.packet_loss > 0.5:
            return "lost"
        elif self.signal_strength < 60 or self.packet_loss > 0.15:
            return "degraded"
        else:
            return "nominal"

    def get_state(self):
        """Return the current communication subsystem readings as a dictionary."""
        return {
            "signal_strength": round(self.signal_strength, 2),
            "packet_loss": round(self.packet_loss, 3),
            "link_status": self._compute_link_status(),
        }
