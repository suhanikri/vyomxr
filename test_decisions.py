from simulator.spacecraft import Spacecraft

# 1. A rejected action is recorded and changes nothing
craft = Spacecraft()
record = craft.execute_action("launch_fireworks")
assert record["allowed"] is False
assert record["effect"] == "rejected"
assert record["subsystem"] is None
print("1. Unknown action is rejected and recorded")

# 2. A valid action with no fault active
craft = Spacecraft()
craft.update()
record = craft.execute_action("switch_to_backup_cooling")
assert record["allowed"] is True
assert record["effect"] == "no_effect"
assert record["fault_active"] is False
assert record["ticks_since_fault"] is None
print("2. Valid action with no fault: recorded as no_effect")

# 3. Acting during a fault: response time and the fix
craft = Spacecraft()
craft.thermal.set_anomaly(True)
for _ in range(5):
    craft.update()
assert craft.fault_start_ticks == {"thermal": 1}
record = craft.execute_action("switch_to_backup_cooling")
assert record["effect"] == "resolved"
assert record["fault_active"] is True
assert record["ticks_since_fault"] == 4
assert record["tick"] == 5
print("3. Fault at tick 1, student acted at tick 5: ticks_since_fault = 4")

# 4. After the fix, the next update clears the fault timer
craft.update()
assert craft.fault_start_ticks == {}
print("4. Fault timer clears once the fault is resolved")

# 5. A bad choice is recorded as worsened
craft = Spacecraft()
craft.thermal.set_anomaly(True)
for _ in range(3):
    craft.update()
record = craft.execute_action("reorient_toward_sun")
assert record["effect"] == "worsened"
print("5. A harmful choice is recorded as worsened")

# 6. The decision record is complete and returned as a copy
craft = Spacecraft()
craft.execute_action("launch_fireworks")
craft.execute_action("reduce_payload_power")
decisions = craft.get_decisions()
assert len(decisions) == 2
decisions.clear()
assert len(craft.get_decisions()) == 2
print("6. Decisions are kept in order and the returned list is a copy")

# 7. Normal state reporting still works
state = craft.get_state()
assert "temperature" in state and "battery_voltage" in state
assert "signal_strength" in state and "angular_velocity" in state
print("7. get_state still reports all four subsystems")

print("\nAll decision tests passed.")
