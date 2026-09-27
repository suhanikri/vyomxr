import os
from dotenv import load_dotenv
from google import genai

load_dotenv()


class AIMentor:
    """An AI Mentor that explains spacecraft telemetry and anomalies to students,
    grounded in real simulation data (never inventing spacecraft state)."""

    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        self.client = genai.Client(api_key=api_key)
        self.model = "gemini-3.8-flash"

    def _build_prompt(self, question, state, anomalies):
        """Construct a prompt that grounds Gemini in the real spacecraft data."""

        anomaly_text = "None currently detected."
        if anomalies:
            lines = [f"- [{a['subsystem']}/{a['severity']}] {a['reason']}" for a in anomalies]
            anomaly_text = "\n".join(lines)

        prompt = f"""You are an AI Mentor inside VyomXR, an educational spacecraft
simulation platform for engineering students. Your role is to explain telemetry,
aerospace concepts, and anomalies clearly. You do NOT control the spacecraft,
and you must NOT invent any spacecraft data beyond what is given below.

Current spacecraft telemetry:
{state}

Current detected anomalies:
{anomaly_text}

The student asks: "{question}"

Answer clearly and educationally, in 3-5 sentences. Base your answer only on
the telemetry and anomalies provided above. If something is not covered by
the data given, say so honestly instead of guessing."""

        return prompt

    def ask(self, question, state, anomalies=None):
        """Ask the AI Mentor a question, grounded in the current spacecraft state."""
        if anomalies is None:
            anomalies = []

        prompt = self._build_prompt(question, state, anomalies)

        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt,
        )

        return response.text
