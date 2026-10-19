import datetime
import threading

from simulator.power import PowerSubsystem
from simulator.thermal import ThermalSubsystem
from simulator.attitude import AttitudeSubsystem
from simulator.communication import CommunicationSubsystem

# Recovery actions a student can choose, and which subsystem handles each one.
AVAILABLE_ACTIONS = {
    "switch_to_backup_cooling": "thermal",
    "reduce_payload_power": "thermal",
    "reorient_toward_sun": "thermal",
}

SUBSYSTEM_NAMES = ("power", "thermal", "attitude", "communication")


def _now():
    return datetime.datetime.utcnow().isoformat()


class Spacecraft:
    """Combines all subsystems into one spacecraft with a single state.
    Also validates and executes student recovery actions, and records them."""

    def __init__(self):
        self.power = PowerSubsystem()
        self.thermal = ThermalSubsystem()
        self.attitude = AttitudeSubsystem()
        self.communication = CommunicationSubsystem()

        self.tick_count = 0
        self.fault_start_ticks = {}   # subsystem name -> tick when its fault began
        self._decisions = []
        # The simulation thread and the API thread both touch the spacecraft.
        self._lock = threading.RLock()

    def update(self):
        """Advance every subsystem by one time step."""
        with self._lock:
            self.tick_count += 1
            self.power.update()
            self.thermal.update()
            self.attitude.update()
            self.communication.update()

            # Remember when each fault began, so we can measure response time.
            for name in SUBSYSTEM_NAMES:
                if getattr(self, name).anomaly_active:
                    self.fault_start_ticks.setdefault(name, self.tick_count)
                else:
                    self.fault_start_ticks.pop(name, None)

    def get_state(self):
        """Return the combined state of the whole spacecraft."""
        with self._lock:
            state = {"timestamp": _now()}
            state.update(self.power.get_state())
            state.update(self.thermal.get_state())
            state.update(self.attitude.get_state())
            state.update(self.communication.get_state())
            return state

    def validate_action(self, action):
        """Safety gate: is this action within the simulation's constraints?
        It checks what the simulator can do, not whether the choice is wise."""
        if action not in AVAILABLE_ACTIONS:
            return {"allowed": False, "reason": f"'{action}' is not an available action."}
        return {"allowed": True, "reason": "Action is within simulation constraints."}

    def execute_action(self, action):
        """Validate a student action, apply it, and record the decision.
        Returns the decision record."""
        with self._lock:
            check = self.validate_action(action)
            subsystem_name = AVAILABLE_ACTIONS.get(action)

            fault_start = self.fault_start_ticks.get(subsystem_name)
            fault_active = fault_start is not None
            ticks_since_fault = (self.tick_count - fault_start) if fault_active else None

            if check["allowed"]:
                outcome = getattr(self, subsystem_name).apply_action(action)
            else:
                outcome = {
                    "action": action,
                    "effect": "rejected",
                    "message": check["reason"],
                }

            record = {
                "tick": self.tick_count,
                "timestamp": _now(),
                "action": action,
                "subsystem": subsystem_name,
                "allowed": check["allowed"],
                "effect": outcome["effect"],
                "message": outcome["message"],
                "fault_active": fault_active,
                "ticks_since_fault": ticks_since_fault,
            }
            self._decisions.append(record)
            return record

    def get_decisions(self):
        """Return a copy of every decision recorded so far, oldest first."""
        with self._lock:
            return list(self._decisions)
