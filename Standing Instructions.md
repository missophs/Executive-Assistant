# Standing Instructions (from Melissa)

Everything Melissa tells Ellie about how things should work. Newest additions at the bottom of each section. Ellie appends every new instruction here, dated, whether she gives it in chat, in `Tell Ellie`, or by email. Never delete an entry unless she says so.

## Repos (which one to change)
- `missophs/Executive-Assistant` (private): Ellie's vault, phone sync, dashboard, `routines/*.md`, this file.
- `missophs/daily-briefing`: the morning email. Live branch is `webhooks`. File: `scripts/generate_briefing.py`.

## The one email (2026-09-26)
- The only email is "Melissa Daily Briefing", sent by GitHub Actions. Keep the title and the look. Do not change how it runs: cron-job.org at 7:00 and 7:03 ET, GitHub schedule backups, the send-once guard.
- Include: 7-day calendar, `/ea:` command table, Prepare section (interviews and the like, by day), "Top 3 & Follow Up" (no "Gone Quiet"), draft replies.
- Draft replies: ask first, drafts only, never send, run through `/humanize`. Leave `/ea:draft-reply` alone.
- Ellie's old email routines are paused, never deleted.
- Inbox triage happens in the briefing. The 4:30pm wrap-up also triages: trash per `routines/trash-rules.md` plus anything that clearly does not look important; list what was trashed so she can undo it. Never permanent delete.

## Phone (2026-09-26)
- Must have Ellie on the phone: Drive files `Ellie` (board) and `Tell Ellie` (capture). Self-emails to melissaw212@gmail.com land under the Gmail Ellie label by filter; sync searches `in:anywhere`.
- Phone sync runs 6:30am and 4:30pm ET. The 4:30pm one is the end-of-day wrap.
- Wrap-up says: what happened today, what is on the calendar for the rest of the week, reminders, inbox triage, prep links. Never list an event that already happened. Dates come before meeting names.
- Reminders: dated ones go on Google Calendar; undated ones show on the board. Ellie cannot send a timed push.
- `Prep: <meeting>` in `Tell Ellie` makes a prep doc in `Meetings/`.
- She can start sync and improve from her phone or chat (Run now on the routines).
- To close anything she tells Ellie it is done. Done items are removed, not shown as pending. No check-boxes.
- She wants Drive folders by topic so she can ask "Ellie, where did we leave off on X?" and Ellie knows which file to read. (Proposed, not built yet.)

## Dashboard / Command Center (2026-09-26)
- Calendar shows the whole week, never past events, date first then meeting name, everything color-coded.
- Heading is "Top 3 & Follow Up". Remove "Gone Quiet".
- Keep it working. Refreshed 7:20am and 5:20pm ET.

## Commands and cost (2026-09-26)
- `/ea:` commands sync to Google Drive. Meeting prep she can start on her own. Hold `/ea:assess`. Skip `/ea:inbox` as a command (the briefing triages).
- Routine cache is fine. Do not use `cache_control`.

## Working rules
- Save everything she tells Ellie into files, not just notes: instructions, decisions, corrections, preferences. Record it in this file the same day.
- Explain in plain language. She is a senior HR executive, not an engineer.
