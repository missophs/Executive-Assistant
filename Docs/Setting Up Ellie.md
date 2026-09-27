# Setting Up Ellie - Every Piece

Written 2026-09-26. Plain-English record of everything built for Ellie (Melissa's executive assistant) and how the pieces fit. Secrets are never written here, only their names.

## The short version
- Three emails, all sent by GitHub Actions, all started by cron-job.org: **Ellie - EA** (morning, ~7:30am ET, `morning-briefing.yml`, meant to replace the older Melissa Daily Briefing once proven), **Ellie - EA Midday** (1pm ET, only if something was filed/closed/needs a call — silent otherwise, `phone-sync.yml` LIGHT mode), **Ellie - EA Wrap-Up** (4:30pm ET, `wrap-up.yml`).
- **Ellie on your phone:** a Google Doc called `Ellie` (the live board) and a Google Doc called `Tell Ellie` (where you drop notes). A GitHub job reads your notes, files them, cleans the mail, and rebuilds the board at **6:30am, 1pm, and 4:30pm ET**.
- **Command Center:** a page in Claude (`https://claude.ai/code/artifact/ef023dc5-7573-4ac8-845f-ba8448315a5b`) that shows your calendar (live from Google Calendar) and your Top 3 & Follow Up (live from the `Ellie` doc).
- Everything runs from Git and cron-job.org, with GitHub's own native schedule as a backup trigger. Nothing should depend on a Claude cloud routine — as of 2026-09-27 three cloud routines (Phone Sync AM/PM, Midday Check) still duplicate this work and are being paused by hand; see "Still open" below.

## Where things live
| Piece | Where |
|---|---|
| Vault (tasks, memory, rules, scripts) | GitHub `missophs/Executive-Assistant`, branch `main` (private). Local copy: `~/Documents/Claude/Executive-Assistant` |
| Morning briefing code (old, being replaced) | GitHub `missophs/daily-briefing`, branch `webhooks`, file `scripts/generate_briefing.py`, workflow `.github/workflows/daily-briefing.yml` |
| Morning briefing code (new, "Ellie - EA") | `scripts/morning_briefing.py` + `scripts/morning_briefing_email.py` and `.github/workflows/morning-briefing.yml` in the vault repo |
| Phone sync + midday email code | `scripts/phone_sync.py` + `scripts/midday_email.py` and `.github/workflows/phone-sync.yml` in the vault repo |
| Wrap-up code | `scripts/wrap_up.py` + `scripts/wrapup_email.py` and `.github/workflows/wrap-up.yml` in the vault repo |
| Timers | cron-job.org (account already used for the briefing) |
| Command Center | Claude artifact `https://claude.ai/code/artifact/ef023dc5-7573-4ac8-845f-ba8448315a5b`. Source file: `dashboard.html` in the vault |
| Phone board | Google Drive doc `Ellie` (replaced on every sync, new file id each time). It stays in whatever folder Melissa last put it (currently `Ellie Setup`). New Ellie files default to `Ellie Files`, never loose in My Drive |
| Notes drop | Google Drive doc `Tell Ellie` |
| Topic files | Drive folder `Ellie Files` (id 18kMOjJuNFY_7u6rEVxsanFRUlX_GXJkh), one `Where we left off - <topic>` doc per topic |
| Every instruction Melissa has given | `Standing Instructions.md` in the vault |

## Schedule (all America/New_York)
- **Morning:** 7:00am/7:03am cron-job.org still starts the old Daily Briefing (not yet turned off — see "Still open"). Separately, 7:00am primary + 7:30am backup starts the new `morning-briefing.yml` ("Ellie - EA", job 8524112). Both may currently land in your inbox some mornings.
- **Midday:** 1:00pm ET only, cron-job.org job 8517937, `phone-sync.yml` with `light=1`. Silent unless something was filed, closed, or is ambiguous — sends "Ellie - EA Midday" only then (built 2026-09-27).
- **Phone sync (vault filing, silent):** 6:30am ET (job "Ellie Phone Sync Trigger") and 4:30pm ET (job "Ellie Phone Sync Trigger 4:30pm"), `phone-sync.yml` full mode.
- **Wrap-up email:** 4:30pm ET primary (job 8517934) + 5:00pm ET backup (job 8517938), `wrap-up.yml`, sends "Ellie - EA Wrap-Up".
- GitHub's own native `schedule:` cron in each workflow is the backup trigger if cron-job.org is late or down — confirmed largely dormant in practice (GitHub Actions' own scheduler is unreliable on this repo; cron-job.org is doing the real work). In November, when clocks change, shift the GitHub backup UTC crons by +1 hour. cron-job.org follows New York time by itself, no change needed.
- Every 30 minutes: "Trash newsletters trigger" runs the newsletter trash workflow in daily-briefing.
- "Job Search AM" is inactive. Not touched. "daily-job-search-trigger" (Claude cloud, 2pm ET) is separate from Ellie and still running — not audited here.

