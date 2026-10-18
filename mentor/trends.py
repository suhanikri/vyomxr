# Fields we summarize, and how much change counts as real (not sensor noise).
FIELD_UNITS = {
    "temperature": " C",
    "battery_percentage": " %",
    "battery_current": " A",
    "angular_velocity": "",
    "signal_strength": " %",
    "packet_loss": "",
}

NOISE_TOLERANCE = {
    "temperature": 0.5,
    "battery_percentage": 2.0,
    "battery_current": 0.3,
    "angular_velocity": 0.05,
    "signal_strength": 5.0,
    "packet_loss": 0.05,
}


def _describe_field(field, values):
    """Describe how one reading changed across the history window."""
    first, last = values[0], values[-1]
    change = last - first
    unit = FIELD_UNITS.get(field, "")
    tolerance = NOISE_TOLERANCE.get(field, 0.0)

    if abs(change) <= tolerance:
        average = sum(values) / len(values)
        return (
            f"- {field}: steady around {average:.2f}{unit} "
            f"(range {min(values):.2f} to {max(values):.2f})"
        )

    direction = "rising" if change > 0 else "falling"
    return (
        f"- {field}: {direction} from {first:.2f}{unit} "
        f"to {last:.2f}{unit} ({change:+.2f}{unit})"
    )


def summarize_trends(states, min_points=3):
    """Turn recent telemetry readings (oldest first) into short plain-text
    trend lines. All numbers come straight from the data."""
    if len(states) < min_points:
        return "Not enough history yet to describe trends."

    ticks = len(states) - 1
    lines = [f"Trend over the last {ticks} ticks (oldest to newest):"]

    for field in FIELD_UNITS:
        values = [s[field] for s in states if field in s]
        if len(values) < min_points:
            continue
        lines.append(_describe_field(field, values))

    return "\n".join(lines)
