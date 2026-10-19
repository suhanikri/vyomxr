import random


class ThermalSubsystem:
    """Simulates a spacecraft's thermal subsystem: internal temperature.
    Scenario: a cooling loop failure that the student can respond to."""

    MAX_TEMPERATURE = 100.0   # ceiling, so a runaway fault stays believable

    def __init__(self):
        self.temperature = 25.0      # degrees Celsius, normal operating temp
        self.anomaly_active = False  # whether a thermal fault is happening
        self.heating_multiplier = 1.0   # above 1 heats faster, below 1 slower
        self.cooling_boost_ticks = 0    # ticks of extra cooling after a fix

    def set_anomaly(self, active: bool):
        """Turn the thermal anomaly on or off (used by scenarios).
        Either way, any earlier recovery effects are reset."""
        self.anomaly_active = active
        self.heating_multiplier = 1.0
        self.cooling_boost_ticks = 0

    def update(self):
        """Advance the simulation by one time step."""
        if self.anomaly_active:
            # Temperature climbs during a fault, scaled by the student's actions
            self.temperature += random.uniform(0.3, 0.6) * self.heating_multiplier
        else:
            # Normal operation: small noise, pulled gently back toward 25
            self.temperature += random.uniform(-0.1, 0.1)
            pull = 0.05
            if self.cooling_boost_ticks > 0:
                pull = 0.2   # backup cooling removes heat faster
                self.cooling_boost_ticks -= 1
            self.temperature += (25.0 - self.temperature) * pull

        self.temperature = min(self.temperature, self.MAX_TEMPERATURE)

    def apply_action(self, action: str):
        """Apply a student recovery action. Returns a dictionary describing
        the effect, which the Evaluation step will use later."""
        if action == "switch_to_backup_cooling":
            if self.anomaly_active:
                self.anomaly_active = False
                self.heating_multiplier = 1.0
                self.cooling_boost_ticks = 15
                return {
                    "action": action,
                    "effect": "resolved",
                    "message": "Backup cooling loop engaged. Heat is being removed.",
                }
            return {
                "action": action,
                "effect": "no_effect",
                "message": "No thermal fault is active, so nothing changed.",
            }

        if action == "reduce_payload_power":
            if self.anomaly_active:
                self.heating_multiplier = min(self.heating_multiplier, 0.4)
                return {
                    "action": action,
                    "effect": "partial",
                    "message": "Heat generation reduced, but the cooling fault is still active.",
                }
            return {
                "action": action,
                "effect": "no_effect",
                "message": "No thermal fault is active, so nothing changed.",
            }

        if action == "reorient_toward_sun":
            if self.anomaly_active:
                self.heating_multiplier = 1.5
                return {
                    "action": action,
                    "effect": "worsened",
                    "message": "Facing the Sun adds heat. The temperature will rise faster.",
                }
            return {
                "action": action,
                "effect": "no_effect",
                "message": "No thermal fault is active, so nothing changed.",
            }

        return {
            "action": action,
            "effect": "unknown_action",
            "message": "This action is not available for the thermal subsystem.",
        }

    def get_state(self):
        """Return the current thermal subsystem readings as a dictionary."""
        return {
            "temperature": round(self.temperature, 2),
        }
