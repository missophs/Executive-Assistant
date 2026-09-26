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

## Added 2026-09-26 (Git move)
- Do not touch the job-search routine (`daily-job-search-trigger`, repo `job-search-routine`) or its sidebar chats.
- Permanent local copy of the vault: `~/Documents/Claude/Executive-Assistant` (the copy in `/private/tmp` is temporary scratch). She starts new Ellie chats in the `hr-executive-assessment` folder so memory loads.
- Goal: everything runs from Git and cron so she knows it runs. Phone sync first. Needs: Google Drive API enabled in project `tough-talent-493313-u9` ("My Project 10929"), a new refresh token from `scripts/get_google_token.py` (scopes gmail.modify, calendar.events, drive), and secrets GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET, GOOGLE_REFRESH_TOKEN, ANTHROPIC_API_KEY in the Executive-Assistant repo.

## 2026-09-26 (later) - Phone sync moves to Git + cron
- Melissa: move Ellie phone sync from the Claude cloud routine to a GitHub Action, test it, then pause (never delete) the routine.
- Built `scripts/phone_sync.py` + `.github/workflows/phone-sync.yml` (no AI yet). Google secrets saved in this repo. Dry run passed 2026-09-26. Not yet live; cron-job.org triggers not yet added.
- Not yet in the Action: Prep captures, Drive topic files, AI filing of captures, ANTHROPIC_API_KEY.

## 2026-09-26 (evening) - Full record of what was decided and built today
Melissa's instructions (all standing):
- One daily email only: the Melissa Daily Briefing, sent by the GitHub Action in daily-briefing (branch webhooks), timed by cron-job.org. Ellie sends no email.
- Ellie phone piece stays: Drive `Ellie` (board), `Tell Ellie` (capture), synced 6:30am and 4:30pm ET. 4:30pm is the end-of-day wrap: what happened today, calendar for the rest of the week (date first, future events only), reminders, inbox triage that trashes per `routines/trash-rules.md`.
- Everything color-coded, phone included. Done items disappear after one showing; she tells Ellie "mark it done" (no check-boxes).
- Drive folders by topic so she can ask "Ellie, where did we leave off on <topic>?" Ellie opens `Where we left off - <topic>` first.
- Cache everything possible to save tokens. Save every instruction in files (this file). Leave /ea:draft-reply and the job-search routine alone.
- Move everything from Claude cloud routines to Git + cron, one piece at a time, phone sync first, test each; pause (never delete) a cloud routine only after the Git version is proven.
- Step-by-step, child-level instructions, one action at a time. Never make her repeat. Never ask her to paste secrets in chat.
Built and verified today:
- Google refresh token + secrets GOOGLE_CLIENT_ID/SECRET/REFRESH_TOKEN and ANTHROPIC_API_KEY saved in missophs/Executive-Assistant (new OAuth client `ellie-phone`, Desktop).
- `scripts/phone_sync.py` + `.github/workflows/phone-sync.yml`: reads captures (self-sent mail + Tell Ellie), Haiku 4.5 sorts them (task, application, memory, link, done, calendar, prep, trash, unclear), trashes only per trash-rules.md, rebuilds the color `Ellie` Doc, rebuilds six `Where we left off` Docs only when changed, records seen ids in `.ellie-state.json`. Live run 2026-09-26 11:51 ET succeeded (AI cost 2,095 in / 70 out tokens).
- Schedule added: 10:30 and 20:30 UTC (6:30am / 4:30pm EDT). Shift +1h UTC when DST ends.
- daily-briefing: `.cache/classified_ids.json` (message id -> timestamp, 14-day expiry, "r:" prefix for trash-rescue checks) so Claude never re-checks an email; phishing/newsletter/rescue sorting switched to Haiku 4.5; briefing writer stays Sonnet 4.6. Cache logic tested with a fake Claude (not yet run in a real 7am run).
Not done yet: the cloud phone-sync routine is still active (pause it after the 6:30am run is compared); cron-job.org timers for the phone sync (GitHub schedule is the backup); Prep captures are only filed under Needs Melissa; board lacks Applications pipeline/People/Decisions sections; midday 1pm check, Improve routine, dashboard live calendar untested.
- 2026-09-26: cron-job.org job "Ellie Phone Sync Trigger" created (POST to phone-sync.yml dispatches, body {"ref":"main"}, 6:30am America/New_York daily, enabled). Test run returned 404: the copied GitHub token only covers daily-briefing. Needs a token with Actions read/write on missophs/Executive-Assistant. The 4:30pm job is not created yet.
- 2026-09-26: New GitHub token added to cron-job.org; test run started a phone-sync run (16:04Z, success). Jobs live: "Ellie Phone Sync Trigger" 6:30am ET and "Ellie Phone Sync Trigger 4:30pm" 4:30pm ET, both daily, America/New_York (cron-job.org handles DST). GitHub schedule stays as backup. Token expires in 1 year: renew before then.
- 2026-09-26: Board now includes Current priorities, Application pipeline (open roles by stage), People, Decisions & context (live run 12:09pm ET verified in Drive). The 4:30pm run IS the end-of-day wrap. Anything Melissa says or emails to herself between runs is sorted at the next run. Command Center (dashboard) is NOT yet fed by the Git sync; next step.
- 2026-09-26 (Melissa, from phone): Command Center must not show "Send resume to Nasreen (Conduit Health)" (moot, done). Remove the Priorities panel entirely (anything in it should be a to-do instead). Remove the Review / drift-check panel and its old items. Done in dashboard.html and republished. Keep them off in future dashboard rebuilds.
- 2026-09-26 (Melissa): a note like "add a priority from Tuesday to call New York City about my documents" = all-day calendar block on that date AND a priority task (Top 3 & Follow Up). Done for 9/29. The sync now adds both when a calendar capture is called a priority.
- 2026-09-26: Command Center now reads the Drive `Ellie` doc live (Google Drive connector, search_files + read_file_content) for Top 3 & Follow Up, on phone and computer. Each device asks once to allow Google Drive. No republish needed for task changes. It reads the Today and This week sections of the board.
- 2026-09-26: Melissa asked to save every piece of the setup in Git and in Drive. Guide: `Docs/Setting Up Ellie.md` (Git) and Drive folder `Setting Up Ellie - Every Piece` inside `Ellie Files`. The phone sync refreshes the Drive copy whenever the Git file changes, so edit the Git file and the Drive copy follows at the next sync.
- 2026-09-26 (Melissa): every Google Doc Ellie creates must be saved in the right Drive folder, never loose in My Drive. Rule: a replaced file (Ellie board, Tell Ellie, topic docs) stays wherever Melissa last put it; topic docs live in their topic folder under `Ellie Files`; the setup guide lives in `Setting Up Ellie - Every Piece`; anything else new goes in `Ellie Files`. Melissa moved the `Ellie` board into the `Ellie Setup` folder on 9/26 and the sync now keeps it there.

