import random

class AttitudeSubsystem:
    """Simulates a spacecraft's orientation: roll, pitch, yaw, and angular velocity."""

    def __init__(self):
        self.roll = 0.0
        self.pitch = 0.0
        self.yaw = 0.0
        self.angular_velocity = 0.0
        self.anomaly_active = False  # whether a tumbling fault is currently happening

    def set_anomaly(self, active: bool):
        """Turn the attitude anomaly (tumbling) on or off (used by scenarios later)."""
        self.anomaly_active = active

    def update(self):
        """Advance the simulation by one time step."""
        if self.anomaly_active:
            # Angular velocity increases during a fault (losing stabilization)
            self.angular_velocity += random.uniform(0.05, 0.15)
        else:
            # Normal operation: angular velocity stays near zero with tiny noise
            self.angular_velocity += random.uniform(-0.01, 0.01)
            # Gently pull angular velocity back toward zero
            self.angular_velocity += (0.0 - self.angular_velocity) * 0.1

        # Roll, pitch, yaw drift based on current angular velocity
        self.roll += self.angular_velocity * random.uniform(0.5, 1.0)
        self.pitch += self.angular_velocity * random.uniform(0.5, 1.0)
        self.yaw += self.angular_velocity * random.uniform(0.5, 1.0)

    def get_state(self):
        """Return the current attitude subsystem readings as a dictionary."""
        return {
            "roll": round(self.roll, 2),
            "pitch": round(self.pitch, 2),
            "yaw": round(self.yaw, 2),
            "angular_velocity": round(self.angular_velocity, 3),
        }
