# Open-source PR kit for awesome-ai-apps (Round 1: 15 points + 10 brownie points)

Everything below is ready to paste. Do the steps in order; each one is 5 to 15 minutes.

Sponsor repo: https://github.com/Arindam200/awesome-ai-apps. The CONTRIBUTING rules are to open an issue first, submit one project per PR, and link the PR with "Closes #N". CI runs `ruff check .` on Python 3.10 to 3.12, and two bots flag README-only PRs and new folders without a README.

---

## Step 0: brownie points (every member, tonight)

1. Open https://github.com/Arindam200/awesome-ai-apps while signed in and click **Star**.
2. Take a screenshot that shows your GitHub username (top right) and the "Starred" button.
3. Submit your GitHub username, the screenshot and the team name wherever the organizers collect it (Unstop form or their instructions).

Also click **Watch**, and follow Arindam200, Astrodevil and shivaylamba.

---

## Step 1: fork and clone (the member who owns the PRs)

```bash
# fork on GitHub first (Fork button), then:
git clone https://github.com/<your-username>/awesome-ai-apps.git
cd awesome-ai-apps
git remote add upstream https://github.com/Arindam200/awesome-ai-apps.git
```

---

## PR B first (smallest, fastest to merge): docs and template fixes

### Issue B (use "Question" or "Feature Request" template; title below)

**Title:** Docs: stale repo name in templates, outdated project count, incomplete category dropdowns

**Body:**

> A few repository docs have drifted from the current state of the repo:
>
> 1. `.github/README_TEMPLATE.md` and `.github/PULL_REQUEST_TEMPLATE.md` still point to the old repository name `awesome-llm-apps` (clone command, `cd` path, CONTRIBUTING and LICENSE links). GitHub redirects the links, but new contributors copy the `cd awesome-llm-apps/...` path from the template into their READMEs.
> 2. `CLAUDE.md` and `AGENTS.md` say the repository contains "70+ example projects"; the README now lists 132.
> 3. The "Project Directory" dropdown in the issue forms lists only some categories. `feature_request.yml` is missing `memory_agents`, `voice_agents`, `fine_tuning` and `course`; `bug_report.yml` is also missing `simple_ai_agents`. The `require-project-readme` workflow already recognises all nine category folders.
>
> I'd be happy to open a small PR that fixes all three.

### PR B

```bash
git checkout -b docs/fix-stale-repo-name-and-categories
# copy the six patched files from gurugraph/oss/docs_fix_pr/ over the same paths in the fork, or:
git apply ../path/to/gurugraph/oss/docs_fix_pr/docs_fix.diff
git add .github CLAUDE.md AGENTS.md
git commit -m "docs: fix stale repo name, project count and issue-form categories"
git push origin docs/fix-stale-repo-name-and-categories
```

**PR title:** docs: fix stale repo name, project count and issue-form categories

**PR body (fill the template):**

> ## 🔗 Linked Issue
> Closes #<issue B number>
>
> ## ✅ Type of Change
> - [x] 📚 Documentation Update
>
> ## 📝 Summary
> - Replace the old `awesome-llm-apps` name with `awesome-ai-apps` in the README and PR templates (clone command, `cd` path, CONTRIBUTING and LICENSE links).
> - Update the project count in `CLAUDE.md` and `AGENTS.md` from "70+" to "130+" to match the README.
> - Add the missing categories to the "Project Directory" dropdowns so they match the nine folders the `require-project-readme` workflow checks.
>
> No code changes. I checked each YAML dropdown keeps the same indentation and the forms still render.

The docs-only bot flags **link-only** README changes of 5 lines or fewer. This PR edits templates and YAML across 6 files, so it should not be flagged. If it is, reply politely and point to the issue.

---

## PR A: the new project

### Issue A (Feature Request template)

**Title:** [FEATURE] New project: Multi-Agent Teaching & Learning Ecosystem (LangGraph + Gemini)

- **Feature Description:** Add `advance_ai_agents/multi_agent_teaching_ecosystem`. Five LangGraph agents (Diagnostician, Examiner, Curator, Analyst, Coach) share a Knowledge-Gap Graph. They diagnose the misconception behind each wrong answer, including from a photo of handwritten working. They adapt the next question, write micro-lessons in English, Hindi or Kannada, and produce a 5-minute teaching plan. The Analyst challenges the Coach's plan with class data before the teacher sees it.
- **Target Project:** multi_agent_teaching_ecosystem
- **Project Directory:** advance_ai_agents
- **Motivation:** The collection has no education examples yet. This one shows patterns other agent projects can reuse. It uses rules first and an LLM only for the long tail. It includes a rule-backed critique loop with conditional LangGraph routing, vision with structured output, and an offline mode for tests.
- **Proposed Solution:** A LangGraph `StateGraph` of six nodes with a conditional edge after the critique. Gemini is used through `google-genai` with Pydantic response schemas. An OpenAI-compatible provider works for text. A deterministic offline model lets the demo and all tests run without keys.
- **User Impact:** A runnable reference for multi-agent workflows that must be explainable and cheap. A simulated class of 30 needs zero LLM calls.
- **Alternatives Considered:** A single-prompt tutor, which is harder to evaluate and explain, or CrewAI. LangGraph was chosen for explicit state and conditional routing.
- **Checklist:** tick all four.

