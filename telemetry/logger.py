import json
import os

class TelemetryLogger:
    """Writes spacecraft state readings to a log file, one JSON object per line."""

    def __init__(self, log_path="telemetry/telemetry.log"):
        self.log_path = log_path
        # Make sure the folder for the log file exists
        os.makedirs(os.path.dirname(self.log_path), exist_ok=True)

    def log(self, state):
        """Append one spacecraft state reading to the log file."""
        with open(self.log_path, "a") as f:
            f.write(json.dumps(state) + "\n")

    def read_all(self):
        """Read every logged reading back as a list of dictionaries."""
        readings = []
        if not os.path.exists(self.log_path):
            return readings
        with open(self.log_path, "r") as f:
            for line in f:
                line = line.strip()
                if line:
                    readings.append(json.loads(line))
        return readings
