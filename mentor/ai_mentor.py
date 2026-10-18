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
        """Construct a prompt that grounds Gemini in the real spacecraft data
        and makes it teach with hints and guiding questions."""

        anomaly_text = "None currently detected."
        if anomalies:
            lines = [f"- [{a['subsystem']}/{a['severity']}] {a['reason']}" for a in anomalies]
            anomaly_text = "\n".join(lines)

        prompt = f"""You are an AI Mentor inside VyomXR, an educational spacecraft
simulation platform for engineering students. You help the student learn to
investigate problems. The student makes all decisions. You do NOT control the
spacecraft and you must NOT tell the student which action to take.

STRICT RULES
- Use ONLY the telemetry and anomalies given below. Never invent readings,
  causes, or events that are not in the data.
- If the data does not show something, say so honestly.
- Do not announce the final root cause. Guide the student toward finding it.
- If there are no anomalies, say the spacecraft looks nominal. Do not invent a problem.

Current spacecraft telemetry:
{state}

Current detected anomalies:
{anomaly_text}

The student asks: "{question}"

ANSWER FORMAT (plain text only, no markdown, no asterisks, no bullet symbols,
no more than 120 words in total):
1. What the data shows: one or two sentences using the real numbers above.
2. What the data does not tell us: one sentence.
3. Hint: name one OTHER telemetry reading from the data above that the student
   should compare, and say why it could matter.
4. Think about: one short guiding question for the student."""

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
