from telemetry.logger import TelemetryLogger
import matplotlib.pyplot as plt

logger = TelemetryLogger(log_path="telemetry/anomaly_demo.log")
readings = logger.read_all()

timestamps = [r["timestamp"] for r in readings]
temperatures = [r["temperature"] for r in readings]

# Use simple index numbers (0,1,2,...) on the x-axis instead of full timestamps,
# since full timestamps are long and cluttered for a small chart like this.
tick_numbers = list(range(len(temperatures)))

plt.plot(tick_numbers, temperatures, marker="o")
plt.title("Spacecraft Temperature Over Time (Thermal Anomaly Demo)")
plt.xlabel("Tick Number")
plt.ylabel("Temperature (C)")
plt.grid(True)
plt.savefig("telemetry/temperature_chart.png")
print("Chart saved to telemetry/temperature_chart.png")
