from simulator.attitude import AttitudeSubsystem
import time

attitude = AttitudeSubsystem()

print("--- Normal operation ---")
for i in range(5):
    attitude.update()
    print(attitude.get_state())
    time.sleep(0.5)

print("--- Anomaly triggered (tumbling) ---")
attitude.set_anomaly(True)
for i in range(5):
    attitude.update()
    print(attitude.get_state())
    time.sleep(0.5)
