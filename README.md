# VyomXR

AI-native experiential aerospace learning and simulation platform, designed initially for Indian higher education.

VyomXR is an **educational simulation**, not a professional spacecraft-control system. Core principle: **AI assists, the human student decides.**

## Current Status

| Phase | Description | Status |
|-------|-------------|--------|
| 0 | Project setup | Done |
| 1 | Spacecraft simulator (power, thermal, attitude, communication) | Done |
| 2 | Telemetry logging and visualization | Done |
| 3 | Anomaly detection (threshold + rate-of-change) | Done |
| 4 | Mission dashboard (FastAPI + Next.js) | Done |
| 5 | AI Mentor (Gemini, grounded in live telemetry) | In progress |
| 6+ | RAG, agents, adaptive learning, XR, research study | Planned |

## Architecture

```text
Spacecraft Simulator (source of truth)
        |
Simulation Loop (background thread)
        |
Telemetry Logger  +  Anomaly Detector
        |
FastAPI Backend
        |
Next.js Dashboard  +  AI Mentor (Gemini)
```

The simulator is the single source of truth. The AI Mentor only reasons over real simulation state and must not invent spacecraft data.

## Tech Stack

- Backend: Python, FastAPI, Uvicorn
- Frontend: Next.js, React, TypeScript, Tailwind CSS
- AI: Google Gemini API (google-genai)
- Visualization: matplotlib (offline charts)
- Version control: Git + GitHub

## Project Structure

```text
vyomxr/
  simulator/    power, thermal, attitude, communication, spacecraft, simulation loop
  telemetry/    JSON Lines logger
  anomaly/      rule-based anomaly detector
  mentor/       AI Mentor (Gemini)
  backend/api/  FastAPI app
  frontend/     Next.js dashboard
  test_*.py     small test scripts for each component
```

## Setup

### 1. Clone and create a virtual environment

```powershell
git clone https://github.com/suhanikri/vyomxr.git
cd vyomxr
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### 2. Add your Gemini API key

Create a file named `.env` in the project root with one line (no quotes, no spaces):

```text
GEMINI_API_KEY=your_key_here
```

The `.env` file is git-ignored. Never commit your key.

### 3. Install frontend dependencies

```powershell
cd frontend
npm install
cd ..
```

## Running the Project

Use two terminals, both started from the project root.

Terminal 1 (backend):

```powershell
uvicorn backend.api.main:app --reload
```

Terminal 2 (frontend):

```powershell
cd frontend
npm run dev
```

Then open http://localhost:3000

## API Endpoints

| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | /spacecraft/state | Current spacecraft telemetry |
| GET | /spacecraft/anomalies | Anomalies on the latest tick |
| GET | /telemetry/history?limit=50 | Recent telemetry readings |
| POST | /mentor/ask | Ask the AI Mentor (grounded in live state) |
| POST | /test/trigger-anomaly/{subsystem} | Dev tool: inject a fault |
| POST | /test/clear-anomaly/{subsystem} | Dev tool: clear a fault |

Subsystems: thermal, power, attitude, communication.

## Anomaly Detection

Phase 1 approach (rule-based):
- Threshold checks (for example temperature above 30 C)
- Rate-of-change checks (for example temperature rising faster than 0.3 C per tick)

Statistical and ML methods (Isolation Forest, etc.) are planned for later phases, only if the data justifies them.

## Testing

Each component has a small script in the project root, for example:

```powershell
python test_spacecraft.py
python test_full_anomaly_detector.py
python test_ai_mentor.py
```

## Known Issues

- The simulator has no recovery or upper limit on thermal anomalies yet.
- Gemini free tier can return temporary 503 errors during high demand. Retry after a moment.
- Dev-mode hydration warnings may appear if a browser extension modifies the page. These are harmless.

## Roadmap

1. Finish the AI Mentor chat interface on the dashboard
2. RAG with a small curated aerospace knowledge base
3. Agents, introduced one at a time (Diagnostic, Mission Planning, Safety, Evaluation, Scenario)
4. Student model and rule-based adaptive scenarios
5. XR prototype
6. Research experiment and paper

## Research Question

Can an adaptive agentic-AI-assisted aerospace simulation environment improve students' conceptual understanding and scenario-based problem-solving compared with conventional or non-adaptive learning approaches?

No experimental results exist yet. This project does not claim to invent AI agents, satellite simulation, XR education, anomaly detection, or RAG. The contribution under study is their integration into an adaptive, human-in-the-loop learning framework.

## Disclaimer

VyomXR is an educational simulation only. It must never be used to control a real spacecraft.
