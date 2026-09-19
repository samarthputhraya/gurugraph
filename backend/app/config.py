"""Settings from the environment. Everything the live demo depends on is switchable here."""

from __future__ import annotations

import os
from dataclasses import dataclass, field


@dataclass(frozen=True)
class Settings:
    llm_provider: str = field(default_factory=lambda: os.getenv("LLM_PROVIDER", "gemini"))   # gemini | openai_compat | offline
    gemini_keys: tuple[str, ...] = field(
        default_factory=lambda: tuple(k.strip() for k in os.getenv("GEMINI_API_KEYS", "").split(",") if k.strip()))
    demo_mode: str = field(default_factory=lambda: os.getenv("DEMO_MODE", "live"))            # live | cached
    database_url: str = field(default_factory=lambda: os.getenv("DATABASE_URL", "sqlite:///./gurugraph.db"))
    cors_origins: tuple[str, ...] = field(
        default_factory=lambda: tuple(o.strip() for o in os.getenv("CORS_ORIGINS", "http://localhost:3000").split(",")))
    llm_timeout_s: float = field(default_factory=lambda: float(os.getenv("LLM_TIMEOUT_S", "8")))


settings = Settings()
