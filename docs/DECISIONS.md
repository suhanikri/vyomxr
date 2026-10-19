# VyomXR - Architecture Decisions

Each entry records what was decided, why, and what was rejected. Newest decisions go at the bottom.

## D1. The simulator is the single source of truth

- Decision: AI components reason over simulator state. They never invent spacecraft state.
- Why: Reliability and research validity. If the AI can make up readings, learning outcomes cannot be measured.
- Consequence: Every AI prompt is built from real data (current state, anomalies, trends).

## D2. Custom Python simulator, one class per subsystem

- Decision: PowerSubsystem, ThermalSubsystem, AttitudeSubsystem and CommunicationSubsystem, combined by a Spacecraft class.
- Why: Enough realism for teaching, and simple enough for a beginner to understand every line.
- Rejected: Professional orbital mechanics or an external simulator. Too complex for the MVP.
- Uniform interface: every subsystem has update(), get_state() and set_anomaly(True/False), so a future Scenario Agent can trigger any fault the same way.

## D3. Link status is derived, not stored

- Decision: CommunicationSubsystem computes link_status (nominal, degraded, lost) from signal strength and packet loss each time.
- Why: A stored label could drift out of sync with the numbers.

## D4. Telemetry stored as JSON Lines

- Decision: One JSON object per line in telemetry/*.log, appended over time.
- Why: Simple, human-readable, easy to read back, no database needed yet.
- Rejected: PostgreSQL now. The spec says to add it only when needed.
- Log and chart files are git-ignored because they are generated data.

## D5. Rule-based anomaly detection first

- Decision: Threshold checks plus rate-of-change checks for all four subsystems.
- Why: Explainable and testable. The spec says ML (Isolation Forest, etc.) only if the data justifies it.
- Severity: high for a hard limit breach, medium for a worrying trend.
- Rejected: Deep learning or ML now. There is no real data to train on.

## D6. The loop reports anomalies through a callback

- Decision: SimulationLoop takes an optional on_anomaly function and calls it when anomalies are found.
- Why: The loop does not need to know what happens next (print, show on dashboard, tell the Mentor). New consumers plug in without changing the loop.

## D7. FastAPI backend and Next.js frontend, polling every 2 seconds

- Decision: The dashboard fetches state and anomalies every 2 seconds.
- Why: Simplest approach that works. Matches the stack in the spec.
- Rejected for now: WebSockets. Worth revisiting if polling feels slow.
- CORS only allows http://localhost:3000.

## D8. Temporary test endpoints for fault injection

- Decision: POST /test/trigger-anomaly/{subsystem} and /test/clear-anomaly/{subsystem}.
- Why: Lets us trigger a fault from the terminal while watching the dashboard.
- Status: Development tools. They must be removed or protected before any real student deployment, and replaced by the Scenario Agent.

## D9. Gemini via google-genai, key kept in .env

- Decision: The API key is read from a git-ignored .env file. It is never hard-coded.
- Model: gemini-3.8-flash. The original choice, gemini-2.5-flash, returned 404 ("no longer available to new users").
- Lesson: Model names change. Keep the name in one place (AIMentor.model).

## D10. Mentor grounding: state, anomalies and trends in the prompt

- Decision: The prompt contains the current state, active anomalies and a trend summary, with strict rules against inventing data.
- Why: Without the data the Mentor gives generic textbook answers.

## D11. Trends are computed by our code, not by the LLM

- Decision: mentor/trends.py calculates changes exactly. Gemini only receives and explains the finished summary.
- Why: Language models make arithmetic mistakes on long lists of numbers.
- Noise tolerance: each field has a threshold below which a change is reported as steady, so sensor wobble is not called a trend.

## D12. Recent history lives in memory, not in the log file

- Decision: SimulationLoop keeps the last 60 readings in a deque protected by a lock.
- Why: The log file keeps readings from every earlier server run, so reading it would mix old sessions into "recent".

## D13. The Mentor teaches instead of answering outright

- Decision: Fixed four-part plain-text answer: what the data shows, what it does not tell us, a hint, and a guiding question. Maximum about 130 words.
- Why: Matches the spec (hints and guiding questions) and the principle that the AI assists and the student decides.
- Rule-out reasoning: a steady reading is evidence that rules a suspect out. Found by testing: an earlier answer asked a self-contradicting question about a steady reading.
- Plain text only, because the chat box shows raw text and would display markdown symbols literally.

## D14. Retry with backoff, then a friendly message

- Decision: Retry on codes 429, 500, 503 and 504 with waits of 2 and 4 seconds. Other errors, such as a wrong model name, fail immediately.
- Why: Gemini overload is usually temporary. An earlier failure left the chat box silent.
- ask() never raises. After the last attempt it returns a readable message.

## Known limitations and open questions

- Thermal anomalies have no ceiling (temperature reached about 290 C in an unattended test).
- Subsystems are not coupled: power draw does not affect temperature, so the Mentor cannot teach cause and effect across subsystems yet. Couple them when designing the first real mission scenario.
- There is one global spacecraft shared by everyone. There are no student sessions.
- The anomaly panel shows only the latest tick's anomalies, with no history of past alerts.
- No recovery actions exist yet, so the decision step of the learning loop is still missing.
- The chat shows error messages as normal replies. A separate error flag would allow different styling.
