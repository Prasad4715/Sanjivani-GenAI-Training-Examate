
"""Google Gemini provider wrapper for ChalanCheck."""

import logging
import os
import time

from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

logger = logging.getLogger("chalancheck.llm")

# Gemini 3.5 Flash-Lite standard paid-tier pricing (USD)
# Prices per 1 million tokens, based on the supplied pricing table.
INPUT_COST_PER_1M = 0.30
OUTPUT_COST_PER_1M = 2.50

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


def calculate_estimated_cost(
    input_tokens: int,
    output_tokens: int,
) -> float:
    """Estimate standard paid-tier token cost in USD."""
    input_cost = (
        input_tokens * INPUT_COST_PER_1M
    ) / 1_000_000

    output_cost = (
        output_tokens * OUTPUT_COST_PER_1M
    ) / 1_000_000

    return input_cost + output_cost


class LLMProvider:
    """Reusable wrapper for generating responses with Gemini."""

    def __init__(self):
        provider = os.getenv("LLM_PROVIDER", "gemini").lower()

        if provider != "gemini":
            raise ValueError(
                f"Unsupported LLM provider: {provider}"
            )

        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key or api_key == "PASTE_YOUR_ACTUAL_API_KEY_HERE":
            raise ValueError(
                "GEMINI_API_KEY is missing or not configured."
            )

        self.model = os.getenv(
            "GEMINI_MODEL",
            "gemini-3.5-flash-lite",
        )

        self.client = genai.Client(api_key=api_key)

    def generate(
        self,
        question: str,
        system_prompt: str = DEFAULT_SYSTEM_PROMPT,
    ) -> str:
        """Generate an answer and log token usage, cost, and latency."""

        if not question or not question.strip():
            raise ValueError("Question cannot be empty.")

        start_time = time.perf_counter()

        response = self.client.models.generate_content(
            model=self.model,
            contents=question,
            config=types.GenerateContentConfig(
                system_instruction=system_prompt,
                temperature=0.2,
            ),
        )

        latency_ms = (
            time.perf_counter() - start_time
        ) * 1000

        usage = response.usage_metadata

        input_tokens = (
            getattr(usage, "prompt_token_count", None)
            if usage is not None
            else None
        )

        output_tokens = (
            getattr(usage, "candidates_token_count", None)
            if usage is not None
            else None
        )

        thinking_tokens = (
            getattr(usage, "thoughts_token_count", None)
            if usage is not None
            else None
        )

        total_tokens = (
            getattr(usage, "total_token_count", None)
            if usage is not None
            else None
        )

        # Calculate cost only when usage data is available.
        estimated_cost = None

        if input_tokens is not None and output_tokens is not None:
            billable_output_tokens = (
                output_tokens + (thinking_tokens or 0)
            )

            estimated_cost = calculate_estimated_cost(
                input_tokens,
                billable_output_tokens,
            )

        logger.info(
            "Gemini request | model=%s | "
            "input_tokens=%s | "
            "output_tokens=%s | "
            "thinking_tokens=%s | "
            "total_tokens=%s | "
            "latency_ms=%.2f | "
            "estimated_cost_usd=%s",
            self.model,
            input_tokens,
            output_tokens,
            thinking_tokens,
            total_tokens,
            latency_ms,
            (
                f"{estimated_cost:.8f}"
                if estimated_cost is not None
                else "unavailable"
            ),
        )

        if not response.text:
            raise RuntimeError(
                "Gemini returned an empty response."
            )

        return response.text.strip()


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(levelname)s:%(name)s:%(message)s",
    )

    provider = LLMProvider()

    answer = provider.generate(
        "Explain Section 185 of the Motor Vehicles Act briefly."
    )

    print("\nGemini Answer:")
    print(answer)
