from simulator.power import PowerSubsystem
from simulator.thermal import ThermalSubsystem
from simulator.attitude import AttitudeSubsystem
from simulator.communication import CommunicationSubsystem
import datetime

class Spacecraft:
    """Combines all subsystems into one spacecraft with a single state."""

    def __init__(self):
        self.power = PowerSubsystem()
        self.thermal = ThermalSubsystem()
        self.attitude = AttitudeSubsystem()
        self.communication = CommunicationSubsystem()

    def update(self):
        """Advance every subsystem by one time step."""
        self.power.update()
        self.thermal.update()
        self.attitude.update()
        self.communication.update()

    def get_state(self):
        """Return the combined state of the whole spacecraft."""
        state = {
            "timestamp": datetime.datetime.utcnow().isoformat(),
        }
        state.update(self.power.get_state())
        state.update(self.thermal.get_state())
        state.update(self.attitude.get_state())
        state.update(self.communication.get_state())
        return state
