import os
import time
from dotenv import load_dotenv
from google import genai

load_dotenv()

BUSY_MESSAGE = (
    "The AI Mentor is busy right now. Please wait a few seconds "
    "and ask again. Your spacecraft data is still updating normally."
)
ERROR_MESSAGE = (
    "The AI Mentor could not answer this time. "
    "Please try again in a moment."
)


class AIMentor:
    """An AI Mentor that explains spacecraft telemetry and anomalies to students,
    grounded in real simulation data (never inventing spacecraft state)."""

    def __init__(self, max_attempts=3):
        api_key = os.getenv("GEMINI_API_KEY")
        self.client = genai.Client(api_key=api_key)
        self.model = "gemini-3.8-flash"
        self.max_attempts = max_attempts

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
        """Ask the AI Mentor a question, grounded in the current spacecraft state.
        Retries on temporary Gemini errors. Never raises: returns a friendly
        message if every attempt fails."""
        if anomalies is None:
            anomalies = []

        prompt = self._build_prompt(question, state, anomalies)

        for attempt in range(1, self.max_attempts + 1):
            try:
                response = self.client.models.generate_content(
                    model=self.model,
                    contents=prompt,
                )
                if response.text:
                    return response.text
                return ERROR_MESSAGE
            except Exception as e:
                code = getattr(e, "code", None)
                temporary = code in (429, 500, 503, 504)
                print(f"Mentor attempt {attempt} failed (code={code}): {e}")

                if not temporary:
                    return ERROR_MESSAGE
                if attempt == self.max_attempts:
                    return BUSY_MESSAGE
                time.sleep(2 * attempt)

        return ERROR_MESSAGE
