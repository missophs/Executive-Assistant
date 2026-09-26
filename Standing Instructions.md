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

## Added 2026-09-26 (later)
- Save tokens: cache as much as possible. Midday is very brief and silent (`routines/midday-light.md`): one look for new captures, stop if nothing is new.
- When she says something is done, remove it from the lists and board. It shows once in the wrap-up ("what happened today"), then never again.
- Google Drive folders by topic under `Ellie Files` with a "Where we left off - <Topic>" file each, plus a Calendar file. Having everything only in the vault does not work for the phone. (`routines/drive-map.md`)
- Color-code everything possible, phone included (the board and topic files are Google Docs with color). One key: red urgent, amber follow-up, blue calendar/appointments, green job search/interviews/done, purple events/other, gray low priority.
- "Always trash <sender>" goes in `routines/trash-rules.md` (wrap-up) and in the daily-briefing repo `scripts/generate_briefing.py` (morning). Goal: everything runs from Git and cron so there are no issues.

## Added 2026-09-26 (evening)
- Move Ellie to Git and cron one piece at a time, phone sync first, and test each before the next. Keep the Claude cloud routine running until the Git version is proven, then pause it (never delete).
- Cache as much as possible to save tokens (asked twice). Ideas queued: run Improve to shrink Memory.md, midday early-exit (done), rebuild Drive topic files only when their source changed (done).
- Sidebar confusion: the left-hand list in the app is folders of past chats, not running assistants. What actually runs: the Melissa Daily Briefing (GitHub Actions + cron-job.org) and the Claude cloud routines listed under Routines.
- She wants every question answered in one reply so she does not have to repeat herself.
