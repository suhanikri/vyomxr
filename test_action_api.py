from fastapi.testclient import TestClient

from backend.api.main import app, craft

client = TestClient(app)

# 1. The action list
r = client.get("/spacecraft/actions")
assert r.status_code == 200
actions = r.json()["actions"]
ids = [a["id"] for a in actions]
assert "switch_to_backup_cooling" in ids
assert "reduce_payload_power" in ids
assert "reorient_toward_sun" in ids
labels = {a["id"]: a["label"] for a in actions}
assert labels["reduce_payload_power"] == "Reduce payload power"
print("1. Action list works, with readable labels")

# 2. No decisions yet
r = client.get("/spacecraft/decisions")
assert r.json() == {"decisions": []}
print("2. Decision list starts empty")

# 3. An unknown action is rejected through the API
r = client.post("/spacecraft/action", json={"action": "launch_fireworks"})
assert r.status_code == 200
body = r.json()
assert body["allowed"] is False
assert body["effect"] == "rejected"
print("3. Unknown action is rejected by the safety gate")

# 4. A bad request is refused before reaching the simulator
r = client.post("/spacecraft/action", json={})
assert r.status_code == 422
print("4. A request with no action is refused (422)")

# 5. The right fix during a fault
craft.thermal.set_anomaly(True)
for _ in range(4):
    craft.update()
r = client.post("/spacecraft/action", json={"action": "switch_to_backup_cooling"})
body = r.json()
assert body["effect"] == "resolved"
assert body["fault_active"] is True
assert body["ticks_since_fault"] == 3
print("5. Backup cooling during a fault: resolved, ticks_since_fault = 3")

# 6. Both decisions are on record, in order
r = client.get("/spacecraft/decisions")
decisions = r.json()["decisions"]
assert len(decisions) == 2
assert decisions[0]["effect"] == "rejected"
assert decisions[1]["effect"] == "resolved"
print("6. Decisions are listed in order")

print("\nAll action API tests passed.")
