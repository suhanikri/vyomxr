from mentor.trends import summarize_trends


def make_state(temperature, current):
    return {
        "temperature": temperature,
        "battery_percentage": 99.0,
        "battery_current": current,
        "angular_velocity": 0.0,
        "signal_strength": 95.0,
        "packet_loss": 0.01,
    }


# Case 1: too little history
one_reading = [make_state(25.0, 2.0)]
text = summarize_trends(one_reading)
print("Case 1:", text)
assert "Not enough history" in text

# Case 2: everything steady (tiny wobble only)
steady = [make_state(25.0 + (i % 2) * 0.1, 2.0) for i in range(10)]
text = summarize_trends(steady)
print("\nCase 2: steady spacecraft")
print(text)
assert "temperature: steady" in text

# Case 3: temperature rising while battery current stays flat
rising = [make_state(25.0 + i * 0.5, 2.0) for i in range(10)]
text = summarize_trends(rising)
print("\nCase 3: temperature rising, current flat")
print(text)
assert "temperature: rising" in text
assert "battery_current: steady" in text

print("\nAll trend tests passed.")
