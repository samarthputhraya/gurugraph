# GuruGraph

Five collaborating AI agents share one Knowledge-Gap Graph. They find each student's misconceptions in minutes, from a tap or a photo of handwritten working. They write each student a micro-lesson in English, Hindi or Kannada, and hand the teacher a five-minute plan for the next class.

Built for ARGONYX '26 (RV University), Problem Statement 1, with Problem Statement 2 inside it.

## What is in this repository, and when it was made

The hackathon rules require the solution to be built or substantially refined during the event. This repository is public from day one, so the commit history shows exactly what existed before the event.

| Prepared before the event (public, dated commits) | Built on-site at ARGONYX '26 |
|---|---|
| `data/`: topic pack (8 concepts, 40 questions validated by exact arithmetic), 30 synthetic students, 50 labelled typed answers | Every product API endpoint and the database model |
| `oss/multi_agent_teaching_ecosystem/`: the open-source agent core (CLI only, no web server or UI), also contributed to [awesome-ai-apps](https://github.com/Arindam200/awesome-ai-apps) | The teacher dashboard, live knowledge graph, heatmap and activity feed |
| `design/` (outside this repo): tokens and mockups used on the Round 1 slides | The student phone flow: join, quiz, camera capture, lesson, retry |
| `landing/`: the static project website | Photo diagnosis in the app, gap-closure meter, parent messages, caching and demo mode |
| `frontend/`, `backend/`: empty shells (config, fonts, `/health`) | Deployment, evaluation run and numbers, demo video |

## Layout

```
gurugraph/
├── data/                 seed data and the generator that validates it (python data/tools/build_seed.py)
├── oss/
│   ├── multi_agent_teaching_ecosystem/   the agent core (LangGraph + Gemini, offline tests)
│   ├── docs_fix_pr/      patched files for the sponsor-repo docs PR
│   └── PR_KIT.md         issue and PR text for both open-source contributions
├── backend/              FastAPI shell (health check only)
├── frontend/             Next.js 16 + Tailwind 4 shell (tokens and fonts only)
└── landing/              static website with Raah analytics
```

## Run what exists today

```bash
cd oss/multi_agent_teaching_ecosystem
pip install -r requirements.txt
python main.py --offline          # watch the five agents work on a simulated class of 30
pytest -q                         # 22 offline tests

cd ../../backend && pip install -r requirements.txt && uvicorn app.main:app --reload   # GET /health
cd ../frontend && npm install && npm run dev                                            # shell only
```