## What the phone sync does each run
1. Reads notes: mail you sent yourself (from and to melissaw212@gmail.com, or to melweiss212@) and the `Tell Ellie` doc. It skips Ellie's own emails and anything already handled.
2. Sorts each new note with Claude Haiku 4.5 (cheapest model): task, application news, memory, saved link, done, calendar entry, prep, "always trash <sender>", or unclear. Dated or "priority" tasks go to Today or This Week.
3. Creates calendar entries you ask for (no attendees, no duplicates). A dated "remind me" becomes a 30-minute entry (9am if no time) with a phone popup 10 minutes before. Titles are the short subject only. All-day if it is a plain calendar entry with no time.
4. Trashes inbox mail only when the sender is on `routines/trash-rules.md` (Gmail Trash only, never permanent, protected senders never touched). Every trashed message is listed on the board so you can undo it.
   Also, Haiku judges each new inbox thread once and trashes clearly unimportant bulk mail (promos, newsletters, product updates, surveys, social notifications). Real people, recruiters, applications, receipts, banking, health, security are never touched.
   RESCUE: it also checks Trash (last 3 days, interview/application/recruiter/meeting keywords), and moves a thread back to the inbox, starred, ONLY if Haiku says a real person or real applicant-tracking system wrote to her about a real role, application or meeting. Never bulk, no-reply or unsubscribe mail, never senders on `## Do Not Rescue` in `Memory.md`, never mail Ellie trashed herself. If a rescued thread shows up in Trash again, Ellie adds that sender to Do Not Rescue. Rescues are listed on the board ("Rescued from Trash").
