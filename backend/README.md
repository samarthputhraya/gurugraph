# GuruGraph API: on-site build list

This folder ships only a health check and the wiring to the agent core. Build everything below on-site, in this order. Contracts and rules are in `BUILD_SPEC.md` at the project root.

```bash
pip install -r requirements.txt        # installs the agent core from ../oss in editable mode
cp .env.example .env                   # add GEMINI_API_KEYS (one per teammate, comma separated)
uvicorn app.main:app --reload --workers 1
```

## Build order (tick as you go)

Hours 0 to 3
- [ ] SQLModel tables: session, student, mastery, response, agent_event, recommendation, lesson_cache (SQLite with WAL and busy_timeout 5000)
- [ ] `POST /api/sessions` returns {session_id, code, join_url}
- [ ] `POST /api/sessions/{code}/join` takes {nickname, language} and returns {student_id}
- [ ] `GET /api/students/{id}/next` uses `examiner.next_question(kinds=("mcq","text"))`, with question 4 always a photo item. Shuffle MCQ options per student with a seeded RNG, because the bank lists the correct option first
- [ ] `POST /api/students/{id}/answer` calls `diagnostician.diagnose` then `apply_diagnosis`, and writes agent_event rows
- [ ] `POST /api/students/{id}/answer-photo` (multipart): resize to 1280 px, then `diagnose_photo`, with a typed-answer fallback
- [ ] `POST /api/sessions/{id}/simulate` runs `simulator.simulate_answer` for 30 personas in-process, with no LLM calls

Hours 3 to 6
- [ ] `GET /api/sessions/{id}/dashboard` returns `analyst.analyze` plus the heatmap and the graph as {nodes, edges}
- [ ] `GET /api/sessions/{id}/events?after=seq` (the dashboard polls every 2 seconds)
- [ ] `POST /api/sessions/{id}/analyze` runs coach.propose, then analyst.critique, then coach.revise if challenged, logging three feed events
- [ ] `POST /api/recommendations/{id}/approve`

Hours 6 to 9
- [ ] `GET /api/students/{id}/lesson` uses `curator.lesson` with the DB-backed cache and `retry_items`
- [ ] `POST /api/students/{id}/retry` checks the answers against the bank, then `close_gap`, then updates the gap-closure metric
- [ ] Parent message via `coach.parent_message`, returned with the recommendation
- [ ] `POST /api/sessions/{id}/load-pilot` loads `data/pilot_v1.csv`, the Google Forms export: one row per student, and the question id in brackets in each column header, for example `[Q16]`
- [ ] `GET /api/eval` reports text accuracy (LLM only) and photo accuracy
- [ ] `DEMO_MODE=cached`: serve every LLM output from cache; photos try live with a 6-second timeout, then fall back to a typed answer
- [ ] Key rotation across `GEMINI_API_KEYS`, an 8-second timeout, one retry

Rules that keep the demo alive: one uvicorn worker; never call the LLM inside a database transaction; synthetic students never call the LLM; the UI never waits on an LLM (return `generating` and poll).
