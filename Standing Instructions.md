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
