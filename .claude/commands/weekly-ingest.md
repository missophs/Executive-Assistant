---
description: Sweep the past week's email and Drive for anything not yet in the vault, propose it, wait for approval
allowed-tools: Read, Write, Edit, Glob, Bash
---

# /weekly-ingest — Catch what the daily sweeps missed

Unlike `/sync` and `/wrap-up`, this looks back 7 days instead of 1, and it never writes to the vault on its own — it proposes, Melissa approves, then it writes.

## Steps

1. **Read** `Task Board.md`, `Applications.md`, `Memory.md` for current state — so proposals don't duplicate what's already filed.
2. **Scan the past 7 days**:
   - Gmail: sent and received mail relevant to the job search or admin tasks that never got filed (check subject/thread content against what's already in Applications.md/Task Board.md).
   - Google Drive: any new or modified files in the past week not already referenced in the vault.
3. **Build a proposal list** — one line per item: what it is, where it would go (Task Board / Applications / Memory), and a one-sentence why. Do not write anything yet.
4. **Present the list** and stop. Wait for Melissa's explicit yes — either "apply all", a list of which numbers to apply, or "none."
5. **Only after approval**, make the edits, commit, and push (same push method as the daily routines: `gh api`, never raw `git push` in the cloud environment; regular `git push` is fine when run locally).

## Rules

- Never invent an item. If a thread is ambiguous, list it as "unclear — needs your read" rather than guessing where it goes.
- Never auto-apply, even if the proposal looks obviously correct.
- Skip anything the daily Standup/Midday/Wrap-up routines would already have caught (same-day captures) — this command is for the week's cracks, not a re-run of today.
