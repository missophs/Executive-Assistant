---
description: Audit the vault for contradictions, stale items, and quietly-forgotten decisions
allowed-tools: Read, Write, Edit, Glob, Bash, Artifact
---

# /drift-check — Find what's rotting

Report only. Never auto-fix, never edit the vault. The point is to surface what's gone stale or inconsistent so Melissa can decide what to do with it.

## Steps

1. **Read** `Task Board.md`, `Applications.md`, `Memory.md` in full.
2. **Check for contradictions** — the same fact stated two different ways in two places. Example: Task Board's "Waiting On" section says "(none open)" while Memory's Follow-Ups table has open rows — that's a contradiction, not a stale item.
3. **Check for stale backlog** — items in Task Board's Backlog sitting 10+ days with no movement (compare the date embedded in the item text to today). Group similar ones (e.g. "6 LinkedIn job-alert triage items untouched since early September") rather than listing each.
4. **Check for unresolved clarifications** — items phrased as a question to Melissa ("Tell Ellie...", "confirm...", "clarify...") that have sat 5+ days with no answer.
5. **Check for dropped security/urgent flags** — anything tagged `#security` or similarly flagged that's still sitting unresolved.
6. **Check for unresolved ambiguity Memory has already flagged** — Memory sometimes explicitly notes something as "unresolved" or "remains unresolved" (e.g. an unidentified calendar block). Surface these too — they're already known drift, not new.
7. **Do not** flag normal in-progress items (an interview awaiting outcome 1-2 days old is not drift).

## Output

A short report, worst-first:
```
## Drift Check — <date>

**Contradictions**
- ...

**Stale (10+ days, no movement)**
- ...

**Unanswered questions (5+ days)**
- ...

**Still-open flags**
- ...
```

If nothing qualifies in a section, omit the section header entirely — do not print "(none)".

Never invent a finding. If unsure whether something counts as drift, leave it out.
