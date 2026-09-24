# Handoff

Last live chat: 2026-09-24. Type `handoff` at the start of a new chat in this folder and Ellie picks up exactly here.

## Open — pick this up first
**The "open chat" iPhone Shortcut.** Melissa's Tell Ellie Shortcut only sends (one-way) — typing a question into it doesn't get her an answer, because it just files as a capture for the next routine. She wants to talk through building a **second, simpler Shortcut** that just opens a live chat with Ellie in Safari/the app with one tap, so she can get real-time answers instead of waiting on a routine. Not yet built. She was too tired to do it tonight — resume this conversation tomorrow.

## What changed today (2026-09-24), already committed and pushed
- All three routines (Standup, Midday, Wrap-Up) now regenerate `dashboard.html` and republish the Command Center artifact at the end of their run, whenever they file something — so the board stops lagging until she asks.
- Wrap-Up moved from 5pm to **4:30pm ET**, and now checks Google Calendar (next 7 days) each run, so calendar additions (e.g. a personal event) reach the Command Center by end of day.
- Midday Sweep is **paused** by Melissa (to save tokens) — leave it paused unless she says otherwise.
- Added a task to `Task Board.md`: call New York Health Insurance re: the HRA, tomorrow (2026-09-25), flagged to remind all day.

## Still outstanding — she owes a manual step
The **live** routines at claude.ai/code/routines are separate from the backup files in `routines/` — Ellie can't push to them directly (they were created via the UI, not by an agent session). Melissa needs to paste the updated `routines/wrap-up.md` text into the live Wrap-Up routine (new 4:30pm time + calendar step) herself, the same way she did for Standup earlier. Offer to give her the exact copy-paste text again if she hasn't done it yet.

## Standing facts worth remembering
- Tell Ellie captures (Shortcut/Drive note) are one-way and only get processed at the routines' fixed times (7:30am Standup, 4:30pm Wrap-Up now that Midday's paused). Talking to Ellie directly in a live chat is always instant — no wait.
- Command Center artifact: `https://claude.ai/code/artifact/ef023dc5-7573-4ac8-845f-ba8448315a5b`
- `Task Board.md` has been observed stuck at stale (~9/4-era) content on a couple of re-reads even after edits elsewhere in the vault landed fine — worth a sanity check next session if it looks wrong again.
