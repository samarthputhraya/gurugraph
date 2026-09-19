"""GuruGraph API. Pre-built scaffold: health check and wiring to the open-source agent core only.
Every product endpoint (sessions, join, answers, photos, dashboard, events, simulate, analyze) is built
on-site at ARGONYX '26; see ../README.md for the list and contracts."""

from __future__ import annotations

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from teaching_ecosystem.topic import load_topic

from .config import settings

load_dotenv()

app = FastAPI(title="GuruGraph API", version="0.1.0")
app.add_middleware(CORSMiddleware, allow_origins=list(settings.cors_origins), allow_methods=["*"], allow_headers=["*"])

TOPIC = load_topic()


@app.get("/health")
def health() -> dict:
    return {
        "ok": True,
        "llm_provider": settings.llm_provider,
        "gemini_keys": len(settings.gemini_keys),
        "demo_mode": settings.demo_mode,
        "topic": TOPIC.name,
        "concepts": len(TOPIC.concepts),
        "questions": len(TOPIC.questions),
    }
