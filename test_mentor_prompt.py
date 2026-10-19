from mentor.ai_mentor import AIMentor

mentor = AIMentor()


def make_state(temperature):
    return {
        "timestamp": "t",
        "temperature": temperature,
        "battery_percentage": 99.0,
        "battery_current": 2.0,
        "angular_velocity": 0.0,
        "signal_strength": 95.0,
        "packet_loss": 0.01,
    }


history = [make_state(25.0 + i * 0.5) for i in range(10)]
anomalies = [{"subsystem": "thermal", "severity": "medium",
              "reason": "Temperature rising too fast"}]

prompt = mentor._build_prompt("Why is it hot?", history[-1], anomalies, history)

assert "temperature: rising from 25.00 C to 29.50 C" in prompt
assert "battery_current: steady" in prompt
print("Prompt includes the trend lines")

no_history = mentor._build_prompt("Why is it hot?", history[-1], anomalies, None)
assert "No history available." in no_history
print("Prompt works without history")

print("\nAll prompt tests passed.")
