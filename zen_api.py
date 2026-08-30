"""Minimal OpenCode Zen API call - Python (free tier, no auth needed)

Docs: https://opencode.ai/docs/zen
Models: https://opencode.ai/zen/v1/models
Free models work WITHOUT API key - just omit Authorization header.

Usage:
    from pay_day import ZenChatSession, ZenFreeModel
    from pay_day.zen_api import call_zen
    r = call_zen("Hello!")
    print(r.text)

    # same session with system prompt:
    s = ZenChatSession(system_prompt="You are a helpful assistant. Reply concisely.")
    s.ask("My name is Sonu")
    s.ask("What's my name?")  # remembers
    s.reset()  # new session (keeps system_prompt)
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any

import requests


class ZenFreeModel(str, Enum):
    """Free-tier Zen models (cost_usd=0, no API key required)"""

    MUSE_SPARK_1_2_CONTRIBUTOR_FREE = "muse-spark-1.2-contributor-free"
    DEEPSEEK_V4_FLASH_FREE = "deepseek-v4-flash-free"
    MIMO_V2_5_FREE = "mimo-v2.5-free"
    LING_3_FLASH_FIN_FREE = "ling-3.0-flash-fin-free"
    NEMOTRON_3_ULTRA_FREE = "nemotron-3-ultra-free"
    NEMOTRON_3_5_LIGHTNING_FREE = "nemotron-3.5-lightning-free"
    LAGUNA_S_2_1_FREE = "laguna-s-2.1-free"


@dataclass(frozen=True)
class ZenUsage:
    input_tokens: int
    output_tokens: int
    total_tokens: int
    reasoning_tokens: int | None = None
    cached_tokens: int | None = None


@dataclass(frozen=True)
class ZenResponse:
    """Typed return from Zen API"""

    text: str
    model: str
    status: str
    usage: ZenUsage | None
    cost: str | None
    raw: dict[str, Any]


def call_zen(
    prompt: str,
    *,
    model: ZenFreeModel | str = ZenFreeModel.MUSE_SPARK_1_2_CONTRIBUTOR_FREE,
    base_url: str = "https://opencode.ai/zen/v1",
    timeout: float = 60.0,
    extra_body: dict[str, Any] | None = None,
) -> ZenResponse:
    """One-off call (stateless)."""
    model_id = model.value if isinstance(model, Enum) else str(model)
    body: dict[str, Any] = {"model": model_id, "input": prompt}
    if extra_body:
        body.update(extra_body)

    resp = requests.post(f"{base_url.rstrip('/')}/responses", json=body, timeout=timeout)
    resp.raise_for_status()
    data: dict[str, Any] = resp.json()

    text = ""
    for item in data.get("output", []):
        if item.get("type") == "message":
            for c in item.get("content", []):
                if c.get("type") == "output_text":
                    text += c.get("text", "")

    usage_raw = data.get("usage") or {}
    usage = None
    if usage_raw:
        usage = ZenUsage(
            input_tokens=usage_raw.get("input_tokens", 0),
            output_tokens=usage_raw.get("output_tokens", 0),
            total_tokens=usage_raw.get("total_tokens", 0),
            reasoning_tokens=(usage_raw.get("output_tokens_details") or {}).get("reasoning_tokens"),
            cached_tokens=(usage_raw.get("input_tokens_details") or {}).get("cached_tokens"),
        )

    return ZenResponse(
        text=text,
        model=data.get("model", model_id),
        status=data.get("status", "unknown"),
        usage=usage,
        cost=data.get("cost"),
        raw=data,
    )


@dataclass
class ZenChatSession:
    """handle chat: reuse same instance to continue, .reset() for new session."""

    model: ZenFreeModel | str = ZenFreeModel.MUSE_SPARK_1_2_CONTRIBUTOR_FREE
    system_prompt: str | None = None
    base_url: str = "https://opencode.ai/zen/v1"
    timeout: float = 60.0
    history: list[ZenResponse] = field(default_factory=list)
    _user_prompts: list[str] = field(default_factory=list, repr=False)

    def ask(self, prompt: str, *, extra_body: dict[str, Any] | None = None) -> ZenResponse:
        """Continue same session - builds history into input (Zen is stateless)."""
        if self.history:
            parts: list[str] = []
            if self.system_prompt:
                parts.append(f"system: {self.system_prompt}")
            parts.extend(f"user: {u}\nassistant: {a.text}" for u, a in zip(self._user_prompts, self.history))
            parts.append(f"user: {prompt}")
            full_prompt = "\n\n".join(parts)
        else:
            full_prompt = f"system: {self.system_prompt}\n\nuser: {prompt}" if self.system_prompt else prompt

        r = call_zen(prompt=full_prompt, model=self.model, base_url=self.base_url, timeout=self.timeout, extra_body=extra_body)
        self._user_prompts.append(prompt)
        self.history.append(r)
        return r

    def reset(self) -> None:
        """Start new session (clear history, keep system_prompt)."""
        self.history.clear()
        self._user_prompts.clear()
