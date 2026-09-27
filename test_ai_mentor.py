from simulator.spacecraft import Spacecraft
from anomaly.detector import AnomalyDetector
from mentor.ai_mentor import AIMentor

craft = Spacecraft()
detector = AnomalyDetector()
mentor = AIMentor()

# Simulate a few normal ticks first
for _ in range(3):
    craft.update()
    detector.check(craft.get_state())

# Now trigger a thermal anomaly and let it develop
craft.thermal.set_anomaly(True)
for _ in range(4):
    craft.update()

state = craft.get_state()
anomalies = detector.check(state)

print("--- Current spacecraft state ---")
print(state)
print("\n--- Detected anomalies ---")
print(anomalies)

print("\n--- Asking the AI Mentor ---")
question = "Why is the temperature increasing?"
answer = mentor.ask(question, state, anomalies)
print(f"\nStudent: {question}")
print(f"AI Mentor: {answer}")
