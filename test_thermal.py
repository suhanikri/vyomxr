from simulator.thermal import ThermalSubsystem
import time

thermal = ThermalSubsystem()

print("--- Normal operation ---")
for i in range(5):
    thermal.update()
    print(thermal.get_state())
    time.sleep(0.5)

print("--- Anomaly triggered ---")
thermal.set_anomaly(True)
for i in range(5):
    thermal.update()
    print(thermal.get_state())
    time.sleep(0.5)
