"""Unified LLM client. Backends, in priority order:

1. ``codex``         — Codex CLI (`codex exec`). Free, real-time, no key.
2. ``claude_session``— claude.ai session-key (``CLAUDE_SESSION_KEY``). Free.
3. ``gemini``        — Gemini API (``GEMINI_API_KEY``). Paid/free tier.
4. ``anthropic``     — Anthropic API (``ANTHROPIC_API_KEY``). Paid.

Override priority via ``LLM_WIKI_BACKEND={codex|claude_session|gemini|anthropic}``.
"""
from __future__ import annotations

import json
import logging
import os
import re
import shutil
import subprocess
import uuid
from typing import Any

import httpx
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

from .config import ENV

logger = logging.getLogger(__name__)


class LLMError(RuntimeError):
    pass


def _detect_backend() -> str:
    forced = os.getenv("LLM_WIKI_BACKEND")
    if forced:
        return forced
    if shutil.which("codex"):
        return "codex"
    if ENV.claude_session_key:
        return "claude_session"
    if ENV.gemini_api_key:
        return "gemini"
    if ENV.anthropic_api_key:
        return "anthropic"
    raise LLMError(
        "No LLM backend available. Install `codex` CLI, set CLAUDE_SESSION_KEY, "
        "or set GEMINI_API_KEY / ANTHROPIC_API_KEY."
    )


class LLMClient:
    """Single entry point. Picks first available backend in priority order."""

    def __init__(self) -> None:
        self.backend = _detect_backend()
        self.model = ""
        if self.backend == "codex":
            self._codex_path = shutil.which("codex")
            self.model = "codex (CLI)"
        elif self.backend == "claude_session":
            if not ENV.claude_session_key:
                raise LLMError("CLAUDE_SESSION_KEY not set.")
            self._claude = _ClaudeSessionBackend(ENV.claude_session_key)
            self.model = "claude.ai (session)"
        elif self.backend == "gemini":
            from google import genai

            self._gemini = genai.Client(api_key=ENV.gemini_api_key)
            self.model = "gemini-2.5-flash"
        elif self.backend == "anthropic":
            import anthropic

            self._anthropic = anthropic.Anthropic(api_key=ENV.anthropic_api_key)
            self.model = "claude-haiku-4-5-20251001"
        else:
            raise LLMError(f"Unknown backend: {self.backend}")
        logger.info("LLMClient backend=%s model=%s", self.backend, self.model)

    @retry(
        wait=wait_exponential(multiplier=1, min=2, max=30),
        stop=stop_after_attempt(3),
        retry=retry_if_exception_type(Exception),
        reraise=True,
    )
    def text(self, prompt: str, *, system: str | None = None, max_tokens: int = 1024) -> str:
        if self.backend == "codex":
            return _codex_exec(self._codex_path, prompt, system=system)
        if self.backend == "claude_session":
            return self._claude.complete(prompt, system=system)
        if self.backend == "gemini":
            full = f"{system}\n\n{prompt}" if system else prompt
            resp = self._gemini.models.generate_content(model=self.model, contents=full)
            return (resp.text or "").strip()
        # anthropic
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
        instruction = "Respond with ONLY valid JSON. No prose, no markdown fences."
        full_system = f"{system}\n{instruction}" if system else instruction
        raw = self.text(prompt, system=full_system, max_tokens=max_tokens)
        return _extract_json(raw)


# --- Codex CLI backend ---------------------------------------------------


def _codex_exec(codex_path: str | None, prompt: str, *, system: str | None) -> str:
    """Run `codex exec` and parse out just the assistant response."""
    if not codex_path:
        raise LLMError("codex CLI not found")
    full = f"{system}\n\n{prompt}" if system else prompt
    try:
        proc = subprocess.run(  # noqa: S603
            [codex_path, "exec", "-"],
            input=full,
            capture_output=True,
            text=True,
            timeout=180,
            check=False,
        )
    except subprocess.TimeoutExpired as e:
        raise LLMError("codex exec timed out") from e
    if proc.returncode != 0:
        raise LLMError(f"codex exec exit={proc.returncode}: {proc.stderr[:300]}")
    return _extract_codex_response(proc.stdout)


