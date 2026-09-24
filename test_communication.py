from simulator.communication import CommunicationSubsystem
import time

comms = CommunicationSubsystem()

print("--- Normal operation ---")
for i in range(5):
    comms.update()
    print(comms.get_state())
    time.sleep(0.5)

print("--- Anomaly triggered (signal degrading) ---")
comms.set_anomaly(True)
for i in range(6):
    comms.update()
    print(comms.get_state())
    time.sleep(0.5)
