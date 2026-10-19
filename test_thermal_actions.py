from simulator.thermal import ThermalSubsystem


def run(thermal, ticks):
    for _ in range(ticks):
        thermal.update()


# 1. Unknown action
t = ThermalSubsystem()
result = t.apply_action("launch_fireworks")
assert result["effect"] == "unknown_action"
print("1. Unknown action is rejected")

# 2. Acting when nothing is wrong
t = ThermalSubsystem()
result = t.apply_action("switch_to_backup_cooling")
assert result["effect"] == "no_effect"
print("2. No fault: backup cooling has no effect")

# 3. The correct fix resolves the fault and temperature recovers
t = ThermalSubsystem()
t.set_anomaly(True)
run(t, 10)
assert t.temperature > 27.9, "temperature should have climbed"
result = t.apply_action("switch_to_backup_cooling")
assert result["effect"] == "resolved"
assert t.anomaly_active is False
run(t, 40)
assert abs(t.temperature - 25.0) < 1.0, "temperature should be back near 25"
print("3. Backup cooling resolves the fault and temperature recovers")

# 4. Reduce power slows heating (normal minimum 6.0 beats reduced maximum 4.8)
normal = ThermalSubsystem()
normal.set_anomaly(True)
run(normal, 20)
normal_rise = normal.temperature - 25.0

reduced = ThermalSubsystem()
reduced.set_anomaly(True)
result = reduced.apply_action("reduce_payload_power")
assert result["effect"] == "partial"
run(reduced, 20)
reduced_rise = reduced.temperature - 25.0
assert reduced.anomaly_active is True
assert reduced_rise < normal_rise
print("4. Reducing power slows heating but the fault stays active")

# 5. Facing the Sun worsens the fault
t = ThermalSubsystem()
t.set_anomaly(True)
result = t.apply_action("reorient_toward_sun")
assert result["effect"] == "worsened"
assert t.heating_multiplier == 1.5
print("5. Reorienting toward the Sun makes it worse")

# 6. Temperature ceiling
t = ThermalSubsystem()
t.set_anomaly(True)
run(t, 500)
assert t.temperature == 100.0
print("6. Temperature stops at the 100 C ceiling")

# 7. A new fault starts fresh
t.set_anomaly(True)
assert t.heating_multiplier == 1.0
print("7. A new fault resets earlier recovery effects")

print("\nAll thermal action tests passed.")
