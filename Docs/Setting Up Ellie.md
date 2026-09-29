# Setting Up Ellie - Every Piece

Written 2026-09-26. Plain-English record of everything built for Ellie (Melissa's executive assistant) and how the pieces fit. Secrets are never written here, only their names.

## The short version
_(as written 2026-09-26 — kept as-is; see "2026-09-27 update" bullet below for what changed)_

- One daily email: the **Melissa Daily Briefing**, sent at about 7:00am ET by GitHub, started by cron-job.org.
- **Ellie on your phone:** a Google Doc called `Ellie` (the live board) and a Google Doc called `Tell Ellie` (where you drop notes). A GitHub job reads your notes, files them, cleans the mail, and rebuilds the board at **6:30am and 4:30pm ET**. The 4:30pm run is the end-of-day wrap.
- **Command Center:** a page in Claude that shows your calendar (live from Google Calendar) and your Top 3 & Follow Up (live from the `Ellie` doc).
- Everything runs from Git and cron-job.org. Nothing depends on a Claude cloud routine once the old routine is paused.
- **→ 2026-09-27 update:** now three emails, all Git + cron-job.org: **Ellie - EA** (morning, ~7:30am ET, `morning-briefing.yml`, meant to replace the Melissa Daily Briefing above once proven — both may currently be landing), **Ellie - EA Midday** (1pm ET, only if something was filed/closed/needs a call, otherwise silent), **Ellie - EA Wrap-Up** (4:30pm ET). Phone board now also refreshes at 1pm. Command Center link corrected to `https://claude.ai/code/artifact/ef023dc5-7573-4ac8-845f-ba8448315a5b` (the `/artifact/WWoVTEpKHKezZaJWiS3x74` link above was stale). Found: three Claude cloud routines were still duplicating this work on the same schedule — being paused by hand, not deleted. Full detail in the 2026-09-27 Build Log at the bottom of this doc.

## Where things live
_(as written 2026-09-26 — kept as-is; new rows added 2026-09-27 below, none of the original rows changed)_

| Piece | Where |
|---|---|
| Vault (tasks, memory, rules, scripts) | GitHub `missophs/Executive-Assistant`, branch `main` (private). Local copy: `~/Documents/Claude/Executive-Assistant` |
| Morning briefing code | GitHub `missophs/daily-briefing`, branch `webhooks`, file `scripts/generate_briefing.py`, workflow `.github/workflows/daily-briefing.yml` |
| Phone sync code | `scripts/phone_sync.py` and `.github/workflows/phone-sync.yml` in the vault repo |
| Timers | cron-job.org (account already used for the briefing) |
| Command Center | Claude artifact `https://claude.ai/artifact/WWoVTEpKHKezZaJWiS3x74`. Source file: `dashboard.html` in the vault _(→ this link is stale, corrected below)_ |
| Phone board | Google Drive doc `Ellie` (replaced on every sync, new file id each time). It stays in whatever folder Melissa last put it (currently `Ellie Setup`). New Ellie files default to `Ellie Files`, never loose in My Drive |
| Notes drop | Google Drive doc `Tell Ellie` |
| Topic files | Drive folder `Ellie Files` (id 18kMOjJuNFY_7u6rEVxsanFRUlX_GXJkh), one `Where we left off - <topic>` doc per topic |
| Every instruction Melissa has given | `Standing Instructions.md` in the vault |
| **(added 2026-09-27)** Morning briefing code, new "Ellie - EA" version | `scripts/morning_briefing.py` + `scripts/morning_briefing_email.py` and `.github/workflows/morning-briefing.yml` in the vault repo — meant to replace the `daily-briefing` row above once proven |
| **(added 2026-09-27)** Midday email code | `scripts/midday_email.py`, hooked into `phone_sync.py`'s LIGHT mode |
| **(added 2026-09-27)** Wrap-up code | `scripts/wrap_up.py` + `scripts/wrapup_email.py` and `.github/workflows/wrap-up.yml` in the vault repo |
| **(added 2026-09-27)** Command Center — corrected link | `https://claude.ai/code/artifact/ef023dc5-7573-4ac8-845f-ba8448315a5b` (the row above, `/artifact/WWoVTEpKHKezZaJWiS3x74`, was wrong/stale) |

## Schedule (all America/New_York)
_(as written 2026-09-26 — kept as-is; 2026-09-27 additions below)_

- 7:00am and 7:03am: cron-job.org starts the Daily Briefing (the 7:03 job is the backup). GitHub's own timers (about 3:30am and 4:15am ET) are extra backups; the workflow skips itself if a briefing already went out today.
- 6:30am and 4:30pm: cron-job.org starts the Ellie phone sync (jobs "Ellie Phone Sync Trigger" and "Ellie Phone Sync Trigger 4:30pm"). GitHub timers at 10:30 and 20:30 UTC are backups. In November, when clocks change, shift only the GitHub backup times by +1 hour UTC. cron-job.org follows New York time by itself.
- Every 30 minutes: "Trash newsletters trigger" runs the newsletter trash workflow in daily-briefing.
- "Job Search AM" is inactive. Not touched.
- **(added 2026-09-27)** New `morning-briefing.yml` ("Ellie - EA"): 7:00am primary + 7:30am backup, job 8524112. Runs alongside the old Daily Briefing above until proven — you may get two morning emails for now.
- **(added 2026-09-27)** New midday email: 1:00pm ET only, cron-job.org job 8517937, `phone-sync.yml` with `light=1`. Silent unless something was filed, closed, or is ambiguous.
- **(added 2026-09-27)** Wrap-up email moved to its own workflow: 4:30pm ET primary (job 8517934) + 5:00pm ET backup (job 8517938), `wrap-up.yml`, sends "Ellie - EA Wrap-Up".
- **(added 2026-09-27)** Checked: GitHub's own native `schedule:` cron in each workflow (the "backup" timers mentioned above) is largely dormant in practice — cron-job.org is doing essentially all the real triggering. Worth knowing if a run seems to be "only" firing at cron-job.org's time and never at GitHub's.
- **(added 2026-09-27)** "daily-job-search-trigger" (Claude cloud, 2pm ET) is separate from Ellie and still running — not audited in this session.

## What the phone sync does each run
_(as written 2026-09-26 — kept as-is; 2026-09-27 additions as items 9-11)_

1. Reads notes: mail you sent yourself (from and to melissaw212@gmail.com, or to melweiss212@) and the `Tell Ellie` doc. It skips Ellie's own emails and anything already handled.
2. Sorts each new note with Claude Haiku 4.5 (cheapest model): task, application news, memory, saved link, done, calendar entry, prep, "always trash <sender>", or unclear. Dated or "priority" tasks go to Today or This Week.
3. Creates calendar entries you ask for (no attendees, no duplicates). A dated "remind me" becomes a 30-minute entry (9am if no time) with a phone popup 10 minutes before. Titles are the short subject only. All-day if it is a plain calendar entry with no time.
4. Trashes inbox mail only when the sender is on `routines/trash-rules.md` (Gmail Trash only, never permanent, protected senders never touched). Every trashed message is listed on the board so you can undo it.
   Also, Haiku judges each new inbox thread once and trashes clearly unimportant bulk mail (promos, newsletters, product updates, surveys, social notifications). Real people, recruiters, applications, receipts, banking, health, security are never touched.
   RESCUE: it also checks Trash (last 3 days, interview/application/recruiter/meeting keywords), and moves a thread back to the inbox, starred, ONLY if Haiku says a real person or real applicant-tracking system wrote to her about a real role, application or meeting. Never bulk, no-reply or unsubscribe mail, never senders on `## Do Not Rescue` in `Memory.md`, never mail Ellie trashed herself. If a rescued thread shows up in Trash again, Ellie adds that sender to Do Not Rescue. Rescues are listed on the board ("Rescued from Trash").
5. Rebuilds the color-coded `Ellie` doc: what happened today, calendar for the rest of the week, trashed mail, current priorities, Today, This week, unsorted captures, application pipeline, waiting on, people, decisions, backlog.
6. Rebuilds the six "Where we left off" docs, only if their content changed.
7. Clears `Tell Ellie` if it processed a note.
8. Saves the vault back to GitHub and remembers handled message ids in `.ellie-state.json` so nothing is paid for twice.
9. **(added 2026-09-27)** Waiting On items older than **5 days** are now left off item 5's board rebuild (still tracked in `Memory.md`'s Follow-Ups table, just not surfaced — Melissa's instruction).
10. **(added 2026-09-27)** Item 8's GitHub save now retries with pull-rebase on a push conflict — it had none before, and a race with the then-still-running cloud routines failed a run on commit 4aacbfa. Fixed.
11. **(added 2026-09-27)** New: at 1pm only (LIGHT mode), if anything was filed, closed, or came in ambiguous, sends the "Ellie - EA Midday" email (`scripts/midday_email.py`) — Filed Your Notes / Marked Done / Needs Your Call, whichever have content. Nothing new at 1pm = no email at all, same as always.

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
_(as written 2026-09-26 — kept as-is; status notes and new items added 2026-09-27)_

- Pause (never delete) the old Claude cloud phone-sync routine after a few good mornings. **→ 2026-09-27: this turned out to be three routines, not one — see the new bullet below for the full list; none paused yet, Melissa is doing it herself.**
- Prep captures: only filed under Needs Melissa; no automatic prep doc yet. _(still true 2026-09-27)_

- Midday 1pm check, the Improve routine, and the dashboard live view on the phone are untested. **→ 2026-09-27: midday 1pm check is now built (see Build Log) — the conditional email and the silent vault-filing pass are both live. Improve routine and dashboard live view still untested.**
- The subject line of a trashed email showed a garbled emoji on the board (cosmetic). _(not looked at 2026-09-27)_

- **(added 2026-09-27)** The three Claude cloud routines that duplicate `phone-sync.yml`'s exact schedule — `trig_01GfvypZDLQZRM9F7Kphsnp8` "Phone Sync AM" (6:30am), `trig_01FEMRhJNPACVqw4HCRd6SNg` "Midday Check (brief)" (1pm), `trig_012SqPZ7Ui5nPFkko73adieN` "Phone Sync PM" (4:30pm) — were racing the Git version on live Gmail/Calendar/git writes and caused the 2026-09-27 4:30pm push failure. Melissa is pausing them herself once she's confirmed the Git runs hold up (an agent session can't disable them — created via the web API). Links: https://claude.ai/code/routines/trig_01GfvypZDLQZRM9F7Kphsnp8, /trig_01FEMRhJNPACVqw4HCRd6SNg, /trig_012SqPZ7Ui5nPFkko73adieN
- **(added 2026-09-27)** Turn off the old `missophs/daily-briefing` "Melissa Daily Briefing" once `morning-briefing.yml`'s "Ellie - EA" has proven itself over a few days — until then you may get two morning emails.
- **(added 2026-09-27)** `trig_01YWcsQWdhbmQRGMTy5Yy8zG` "Ellie - Dashboard Refresh" (Claude cloud, twice daily) still costs Claude tokens for the dashboard regeneration — Melissa wants this moved off Claude entirely; not yet built.

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

### 2026-09-27 (night) — Richer morning email, and a real live-verification pass

- Ported the features the old "Melissa Daily Briefing" had that the new "Ellie - EA" morning email did not yet: an Executive Summary box (top priority, inbox items needing her, longest open wait, RSVP-needed count, conflict count), an Action Required list of every board item with a due date (not just the top 3), calendar conflict detection (overlapping timed events flagged), RSVP-needed flags on calendar events, and the Email Triage Quick List rebuilt as a real table. Files: `scripts/morning_briefing.py`, `scripts/morning_briefing_email.py`.
- Confirmed the Ellie Commands table (`/ea:setup`, `/ea:sync`, `/ea:done`, `/ea:meeting-prep`, `/ea:assess`, `/ea:draft-reply`, `/ea:review-doc`, `/ea:improve`) matches what was built the day before, word for word. `/ea:inbox` is deliberately left off (documented decision: "the briefing triages").
- Built Waiting-On removal into `phone_sync.py`'s "done" handling: saying "Nasreen replied" or "mark it done" now closes a Memory.md Follow-Ups row (not just a Task Board checkbox), removes it, and logs "No longer waiting on X" under Done.
- **Live verification, not just a code read**: triggered real runs instead of trusting the files.
  - Phone sync's push-race fix (see the entry above) confirmed working on an actual live run — build, commit, pull-rebase, push, all clean. All three daily slots (6:30am/1pm/4:30pm ET) had already run successfully today via cron-job.org.
  - Wrap-up confirmed to have actually sent a real email today at 4:30pm ET (not just "should send") — verified against the actual commit and the actual "Build and send" step result. The send-once guard correctly kept two backup firings silent.
  - Morning briefing had never run before (built after its own morning trigger window had already passed today). Test-firing it live caught a real crash: the calendar conflict/RSVP change widened each event to a 4-value tuple, and one loop in the Prepare section still unpacked 2, throwing `ValueError`. Fixed and re-verified with a second live run — clean. Its first real (non-dry, non-test) send is still ahead: tomorrow's ~7am ET trigger.

### 2026-09-27 (night, final) — Complete bug list for tonight: both fixed, both verified

Melissa asked directly whether every bug tonight was fixed, after two failure-notification emails (GitHub's own run-failed email, and the workflow's own Gmail alert — both were the same single event, bug #2 below). This is the full list, nothing else broke:

1. `phone-sync.yml` git push had no retry — the original failure that started this session. Fixed with pull-rebase-and-retry. Verified live.
2. `morning_briefing.py` Prepare section crashed (`ValueError`, tuple-unpacking mismatch from the conflict/RSVP change) on its first-ever run. Fixed, verified live with a second successful run.

Checked at time of writing: all three workflows green, zero open failures. Only remaining unknown is `morning-briefing.yml`'s first real (non-dry) send, tomorrow ~7am ET.

## Update 2026-09-29: email design and prep
All three Ellie emails share one look (`scripts/ellie_ui.py`, Ellie purple). The morning email has every section the old Melissa Daily Briefing had. Wrap-up and midday: design only, no inbox triage. To get a prep doc, tell Ellie from your phone: "prep for interview with <company> tomorrow" — it appears in the next morning email's Prepare section. Rollback for this change: `git revert -m 1 90a4c7a` on main.