_CODEX_TOKENS_USED = re.compile(r"^tokens used\s*$", re.MULTILINE)


def _extract_codex_response(stdout: str) -> str:
    """Codex emits header → 'codex\\nRESPONSE\\n...hooks...\\ntokens used\\nN\\nRESPONSE'.

    The text after the final 'tokens used\\n<count>' line is the clean answer.
    """
    m = _CODEX_TOKENS_USED.search(stdout)
    if m:
        tail = stdout[m.end() :].lstrip("\n")
        # Skip the token count line
        lines = tail.splitlines()
        if lines and lines[0].strip().replace(",", "").isdigit():
            tail = "\n".join(lines[1:])
        return tail.strip()
    # Fallback: take everything after the last "codex\n" header line
    parts = re.split(r"\n\s*codex\s*\n", stdout)
    if len(parts) > 1:
        # Strip the trailing hook chatter
        body = parts[-1]
        body = re.split(r"\n\s*hook:\s", body)[0]
        return body.strip()
    return stdout.strip()


# --- Claude session backend ----------------------------------------------


class _ClaudeSessionBackend:
    """Synchronous wrapper around Fleming-AI's claude.ai session-key flow."""

    BASE = "https://claude.ai/api"

    def __init__(self, session_key: str, timeout: float = 120.0) -> None:
        self._key = session_key
        self._timeout = timeout
        self._org_id: str | None = None

    def _headers(self) -> dict[str, str]:
        return {
            "Cookie": f"sessionKey={self._key}",
            "Content-Type": "application/json",
            "User-Agent": (
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
            ),
        }

    def _ensure_org(self, c: httpx.Client) -> str:
        if self._org_id:
            return self._org_id
        r = c.get(f"{self.BASE}/organizations", headers=self._headers(), timeout=self._timeout)
        if r.status_code == 401:
            raise LLMError("Invalid CLAUDE_SESSION_KEY (401).")
        r.raise_for_status()
        self._org_id = r.json()[0]["uuid"]
        return self._org_id

    def complete(self, prompt: str, *, system: str | None = None) -> str:
        with httpx.Client(timeout=self._timeout * 2) as c:
            org = self._ensure_org(c)
            conv_id = self._create_conversation(c, org)
            try:
                return self._send(c, org, conv_id, prompt, system=system)
            finally:
                try:
                    c.delete(
                        f"{self.BASE}/organizations/{org}/chat_conversations/{conv_id}",
                        headers=self._headers(),
                        timeout=self._timeout,
                    )
                except Exception as e:  # noqa: BLE001
                    logger.debug("conversation cleanup failed: %s", e)

    def _create_conversation(self, c: httpx.Client, org: str) -> str:
        payload = {"uuid": str(uuid.uuid4()), "name": "llm-wiki"}
        r = c.post(
            f"{self.BASE}/organizations/{org}/chat_conversations",
            headers=self._headers(), json=payload, timeout=self._timeout,
        )
        if r.status_code == 401:
            raise LLMError("Invalid CLAUDE_SESSION_KEY (401).")
        r.raise_for_status()
        return r.json()["uuid"]

    def _send(self, c: httpx.Client, org: str, conv_id: str, prompt: str,
              *, system: str | None = None) -> str:
        payload: dict[str, Any] = {"prompt": prompt, "attachments": []}
        if system:
            payload["system"] = system
        r = c.post(
            f"{self.BASE}/organizations/{org}/chat_conversations/{conv_id}/completion",
            headers=self._headers(), json=payload, timeout=self._timeout * 2,
        )
        if r.status_code == 401:
            raise LLMError("Invalid CLAUDE_SESSION_KEY (401).")
        r.raise_for_status()
        out = []
        for line in r.text.splitlines():
            if line.startswith("data: "):
                try:
                    data = json.loads(line[6:])
                except json.JSONDecodeError:
                    continue
                if "completion" in data:
                    out.append(data["completion"])
        return "".join(out).strip()


# --- JSON extraction -----------------------------------------------------


_FENCE_RE = re.compile(r"```(?:json)?\s*(.*?)```", re.DOTALL)


def _extract_json(text: str) -> Any:
    text = text.strip()
    m = _FENCE_RE.search(text)
    if m:
        text = m.group(1).strip()
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
