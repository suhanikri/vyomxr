import threading
import time

class SimulationLoop:
    """Runs a Spacecraft continuously in the background at a fixed tick rate."""

    def __init__(self, spacecraft, tick_rate=1.0):
        self.spacecraft = spacecraft
        self.tick_rate = tick_rate      # seconds between each update
        self.running = False
        self._thread = None

    def _run(self):
        """Internal loop that keeps updating the spacecraft until stopped."""
        while self.running:
            self.spacecraft.update()
            time.sleep(self.tick_rate)

    def start(self):
        """Start the simulation loop in the background."""
        if self.running:
            return  # already running, do nothing
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
