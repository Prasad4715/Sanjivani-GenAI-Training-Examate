
"""Google Gemini provider wrapper for ChalanCheck."""

import os

from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

DEFAULT_SYSTEM_PROMPT = """
You are ChalanCheck, an assistant that explains Indian traffic challans
in simple and clear language.

Explain the offence, applicable section, fine, and additional action
only when supported by reliable legal information.

Do not invent fine amounts, legal sections, or punishments.
If information is missing or uncertain, clearly say so.
Distinguish maximum statutory fines from actual challan amounts.
Do not claim to know local police station hours or payment availability.
"""


class LLMProvider:
    """Reusable wrapper for generating responses with Gemini."""

    def __init__(self):
        provider = os.getenv("LLM_PROVIDER", "gemini").lower()

        if provider != "gemini":
            raise ValueError(f"Unsupported LLM provider: {provider}")

        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key or api_key == "PASTE_YOUR_ACTUAL_API_KEY_HERE":
            raise ValueError("GEMINI_API_KEY is missing or not configured.")

        self.model = os.getenv("GEMINI_MODEL", "gemini-3.5-flash-lite")
        self.client = genai.Client(api_key=api_key)

    def generate(self, question: str, system_prompt: str = DEFAULT_SYSTEM_PROMPT) -> str:
        """Send a question to Gemini and return the generated text."""

        if not question.strip():
            raise ValueError("Question cannot be empty.")

        response = self.client.models.generate_content(
            model=self.model,
            contents=question,
            config=types.GenerateContentConfig(
                system_instruction=system_prompt,
                temperature=0.2,
            ),
        )

        if not response.text:
            raise RuntimeError("Gemini returned an empty response.")

        return response.text.strip()
