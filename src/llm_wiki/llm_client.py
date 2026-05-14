"""Unified LLM client. Gemini primary (free tier, real SDK); Anthropic fallback if key set.

Design: synchronous, batch-friendly, tenacious retries. Returns plain text or parsed JSON.
"""
from __future__ import annotations

import json
import logging
import re
from typing import Any

from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

from .config import ENV

logger = logging.getLogger(__name__)


class LLMError(RuntimeError):
    pass


class LLMClient:
    """Single entry point. Picks Gemini if available, else Anthropic."""

    def __init__(self) -> None:
        self.backend: str
        if ENV.gemini_api_key:
            from google import genai

            self._gemini = genai.Client(api_key=ENV.gemini_api_key)
            self.backend = "gemini"
            self.model = "gemini-2.5-flash"
        elif ENV.anthropic_api_key:
            import anthropic

            self._anthropic = anthropic.Anthropic(api_key=ENV.anthropic_api_key)
            self.backend = "anthropic"
            self.model = "claude-haiku-4-5-20251001"
        else:
            raise LLMError(
                "No LLM credentials. Set GEMINI_API_KEY or ANTHROPIC_API_KEY."
            )
        logger.info("LLMClient backend=%s model=%s", self.backend, self.model)

    @retry(
        wait=wait_exponential(multiplier=1, min=2, max=30),
        stop=stop_after_attempt(4),
        retry=retry_if_exception_type(Exception),
        reraise=True,
    )
    def text(self, prompt: str, *, system: str | None = None, max_tokens: int = 1024) -> str:
        if self.backend == "gemini":
            full = f"{system}\n\n{prompt}" if system else prompt
            resp = self._gemini.models.generate_content(model=self.model, contents=full)
            return (resp.text or "").strip()
        else:  # anthropic
            kwargs: dict[str, Any] = {
                "model": self.model,
                "max_tokens": max_tokens,
                "messages": [{"role": "user", "content": prompt}],
            }
            if system:
                kwargs["system"] = system
            resp = self._anthropic.messages.create(**kwargs)
            return resp.content[0].text.strip()

    def json(self, prompt: str, *, system: str | None = None, max_tokens: int = 2048) -> Any:
        """Ask for JSON; tolerate code-fenced output."""
        instruction = "Respond with ONLY valid JSON. No prose, no markdown fences."
        full_system = f"{system}\n{instruction}" if system else instruction
        raw = self.text(prompt, system=full_system, max_tokens=max_tokens)
        return _extract_json(raw)


_FENCE_RE = re.compile(r"```(?:json)?\s*(.*?)```", re.DOTALL)


def _extract_json(text: str) -> Any:
    text = text.strip()
    m = _FENCE_RE.search(text)
    if m:
        text = m.group(1).strip()
    # Greedy bracket extraction fallback
    if not text.startswith(("{", "[")):
        for opener, closer in (("{", "}"), ("[", "]")):
            i, j = text.find(opener), text.rfind(closer)
            if i != -1 and j != -1 and j > i:
                text = text[i : j + 1]
                break
    try:
        return json.loads(text)
    except json.JSONDecodeError as e:
        raise LLMError(f"Could not parse JSON from LLM output: {text[:200]!r}") from e
