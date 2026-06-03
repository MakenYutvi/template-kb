Role

You are helping run a weekly maintenance review for a personal knowledge base.

Input

- Repository path or current workspace.
- Optional focus area: personal, work, projects, decisions, sources.

Output

Create a short weekly review report and update wiki only if durable context changed.

Process

1. Read `AGENTS.md`, `README.md`, `wiki/index.md`, `wiki/current-status.md`, `wiki/log.md` and `indexes/map.md`.
2. Review recent Git changes and recent `wiki/log.md` entries.
3. Identify:
   - open questions;
   - stale next actions;
   - source areas without wiki summaries;
   - wiki pages that may need compaction;
   - decisions that should be documented;
   - missing index or manifest updates.
4. Run available checks:
   - `scripts/kb_doctor.cmd` on Windows, if available;
   - `scripts/wiki_lint.cmd` on Windows, if available;
   - Python equivalents on macOS/Linux.
5. Recommend no more than 5 next actions.
6. If the review itself creates durable context, update `wiki/current-status.md` and `wiki/log.md`.

Output format

1. Current state.
2. Findings.
3. Top 5 next actions.
4. Suggested writeback.
5. Checks run.
6. Confidence and limits.

Rules

- Do not read all of `raw/` without a clear reason.
- Do not summarize sensitive details into broad wiki pages.
- Mark uncertain claims as hypotheses.
