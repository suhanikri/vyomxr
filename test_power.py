from simulator.power import PowerSubsystem
import time

power = PowerSubsystem()

for i in range(10):
    power.update()
    print(power.get_state())
    time.sleep(0.5)
