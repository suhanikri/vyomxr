from simulator.spacecraft import Spacecraft
import time

craft = Spacecraft()

for i in range(5):
    craft.update()
    print(craft.get_state())
    time.sleep(0.5)