5. Rebuilds the color-coded `Ellie` doc: what happened today, calendar for the rest of the week, trashed mail, current priorities, Today, This week, unsorted captures, application pipeline, waiting on, people, decisions, backlog. Waiting On items older than **5 days** are left off (still tracked in `Memory.md`'s Follow-Ups table, just not surfaced — Melissa, 2026-09-27).
6. Rebuilds the six "Where we left off" docs, only if their content changed.
7. Clears `Tell Ellie` if it processed a note.
8. Saves the vault back to GitHub (pull-rebase-and-retry on push conflicts, fixed 2026-09-27 after a race with the then-still-running cloud routines) and remembers handled message ids in `.ellie-state.json` so nothing is paid for twice.
9. **At 1pm only** (LIGHT mode): if anything was filed, closed, or came in ambiguous, sends the "Ellie - EA Midday" email (`scripts/midday_email.py`) — Filed Your Notes / Marked Done / Needs Your Call, whichever have content. Nothing new at 1pm = no email at all, same as always.

## Cost controls
- Nothing new = no AI call at all.
- Phone sync uses Haiku 4.5 and sends only new notes and a short list of open tasks (about 2,100 tokens in, 80 out per run, a fraction of a cent).
- Morning briefing: the phishing and trash-rescue sorting now uses Haiku 4.5. The briefing writer stays on Sonnet 4.6.
- Briefing cache: `.cache/classified_ids.json` in daily-briefing (message id -> time checked, 14-day expiry). An email is never sent to Claude twice. First real effect: Monday 2026-09-28.
- The GitHub jobs pay per token from the Anthropic API key, separate from the Claude plan. Set a spending limit in the Anthropic Console if you want a hard cap (Melissa said she will handle auto-reload).

## Secrets (names only)
- In `Executive-Assistant`: GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET, GOOGLE_REFRESH_TOKEN, ANTHROPIC_API_KEY.
- In `daily-briefing`: its own set (Google, Anthropic, mail settings). Not changed today.
- Google login: OAuth client `ellie-phone` (Desktop app) in Google Cloud project `tough-talent-493313-u9`, consent screen "gws local", scopes Gmail modify, Calendar events, Drive. The one-time helper is `scripts/get_google_token.py`.
- cron-job.org sends a GitHub token (fine-grained, Actions read/write on Executive-Assistant, expires one year after 2026-09-26). **Renew it before it expires** and paste the new one into both Ellie cron jobs, Advanced tab, Authorization header.

## How Melissa uses it
- Capture: email yourself, or write in `Tell Ellie`, or tell Ellie in chat. Examples: "remind me the vet is Thursday at 2", "add a priority from Tuesday to call the city about my documents", "always trash <sender>", "Prep: Acme interview Thursday" (only filed under Needs Melissa for now).
- Close a task: say "mark <task> done". It leaves the board at the next sync and shows once under what happened today.
- Ask "Ellie, where did we leave off on <topic>?" and Ellie opens the matching Drive doc first.
- "Ellie, sync" in chat runs the sync right away. Otherwise it runs at 6:30am and 4:30pm.
- Do not touch `/ea:draft-reply` or the job-search routine.

## Command Center
- Calendar: read live from Google Calendar each time it opens.
- Top 3 & Follow Up: read live from the `Ellie` doc (Today and This week sections) every 5 minutes while open. Each device asks once to allow Google Drive.
- Removed at Melissa's request: Priorities panel, Review / drift-check panel, check-boxes, and the old Conduit résumé task.
- Untested: the full path inside the Claude phone app.

## Still open
- **Pause (never delete) the three Claude cloud routines** that duplicate `phone-sync.yml`'s exact schedule — `trig_01GfvypZDLQZRM9F7Kphsnp8` "Phone Sync AM" (6:30am), `trig_01FEMRhJNPACVqw4HCRd6SNg` "Midday Check (brief)" (1pm), `trig_012SqPZ7Ui5nPFkko73adieN` "Phone Sync PM" (4:30pm). These were racing the Git version on live Gmail/Calendar/git writes and caused the 2026-09-27 4:30pm push failure. Melissa is pausing them herself once she's confirmed the Git runs hold up (an agent session can't disable them — created via the web API). Links: https://claude.ai/code/routines/trig_01GfvypZDLQZRM9F7Kphsnp8, /trig_01FEMRhJNPACVqw4HCRd6SNg, /trig_012SqPZ7Ui5nPFkko73adieN
- **Turn off the old `missophs/daily-briefing` "Melissa Daily Briefing"** once `morning-briefing.yml`'s "Ellie - EA" has proven itself over a few days — until then you may get two morning emails.
- Prep captures: only filed under Needs Melissa; no automatic prep doc yet.
- `trig_01YWcsQWdhbmQRGMTy5Yy8zG` "Ellie - Dashboard Refresh" (Claude cloud, twice daily) still costs Claude tokens for the dashboard regeneration — Melissa wants this moved off Claude entirely; not yet built.
- The Improve routine and the dashboard live view on the phone are untested.
- The subject line of a trashed email showed a garbled emoji on the board (cosmetic).

## If something breaks
| Symptom | Check |
|---|---|
| Board did not update | GitHub `Executive-Assistant` -> Actions -> "Ellie phone sync" for a red run; then cron-job.org job history (404 means the GitHub token expired or lacks the repo) |
| Sync says login failed | Rerun `~/.ellie-venv/bin/python ~/Documents/Claude/Executive-Assistant/scripts/get_google_token.py` (needs a new client JSON download from Google Cloud) |
| Note not filed | It files at the next run; check Task Board.md "Captured (unsorted)" |
| Wrong mail trashed | Gmail Trash, undo; then say "never trash <sender>" and it goes on the protected list |
| Briefing missing | daily-briefing repo -> Actions -> "Daily Briefing"; cron-job.org history |
| Dashboard tasks stale | Open it once and allow Google Drive; check the `Ellie` doc updated time |

## Build log, 2026-09-26
Google refresh token and secrets saved; phone sync script and workflow built and tested (dry run, then live); Haiku sorting; Drive topic files; cron-job.org triggers at 6:30am and 4:30pm; board sections for pipeline, people, decisions; briefing ID cache and Haiku sorting; Command Center cleaned and made to read the Drive board; all instructions saved in `Standing Instructions.md`.
- Reminders section on the wrap: dated open tasks for the next 7 days (no AI, no cost).
- Inbox table on the wrap: STATUS / FROM / SUBJECT / SUMMARY, NEEDS YOU rows first in red. Haiku writes one line per NEW inbox thread only; results are cached by thread id in `.ellie-state.json`, so seen mail costs nothing. Test run: about 3,200 tokens in. Rescue-from-Trash stays in the 7am briefing email.

### 2026-09-26 late additions
- Drive docs are updated in place, never trashed; Drive version history keeps every earlier version.
- cron-job.org jobs: wrap-up 4:45pm + backup 5:15pm (wrap-up.yml), midday light sync 1pm (phone-sync.yml, light=1), phone sync 6:30am + 4:30pm. GitHub crons back them all up. Shift GitHub UTC crons +1h in November.
- Rescue from Trash, dated reminders as calendar popups, 7-day calendar, Handoff.md each sync.

### 2026-09-27 — combined morning email, midday email, push-race fix, Waiting On cutoff
- Built `morning-briefing.yml`/`morning_briefing.py` (replaces daily-briefing + old cloud Standup once proven — neither turned off yet) and `wrap-up.yml`/`wrap_up.py` (replaces the old cloud Wrap-Up routine), both with send-once guards and cron-job.org primary + GitHub backup, same pattern as phone-sync.yml.
- Fixed `phone-sync.yml`: the workflow's `git push` had no retry, unlike morning-briefing.yml/wrap-up.yml. A push race (root cause: the still-live cloud routines writing to `main` at the same schedule) failed the 4:30pm run on commit 4aacbfa. Added the same pull-rebase-and-retry loop the other two already use.
- Discovered the three cloud routines listed under "Still open" had been silently repurposed (renamed, rescheduled, prompts swapped) at some point without `routines/README.md` being updated — its routine table was pointing at names/schedules that no longer matched what was actually live. Corrected.
- Built the midday conditional email (`scripts/midday_email.py`, hooked into `phone_sync.py`'s LIGHT mode) — closes the gap noted 2026-09-27 morning in Standing Instructions.md ("the 1pm run is meant to send an email only if something new happened... no conditional email exists yet").
- Added the dashboard's missing "Waiting On" panel — the data (`DATA.waiting`, `STALE_DAYS`, `daysSince`) was already wired up in `dashboard.html` but never rendered.
- Waiting On items older than 5 days now drop out of the dashboard, the wrap-up email, and the phone board (still tracked in `Memory.md`, just not surfaced) — Melissa's instruction, 2026-09-27.
