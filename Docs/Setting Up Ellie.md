# Setting Up Ellie - Every Piece

Written 2026-09-26. Plain-English record of everything built for Ellie (Melissa's executive assistant) and how the pieces fit. Secrets are never written here, only their names.

## The short version
- One daily email: the **Melissa Daily Briefing**, sent at about 7:00am ET by GitHub, started by cron-job.org.
- **Ellie on your phone:** a Google Doc called `Ellie` (the live board) and a Google Doc called `Tell Ellie` (where you drop notes). A GitHub job reads your notes, files them, cleans the mail, and rebuilds the board at **6:30am and 4:30pm ET**. The 4:30pm run is the end-of-day wrap.
- **Command Center:** a page in Claude that shows your calendar (live from Google Calendar) and your Top 3 & Follow Up (live from the `Ellie` doc).
- Everything runs from Git and cron-job.org. Nothing depends on a Claude cloud routine once the old routine is paused.

## Where things live
| Piece | Where |
|---|---|
| Vault (tasks, memory, rules, scripts) | GitHub `missophs/Executive-Assistant`, branch `main` (private). Local copy: `~/Documents/Claude/Executive-Assistant` |
| Morning briefing code | GitHub `missophs/daily-briefing`, branch `webhooks`, file `scripts/generate_briefing.py`, workflow `.github/workflows/daily-briefing.yml` |
| Phone sync code | `scripts/phone_sync.py` and `.github/workflows/phone-sync.yml` in the vault repo |
| Timers | cron-job.org (account already used for the briefing) |
| Command Center | Claude artifact `https://claude.ai/artifact/WWoVTEpKHKezZaJWiS3x74`. Source file: `dashboard.html` in the vault |
| Phone board | Google Drive doc `Ellie` (replaced on every sync, new file id each time). It stays in whatever folder Melissa last put it (currently `Ellie Setup`). New Ellie files default to `Ellie Files`, never loose in My Drive |
| Notes drop | Google Drive doc `Tell Ellie` |
| Topic files | Drive folder `Ellie Files` (id 18kMOjJuNFY_7u6rEVxsanFRUlX_GXJkh), one `Where we left off - <topic>` doc per topic |
| Every instruction Melissa has given | `Standing Instructions.md` in the vault |

## Schedule (all America/New_York)
- 7:00am and 7:03am: cron-job.org starts the Daily Briefing (the 7:03 job is the backup). GitHub's own timers (about 3:30am and 4:15am ET) are extra backups; the workflow skips itself if a briefing already went out today.
- 6:30am and 4:30pm: cron-job.org starts the Ellie phone sync (jobs "Ellie Phone Sync Trigger" and "Ellie Phone Sync Trigger 4:30pm"). GitHub timers at 10:30 and 20:30 UTC are backups. In November, when clocks change, shift only the GitHub backup times by +1 hour UTC. cron-job.org follows New York time by itself.
- Every 30 minutes: "Trash newsletters trigger" runs the newsletter trash workflow in daily-briefing.
- "Job Search AM" is inactive. Not touched.

## What the phone sync does each run
1. Reads notes: mail you sent yourself (from and to melissaw212@gmail.com, or to melweiss212@) and the `Tell Ellie` doc. It skips Ellie's own emails and anything already handled.
2. Sorts each new note with Claude Haiku 4.5 (cheapest model): task, application news, memory, saved link, done, calendar entry, prep, "always trash <sender>", or unclear. Dated or "priority" tasks go to Today or This Week.
3. Creates calendar entries you ask for (no attendees, no duplicates). All-day if no time is given.
4. Trashes inbox mail only when the sender is on `routines/trash-rules.md` (Gmail Trash only, never permanent, protected senders never touched). Every trashed message is listed on the board so you can undo it.
5. Rebuilds the color-coded `Ellie` doc: what happened today, calendar for the rest of the week, trashed mail, current priorities, Today, This week, unsorted captures, application pipeline, waiting on, people, decisions, backlog.
6. Rebuilds the six "Where we left off" docs, only if their content changed.
7. Clears `Tell Ellie` if it processed a note.
8. Saves the vault back to GitHub and remembers handled message ids in `.ellie-state.json` so nothing is paid for twice.

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
- Pause (never delete) the old Claude cloud phone-sync routine after a few good mornings.
- Prep captures: only filed under Needs Melissa; no automatic prep doc yet.
- Midday 1pm check, the Improve routine, and the dashboard live view on the phone are untested.
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
