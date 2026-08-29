---
description: Regenerate the visual dashboard from the vault and open it in the browser
allowed-tools: Read, Write, Edit, Glob, Bash
---

# /dashboard — Render the Command Center

Read the vault, regenerate `dashboard.html`, and open it.

## Steps

1. **Read the data.** `Task Board.md`, `Applications.md`, `Memory.md`, and the most recent file in `Daily Notes/`.
2. **Regenerate `dashboard.html`.** Keep the existing design exactly — only the data changes. Update the `DATA` object near the top of the `<script>` block; do not rewrite the CSS or the layout.

   `DATA` shape:
   ```js
   {
     generated: "2026-08-29",          // today
     today: [ {task, why, due} ],       // from Task Board "Today", max 3
     week: [ {task, due} ],             // from Task Board "This Week"
     pipeline: [ {company, role, stage, applied, lastContact, nextAction} ],
     waiting: [ {item, who, since} ],   // days elapsed is computed in-page
     priorities: [ "..." ],             // Memory "Current Priorities"
     people: [ {name, note} ]           // Memory "People"
   }
   ```
3. **Compute nothing by hand.** Day counts and stage totals are derived in-page from the dates you supply. Always use `YYYY-MM-DD`.
4. **Open it:** `open dashboard.html`
5. **Report in one line:** what changed since the last render — new applications, stage moves, anything now overdue.

## Rules

- Never invent a company, role, contact, or date. If the vault is empty, the dashboard shows its empty states — that is correct behavior, not a failure.
- Anything stale (no contact in 10+ days) should surface. The page flags it automatically from `lastContact`.
