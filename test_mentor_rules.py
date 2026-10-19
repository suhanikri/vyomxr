from mentor.ai_mentor import AIMentor

mentor = AIMentor()
state = {"temperature": 30.0, "battery_current": 2.0}
prompt = mentor._build_prompt("Why is it hot?", state, [], None)

assert "rules that reading OUT as a cause" in prompt
assert "helps rule it out" in prompt
assert "ruling out suspects" in prompt
assert "assumes a steady reading changed" in prompt
print("Prompt contains the rule-out guidance")
