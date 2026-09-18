---
description: Regenerate the visual dashboard from the vault and open it in the browser
allowed-tools: Read, Write, Edit, Glob, Bash, Artifact
---

# /dashboard — Render the Command Center

Read the vault, regenerate `dashboard.html`, publish it, and open it.

## Steps

1. **Read the data.** `Task Board.md`, `Memory.md`, and the most recent file in `Daily Notes/`.
2. **Regenerate `dashboard.html`.** Keep the existing design exactly — only the data changes. Update the `DATA` object near the top of the `<script>` block; do not rewrite the CSS or the layout.

   `DATA` shape:
   ```js
   {
     generated: "2026-08-29",          // today
     calendar: [ {day, time, title, conflict} ], // today's AND tomorrow's Google Calendar events — day is "Today"/"Tomorrow", time like "12:00–1:30 PM ET", conflict:true only for same-day overlaps. Empty array if nothing either day.
     today: [ {id, task, why, due} ],   // from Task Board "Today", max 3 — id = "YYYY-MM-DD-t0" etc, must stay stable day-to-day so checkbox state matches
     week: [ {task, due} ],             // from Task Board "This Week"
     waiting: [ {item, who, since} ],   // from Task Board "Waiting On" — days elapsed is computed in-page
     priorities: [ "..." ],             // Memory "Current Priorities"
     people: [ {name, note} ]           // Memory "People"
   }
   ```
   Calendar events come from Google Calendar (`list_events`, `melissaw212@gmail.com`, today 00:00–23:59 America/New_York) — never invent one.

   **Also update the pre-baked HTML** inside `#stampDate`, `#badges`, `#stats`, `#todayNote`, `#todayWrap`, `#waitWrap`, `#prioWrap`, and `#pplWrap` so it matches `DATA` exactly (same markup the script below would generate, with day-counts computed by hand for this one step). This is deliberate duplication: a downloaded copy of this file, or anything that reads it without running JavaScript (iOS Quick Look, a link pasted into a chat for fetching), only ever sees this static markup — the `<script>` block then overwrites it with the live, interactive version when JS does run. If only `DATA` is updated and the static markup is left stale, the phone/download path silently regresses to old data.
3. **Compute nothing by hand in the script.** Day counts are derived in-page from the dates you supply. Always use `YYYY-MM-DD`. (The one exception is the static markup from step 2, which has no script to compute for it.)
4. **Publish it.** Use the Artifact tool to republish `dashboard.html` to the canonical Command Center artifact: `https://claude.ai/code/artifact/ef023dc5-7573-4ac8-845f-ba8448315a5b`. This is what the phone shortcut opens — skipping this step means the phone shows stale data. Do not publish a new artifact; always target this URL.
5. **Open it locally too:** `open dashboard.html`
6. **Report in one line:** what changed since the last render — tasks added/closed, anything now overdue.

## Rules

- Never invent a task, contact, or date. If the vault is empty, the dashboard shows its empty states — that is correct behavior, not a failure.
- Anything stale (no reply in 10+ days on a Waiting On item) should surface. The page flags it automatically from `since`.
- There is exactly one live Command Center artifact (`ef023dc5...`). Never publish a second one — a duplicate is how the phone and computer end up out of sync.
- **Waiting On wording:** every item must be unambiguous about who owes whom. Never write bare "Reply to X" — it reads as an instruction for Melissa to act, even when she's the one who already acted and is waiting on the other person. Confirmed as a real point of confusion 2026-09-18 ("Reply to cold outreach" read as her to-do when she'd already sent it). Phrase it from her point of view: "No reply to your outreach yet — you sent it, waiting on them" vs. "Needs your decision — nothing sent yet" for the reverse case.
- **Getting it onto her phone home screen:** "Add to Home Screen" only works from the **Safari app itself**, navigated to the live artifact URL via its own address bar. It does NOT appear from Mail's attachment preview, the Files app preview, or any in-app browser — confirmed after two rounds of "it doesn't work" (2026-09-16). Don't route her through emailed HTML attachments or iCloud Drive file sync for "always current on my phone" — those only work as one-off offline snapshots. Give her: open Safari → paste `https://claude.ai/code/artifact/ef023dc5-7573-4ac8-845f-ba8448315a5b` → Share → Add to Home Screen.
