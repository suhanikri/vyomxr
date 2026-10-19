# VyomXR - Development Log

What was built, in order, and the problems solved along the way.
Dates are taken from file timestamps and terminal output.

## Phase 0 - Project setup (23 Sep 2026)

Built:
- Project folder, Python virtual environment (.venv), .gitignore, README.md, requirements.txt.
- Git repository, GitHub repository created with the GitHub CLI (gh), first push.

Problems and fixes:
- Two commands pasted into PowerShell ran together on one line, giving "error: no action specified". One of the garbled commands still committed successfully. Fix: run one command at a time and check output after each.
- gh was not recognized right after winget installed it. Windows had not refreshed PATH. Fix: restart the computer.

## Phase 1 - Spacecraft simulator (23-24 Sep)

Built:
- PowerSubsystem, ThermalSubsystem, AttitudeSubsystem, CommunicationSubsystem.
- Spacecraft class combining all four into one state dictionary with a timestamp.
- SimulationLoop: runs the spacecraft in a background thread at a fixed tick rate.
- A small test script for each part.

Problems and fixes:
- A test file was created in the wrong folder, so python could not find it. Fix: confirm the current folder with pwd before creating files.
- The first power test forced the battery from 99 to 15 percent in one tick, which gave an unrealistic -84.9 percent per tick alert. Fix: added set_anomaly() to the power subsystem so all four subsystems fail gradually and the same way.

## Phase 2 - Telemetry (24 Sep)

Built:
- TelemetryLogger writing JSON Lines, and reading them back.
- SimulationLoop logs every tick.
- A demo proving a mid-run fault appears in the log, and a matplotlib temperature chart.
- Log and chart files added to .gitignore.

Problems and fixes:
- The chart image would not open inside VS Code but the file was valid (29 KB). It opened with the Windows viewer. Treated as a one-off preview glitch.

## Phase 3 - Anomaly detection (24 Sep)

Built:
- AnomalyDetector with threshold and rate-of-change checks for all four subsystems.
- Severity levels: high for a limit breach, medium for a worrying trend.
- Live detection inside SimulationLoop with an on_anomaly callback.

Validated against:
- A thermal-only log, a log with all four faults at once, and a live run.

Notes:
- The detector flagged the fault on the first tick where the rate limit was exceeded, matching when the fault was injected.
- Emoji printed as ?? in PowerShell. Display issue only.

## Phase 4 - Mission dashboard (24-25 Sep)

Built:
- FastAPI backend: /spacecraft/state, /spacecraft/anomalies, /telemetry/history.
- Next.js, TypeScript and Tailwind frontend polling every 2 seconds.
- Anomaly panel (green when nominal, yellow or red alerts otherwise).
- Temporary test endpoints to trigger and clear faults.

Problems and fixes:
- create-next-app downloaded its compiler (SWC) and the download timed out. Fix: npm install @next/swc-win32-x64-msvc, then npm run dev worked.
- The recommended defaults created the app in frontend\app, not frontend\src\app, so writing page.tsx failed with "Could not find a part of the path". Fix: check the real path with Test-Path.
- The browser blocked frontend-to-backend requests. Fix: CORS middleware allowing http://localhost:3000.
- Commands run from inside frontend\ resolved paths wrongly, and uvicorn failed with "No module named 'backend'". Fix: always run backend commands from the project root.
- Duplicate uvicorn processes (8 Python processes) from repeated restarts gave inconsistent data: the dashboard showed 24.98 C while the alert said 30.14 C. Fix: stop all Python processes, start one backend.
- A leftover next dev server held port 3000. Fix: stop it with taskkill, start one frontend.
- A React hydration warning appeared. The error text showed an attribute injected by a browser extension (data-qb-installed), so it was treated as harmless.
- Frontend and backend stopping silently whenever a terminal was closed or reused. Fix: one terminal per server and do not reuse them.

## Phase 5 - AI Mentor (27 Sep, 18-19 Oct)

Built:
- Gemini connection with the key in .env, and a test script.
- AIMentor grounded in current state and active anomalies, exposed as POST /mentor/ask, with a chat box on the dashboard.
- Retry with backoff and a friendly fallback message.
- Hint and guiding-question answer format, plain text.
- mentor/trends.py: exact trend summaries from recent readings.
- SimulationLoop keeps the last 60 readings in memory.
- Prompt rule: steady readings rule a suspect out.
- Tests: test_trends.py, test_history.py, test_mentor_prompt.py, test_mentor_rules.py.

Problems and fixes:
- gemini-2.5-flash returned 404 "no longer available to new users". Fix: switched to gemini-3.8-flash.
- Gemini returned 503 "high demand". Retrying a moment later worked.
- UnicodeDecodeError (byte 0x97) when importing ai_mentor.py. An em dash in the prompt text was saved in a Windows encoding. Fix: plain ASCII text and -Encoding utf8 when writing files from PowerShell.
- The chat box stayed silent when Gemini failed, because the backend returned a 500 error. Fix: retry on 429, 500, 503 and 504, and return a readable message if all attempts fail.
- Early answers were honest but gave the student nothing to do next. Fix: a four-part prompt format with a hint and a guiding question.
- With history added, one answer asked "if current is steady, could increased electrical load be the cause?", which contradicts itself. The simulator does not link power to temperature, so this sends a student to a dead end. Fix: a prompt rule to treat steady readings as evidence that rules a cause out. Two repeat runs followed the rule.
- A test run left the thermal fault on unattended and the temperature climbed above 59 C. Confirms the missing temperature ceiling (see DECISIONS.md).

## Working practices that paid off

- Run one command at a time and read the actual output.
- Check the current folder (pwd) before creating or running anything.
- Use only plain ASCII when writing files from PowerShell, with -Encoding utf8.
- Commit and push after every working step.
- Write a small test before building on a component.
- Keep exactly one backend and one frontend process running.

## Next

- Student recovery actions (the decision step of the learning loop) with a safety check.
- Live telemetry chart on the dashboard.
- Phase 6: RAG with a small curated aerospace knowledge base.
- Couple subsystems in the simulator, and add a thermal ceiling.