### PR A

```bash
git checkout main && git pull upstream main
git checkout -b feat/multi-agent-teaching-ecosystem
cp -r ../path/to/gurugraph/oss/multi_agent_teaching_ecosystem advance_ai_agents/
# add one line to the root README.md, Advanced Agents list, directly after "Multi-Agent Coding Harness":
#   - [Multi-Agent Teaching & Learning Ecosystem](advance_ai_agents/multi_agent_teaching_ecosystem): Five LangGraph agents diagnose fraction misconceptions (including from photos of handwritten working), write multilingual micro-lessons and debate the teacher's plan
# and bump the counts: "_34 projects_" -> "_35 projects_" under Advanced Agents, "132 projects" -> "133 projects" at the top
pip install ruff pytest && ruff check . && (cd advance_ai_agents/multi_agent_teaching_ecosystem && pip install -r requirements.txt && pytest -q)
git add advance_ai_agents/multi_agent_teaching_ecosystem README.md
git commit -m "feat: add multi-agent teaching and learning ecosystem (LangGraph + Gemini)"
git push origin feat/multi-agent-teaching-ecosystem
```

**PR title:** feat: add multi-agent teaching & learning ecosystem (LangGraph + Gemini)

**PR body:**

> ## 🔗 Linked Issue
> Closes #<issue A number>
>
> ## ✅ Type of Change
> - [x] ✨ New Project/Feature
>
> ## 📝 Summary
> Adds `advance_ai_agents/multi_agent_teaching_ecosystem`: five LangGraph agents around a shared Knowledge-Gap Graph.
>
> - **Diagnostician**: MCQ answers are diagnosed from misconception-tagged distractors and typed answers with exact fraction arithmetic. Only unfamiliar answers go to the LLM. Photos of handwritten working go to Gemini vision, which returns the steps, the first wrong step and the tag.
> - **Examiner**: the lowest-mastery concept whose prerequisites are ready, at most 2 questions per concept.
> - **Curator**: cached micro-lessons in English, Hindi or Kannada with a script check. Gap-closing retry items always come from the verified bank.
> - **Analyst**: class aggregation, then a rule-backed critique of the Coach's plan. The LLM may rephrase a verdict but never flip it.
> - **Coach**: proposes, revises after a challenge (a conditional LangGraph edge), and drafts parent messages. Every LLM path has a template fallback.
>
> Runs fully offline with a deterministic stand-in model (`python main.py --offline`). Includes a 40-question topic pack validated by exact arithmetic, 30 synthetic students, 50 hand-labelled typed answers (`--eval`) and a photo-evaluation command (`--eval-photos`).
>
> ## 📖 README Checklist
> - [x] I have created a `README.md` file for my project.
> - [x] My `README.md` follows the official `.github/README_TEMPLATE.md`.
> - [x] I have included clear installation and usage instructions in my `README.md`.
> - [x] I have added a GIF or screenshot to the `assets` folder and included it in my `README.md`.
>
> ## ✔️ Contributor Checklist
> - [x] I have read the CONTRIBUTING.md document.
> - [x] My code follows the project's coding standards (`ruff check .` passes).
> - [x] I have placed my project in the correct directory (`advance_ai_agents`).
> - [x] I have included a `requirements.txt` and `pyproject.toml`.
> - [x] I have added a `.env.example` file and ensured no secrets are committed.
> - [x] My pull request is focused on a single project.
>
> ## 💬 Additional Comments
> 18 offline tests (`pytest`) cover the answer parser, mastery updates, each agent, LLM outages and the full graph. No API key is needed to review it.

---

## PR C: a real bug fix (optional, if time allows)

Tonight, two members each install and run two projects from `simple_ai_agents/` or `rag_apps/` on Python 3.12. For each real failure (import error, retired model name, stale pin), open an issue with the stack trace, then a PR with the smallest fix. Do not take issue #105 (job_finder_agent); it was claimed on 17 Sep.

---

## Etiquette that earns the "community" half of the points

- Reply to CodeRabbit and maintainer comments within hours, and push fixes as new commits.
- Never write "please merge for my hackathon". If asked, mention the hackathon as context.
- Help on one or two other open threads, for example by pointing a new contributor to the README template.
- Screenshot the issues, the PRs with green checks, and any maintainer reply for slide 5.