- 2026-09-26: Wrap (phone sync) now includes a Reminders section (dated open tasks, next 7 days) and an Inbox table (STATUS / FROM / SUBJECT / SUMMARY; NEEDS YOU first). One Haiku call per NEW inbox thread only, cached by thread id in .ellie-state.json. Rescue-from-Trash stays in the 7am briefing email.

## 2026-09-26 (Melissa, evening) - Wrap-up email comes from Git, exactly like the morning digest
- Melissa never received a wrap-up on 9/26. She wants the 4:30pm wrap-up to be ONE email from GitHub Actions, run the same way as the Melissa Daily Briefing: one send, a cron backup if the primary is late, never a second email. This supersedes the earlier "Ellie sends no email" note. The morning phone sync stays silent.
- Do not touch the working phone sync (`phone-sync.yml`, `phone_sync.py`). The wrap-up is its own workflow: `.github/workflows/wrap-up.yml` + `scripts/wrap_up.py` + `scripts/wrapup_email.py` (layout from `routines/email-template.md` section 4).
- Guard: `.last_wrapup_date` in the repo plus a Gmail sent-mail check for the same subject. Backup crons 17:00 and 17:45 UTC skip if it is before 4:45pm ET. Shift +1h UTC in November. Failure sends an ALERT email.
- Known: `phone-sync.yml` defaults `dry_run` to "1", so cron-job.org dispatches (no inputs) run as DRY RUNS and change nothing. Not fixed, because she said not to break what works. Ask her before changing.
- Wrap-up email does not yet reconcile from sent mail or show "Added To Your Calendar".

## 2026-09-26 (Melissa, night) - What she authorized and what was built
- Yes to trashing inbox mail that should go to Trash, using judgment. Built: Haiku flags clearly unimportant bulk mail (promos, product updates, newsletters, webinars, surveys, social notifications) on NEW inbox threads only; rules-protected senders/subjects, real people, recruiters, applications, job alerts, receipts, banking, health, security are never AI-trashed. Everything goes to Gmail Trash (recoverable), never permanently deleted. Listed on the board under "Inbox trash".
- Calendar is a rolling 7 days (board, topic file, wrap-up email), not "until Sunday".
- Everything told to Ellie is filed in Git by the sync commit and mirrored to the Drive topic files: application notes, decisions, prep requests now appear in Job Search / Meetings & Prep files.
- `Handoff.md` (repo root) is rebuilt every sync: read it first in a new chat.
- Board has "Who you are" and "Which file to read". Waiting-on now reads the Memory.md Follow-Ups table too.
- `phone-sync.yml` `dry_run` default is now "0" (cron-job.org calls were dry runs). Concurrency lock added. `__pycache__` untracked.
- Midday: light mode (`LIGHT=1`, GitHub cron 17:00 UTC = 1pm EDT). Exits in seconds with no AI when there are no new captures. cron-job.org 1pm job (POST phone-sync.yml dispatches, body {"ref":"main","inputs":{"light":"1"}}) not created yet.
- Cache: Haiku only for new captures and new inbox threads; seen ids + mail cache in `.ellie-state.json`; topic files rebuilt only when content changed; wrap-up email uses no AI.
- She pauses the cloud routines herself once she sees the Git runs working (never delete).

- 2026-09-26: A dated "remind me" capture now also creates a Google Calendar entry (9am if no time, 30 min, phone popup 10 min before). Calendar and reminder titles are the short subject only; a stated end time is honored. Undated reminders stay on the board.

- 2026-09-26: Ellie also RESCUES important mail from Trash like the morning briefing: Trash last 3 days, interview/application/recruiter/meeting keywords, Haiku decides, high bar (real person or real ATS about a real role or meeting, addressed to her, never bulk/no-reply/unsubscribe). Moves back to inbox, starred and important. Never rescues Do Not Rescue senders or mail Ellie trashed herself; a rescued thread that returns to Trash adds its sender to Do Not Rescue in Memory.md. Board section "Rescued from Trash". Drive docs are updated in place, never trashed. Everything she tells Ellie is saved in Git and mirrored to the Drive topic folders and the Setting Up Ellie folder.
