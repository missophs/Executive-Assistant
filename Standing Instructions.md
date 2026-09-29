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

## 2026-09-27 - Combined morning email built (replaces the plan for two separate emails)

Confirmed yesterday: one combined email — Ellie's standup with the 7-day calendar and briefing folded in — with the daily-briefing GitHub email turned off afterward, once proven. Built, not yet live:

- `scripts/morning_briefing.py` + `scripts/morning_briefing_email.py` + `.github/workflows/morning-briefing.yml`. Subject `Ellie - EA - <Weekday>, <Month> <Day>`. Sends once daily via the same guard shape as `wrap-up.yml` (`.last_morning_date` + a Gmail sent-mail check), backup crons 11:30/12:00 UTC (shift +1h in Nov), concurrency group `ellie-morning`.
- Contains: Rescued From Trash, Inbox Triage, Inbox Trash, 7-day Calendar (every day shown, same shape as the old Melissa Daily Briefing), Prepare (interview/appointment checklists built only from the vault — "not in vault" if missing, logic ported from daily-briefing's `generate_briefing.py`), Draft Replies — Awaiting Your OK (proposes only, asks first with a literal `Tell Ellie: draft <n>` line, never drafts or sends on its own — actually creating the draft still happens in a chat session, through `/humanize`, same as today), Top 3 & Follow Up (merged, not "Gone Quiet"), and the `/ea:` command table.
- **Not touched:** `missophs/daily-briefing` (still sends the Melissa Daily Briefing every morning) and the old cloud "Ellie — Morning Standup" trigger. Both keep running until the new email is proven over a few days, per the plan above — then daily-briefing gets turned off. This session did not disable anything.
- **Flag:** repo docs do not confirm the old cloud "Ellie — Morning Standup" trigger (`trig_01GfvypZDLQZRM9F7Kphsnp8`) is actually disabled — only that pausing it (never deleting) was the plan, and the most recent Memory.md entries show the phone-sync cloud routine was still confirmed live well after its Git replacement worked. If Standup is still enabled, expect up to three separate morning emails (old Standup + this new one + the Daily Briefing) until she disables `trig_01GfvypZDLQZRM9F7Kphsnp8` herself.
- **cron-job.org job Melissa (or a future session) still needs to create**, same account/pattern as the existing wrap-up/phone-sync jobs:
  - URL: `https://api.github.com/repos/missophs/Executive-Assistant/actions/workflows/morning-briefing.yml/dispatches`
  - Method: `POST`
  - Headers: `Authorization: Bearer <the same GitHub token already used for the wrap-up/phone-sync cron-job.org jobs>`, `Accept: application/vnd.github+json`
  - Body: `{"ref":"main"}`
  - Schedule: 7:30 AM America/New_York, daily (cron-job.org handles DST)
  - Test with a manual "Run now" first; the workflow's own guard will no-op a second same-day dispatch, so an extra test run is safe.

## 2026-09-27 (evening) - Midday email built, Waiting On 5-day cutoff, cloud routines being paused
- Melissa: nothing should run as a Claude cloud routine — everything runs from git + cron (cron-job.org primary, GitHub Actions native schedule as backup), matching the pattern already proven for morning-briefing.yml/wrap-up.yml/phone-sync.yml. She is pausing the three duplicate cloud routines (Phone Sync AM/PM, Midday Check — see routines/README.md 2026-09-27 note) herself once she's confirmed the git versions hold up; this session could not disable them (created via the web API, not by an agent).
- Midday 1pm conditional email built into `scripts/phone_sync.py` (LIGHT mode) + new `scripts/midday_email.py` — see the gap note above, now resolved.
- Melissa: Waiting On items older than 5 days should stop being shown — not deleted from Memory.md's Follow-Ups table (that stays the record), just dropped from what's reported. Applied to `dashboard.html` (STALE_DAYS now 5, items past it are filtered out, not just flagged), `scripts/wrap_up.py`'s Waiting On email section, and `scripts/phone_sync.py`'s phone-board Waiting On section (`WAITING_MAX_DAYS = 5` in both).

## 2026-09-27 (later) - Cron timings finalized, phone capture confirmed working, Command Center findings

- Melissa's final cron spec, built in cron-job.org: morning 7:00am ET primary + 7:30am backup (job 8524112 "Ellie Morning Briefing Trigger", created, enabled, points at morning-briefing.yml); midday 1:00pm ET only, phone-sync.yml with light=1 (job 8517937, already correctly timed); evening 4:30pm ET primary (job 8517934, retimed from 4:45pm) + 5:00pm ET backup (job 8517938, retimed from 5:15pm), both wrap-up.yml. Daily Briefing backup job 8219170 retimed 7:03am -> 7:30am.
- ~~Gap, not yet built: the 1pm run is meant to send an email only if something new happened since the last run, otherwise stay silent.~~ Built 2026-09-27: `scripts/midday_email.py` + `phone_sync.py` LIGHT-mode hook. Sends the Midday email (routines/email-template.md section 4: Filed Your Notes, Marked Done, Needs Your Call) only when one of those has content; silent otherwise. Same send-once guard pattern as wrap_up.py (Gmail `in:sent` subject check). Runs from git + cron only — Melissa is pausing the cloud routines herself once this is proven (see routines/README.md).
- Confirmed the actual sends/syncs run on GitHub Actions + cron-job.org only, no Claude Code session cost. The one genuine Claude cloud cost is the Command Center dashboard refresh routine (trig_01YWcsQWdhbmQRGMTy5Yy8zG, twice daily, currently Sonnet). Melissa wants this moved off Claude entirely (not just to a cheaper model) - not yet built.
- Command Center is already color-coded in its persisted HTML/CSS (dashboard.html) - carried forward on every republish, no fix was needed.
- Command Center was never built to show inbox/emails - by design it only shows live calendar and Top 3 & Follow Up from the Ellie doc. Not a bug. A real feature add if Melissa wants inbox on the dashboard too - not scoped.
- Old cloud "Standup" trigger (trig_01GfvypZDLQZRM9F7Kphsnp8) confirmed safe: already renamed/repurposed to "Phone Sync AM", fires 6:30am silently, never sends email. Wasteful duplicate of the free GitHub phone sync at the same time, not a risk. She will pause it herself once the Git version is proven.
- Confirmed the "tell Ellie on my phone" capture pipeline works end to end: Melissa's iOS Shortcut dictates and self-emails melissaw212@gmail.com with subject "Tell Ellie" (one of three documented capture paths - the others are writing in the Tell Ellie doc, and talking to Ellie directly in chat). 5 captures sent 2026-09-27 10:30-10:39am ET, landed correctly. She reported being cut off mid-dictation; diagnosed as the Shortcut's "Dictate text" action being set to stop listening after a pause; fixed by setting Stop Listening to "On Tap" in the Shortcut.
- Corrected a doc mismatch: the old Standup trigger fires at 6:30am, not 7:30am as routines/README.md and the Tell Ellie doc header still say. Not yet corrected in those files.
- GitHub write access from Claude Code chat sessions was down all day: the fine-grained personal access token behind the local github connection had Actions (read/write) and Metadata (read) but was missing Contents permission entirely. Fixed 2026-09-27 by adding Contents: Read and write to that same token ("Ellie Write Access") on GitHub. This entry is the first successful write since the fix.

## 2026-09-27 (incident) - Accidental overwrite of this file, and the permanent fix

- Right after GitHub write access was restored, the first write to this file replaced its entire contents with only the new dated entry, briefly deleting all prior history (everything from 2026-09-26 onward). Caught immediately (before Melissa saw it) by comparing file size, and fixed within the same minute by re-reading the pre-write content and rewriting the full file (all history + the new entry) in a second commit.
- Cause: passing only the new section as the file's content to the GitHub write tool, instead of the full file content with the addition appended. That tool replaces the whole file body; it does not append.
- Melissa's instruction, permanent: never do this again, in Git or in Google Drive. Rule now saved in memory (`feedback-git-append-not-overwrite`, alongside the existing `feedback-no-replace-drive-docs` rule): every future write to an existing file in this vault reads the full current content and sha first, then writes old content + new content together. Never write just the addition.

## 2026-09-27 (later still) - Richer morning email: gap closed, not just flagged

- Melissa: the old `missophs/daily-briefing` email has Executive Summary, due-date Action Required cards, calendar conflict detection, RSVP-needed flags, and an Email Triage Quick List table that `morning_briefing.py` did not yet have — she does not want a "gap disclosed" answer, she wants it built before she turns the old email off. Built and pushed 2026-09-27:
  - **Executive Summary** box (new, top of email): top priority from Today's board, count of inbox items needing her, longest open Waiting-On wait, RSVP-needed count, conflict count — or "Nothing urgent. Light day." when none apply.
  - **Action Required**: every board item (Today/This Week/Backlog) with an explicit `due YYYY-MM-DD`, sorted by due date, capped at 12 — not just the curated Top 3. Bar color: red if due today or overdue, amber within 3 days, blue otherwise.
  - **Calendar conflict detection**: timed events on the same day that overlap are both flagged "CONFLICT" in red in the Calendar — Next 7 Days box.
  - **RSVP-needed flags**: any event where she's an attendee with `responseStatus: needsAction` is flagged "RSVP NEEDED" in amber next to it, and counted in the Executive Summary.
  - **Email Triage Quick List** rebuilt as an actual HTML table (From / Subject / Note columns, NEEDS YOU rows tinted) instead of a plain stacked list.
  - Files: `scripts/morning_briefing.py` (calendar overlap/RSVP computation, `action_items` due-date extraction), `scripts/morning_briefing_email.py` (`_triage_rows`, Executive Summary, Action Required box, `_time` conflict/RSVP tags). Self-test in `morning_briefing_email.py` passes (`python3 morning_briefing_email.py` → `ok`), `morning_briefing.py` parses clean.
  - Nothing about the daily-briefing repo or its trigger was touched — still her call when to turn it off, now with the feature gap closed first.

## 2026-09-27 (night) - Live verification pass: one real bug caught, everything else confirmed working

Melissa: don't just tell her things work, prove it, and if something breaks while proving it, fix it properly rather than reverting ("never break, refactor it"). Ran real GitHub Actions triggers instead of reading code, and read the actual run logs:

- **Phone sync push-race fix**: confirmed live. Triggered a real run after the retry-loop fix landed — succeeded end to end (build, commit, pull-rebase, push). All three daily slots (6:30am, 1pm, 4:30pm ET) had already run successfully today via cron-job.org before this check.
- **Wrap-up sends real email**: confirmed. The actual send happened today at 4:30pm ET via cron-job.org's `workflow_dispatch` (commit `834bfd6`, "Build and send wrap-up" step succeeded). The two earlier GitHub-native schedule firings and the 5pm backup correctly stayed silent — the send-once guard did its job, no duplicate emails.
- **Morning briefing — real bug found and fixed**: `morning-briefing.yml` had never actually run before (built too late in the day, 10:04am ET, to catch its own 7:00/7:30am triggers). Test-firing it live crashed: `ValueError: too many values to unpack (expected 2)` in the Prepare section of `morning_briefing.py` — the calendar conflict/RSVP work earlier the same day widened each event to a 4-value tuple `(when, what, conflict, rsvp)`, but one loop (line 212, building `prepare_items`) still unpacked 2. Read the actual failure log, fixed the unpacking (`for _, what, _, _ in day["events"]:`), pushed, re-triggered — second run succeeded clean. First real (non-dry) send is still untested: next chance is tomorrow's ~7am ET trigger.
- Nothing else flagged as broken. Ellie Commands table, the Waiting-On removal build, and the richer morning email (Executive Summary/Action Required/conflict+RSVP flags/triage table) all still confirmed correct from the prior two entries.

## 2026-09-27 (night) - "What did we do yesterday on X" answers from the topic folders, always

- Melissa: when she asks what happened on a topic (e.g. "what did we do yesterday on the interview, was it sent") Ellie must be able to point to the actual record and pull it — Applications.md/Memory.md for job search, Task Board.md for open items, and the matching Drive "Where we left off - <Topic>" doc (Job Search, Meetings & Prep, Reminders & Tasks, Saved Links, Ellie Setup, Calendar — all under `Ellie Files`, created 9/26) — not say it can't be found. Confirmed this already works: e.g. LRN/Ashley Fredericks (screen held 9/25, thank-you sent same day 4:49pm ET, verified against Gmail) and Conduit Health (closing reply drafted, confirmed still NOT sent, sitting in Gmail Drafts) are both answerable straight from the vault today.
- If a future topic doesn't fit one of the six existing folders, create a new one under `Ellie Files` rather than forcing it into an ill-fitting folder or declining. Melissa: "if we need to create more, we will."

## 2026-09-27 (night, final) - Complete bug list: both fixed, both verified, zero open

Melissa asked point-blank whether every bug was actually fixed, after getting two failure-notification emails tonight (GitHub's own + the workflow's own alert). Confirmed: both emails were the SAME single event, already accounted for below. This is the complete list — nothing else broke tonight, checked against all three workflows' live run history at the time of writing:

1. **`phone-sync.yml` git push had no retry.** Root cause of the original failure email that started this session. Plain `git push` with no fallback meant any push race (the three then-still-live duplicate cloud routines writing to `main` on the same schedule) failed the run outright. Fixed with a pull-rebase-and-retry loop. Verified live afterward with a real triggered run — succeeded clean.
2. **`morning_briefing.py` Prepare section crashed (`ValueError: too many values to unpack`).** The calendar conflict/RSVP feature widened each event to a 4-value tuple; one loop still expected 2. This was `morning-briefing.yml`'s very first-ever run (it had never fired before — built too late in the day to catch its own 7am trigger), so the bug had never been exercised until that test. Fixed the unpacking, re-ran live — succeeded clean. Both failure-notification emails Melissa received tonight (GitHub's run-failed email and the workflow's own Gmail alert) were for this one event.

Status checked at time of writing: `morning-briefing.yml` 2 runs total (1 failed on bug #2, 1 succeeded after the fix, nothing since); `phone-sync.yml` latest run succeeded; `wrap-up.yml` all green, sent for real today 4:30pm ET. Zero open failures across all three. Only remaining unknown: `morning-briefing.yml`'s first real (non-dry) send, due tomorrow ~7am ET.

## 2026-09-28 - Midday landed late, calendar formatting, priorities pruning, wrap-up retimed to 5-5:30pm

Melissa reported the midday email arrived after 6pm ET instead of 1pm, the calendar section wasn't visually separated by day, the "Current priorities" box was stale/truncated, and wrap-up should move from 4:30/4:45pm to between 5:00 and 5:30pm ET. Root cause on timing: GitHub's own schedule crons (not cron-job.org, which fires on time) get delayed hardest exactly on the hour/half-hour — today's on-the-hour backups fired 5+ hours late, which is what actually sent the midday email that late (the on-time 1pm run found nothing to report and correctly stayed silent).

- **Calendar — Next 7 days** (Ellie board): now grouped by day, each day color-coded with a left border and separated by a horizontal rule, instead of one flat bullet list. `scripts/phone_sync.py`, new `cal_html()`.
- **Current priorities**: now filtered to bullets whose most recent mentioned date is within 5 days (only go back 5 days) instead of just the first 3 bullets positionally. New `_priority_fresh()` in `phone_sync.py`. Conduit Health content removed from `Memory.md`'s Current Priorities (both the standalone bullet and the clause inside the master summary bullet) — it's now moot and over 5 days stale regardless.
- **Midday links**: link captures (bare URLs, e.g. saved LinkedIn job links) are still filed to `Memory.md`'s Saved Links for the record, but no longer shown in the midday email — Haiku has no title to give them (just echoes the raw URL back), so they were pure noise. Add a word or two (company/role) when sending yourself a link if you want it identifiable later. The 4 bare links already sent today were removed from Saved Links.
- **Wrap-up retimed to 5:00-5:30pm ET** (was 4:30/4:45pm): cron-job.org's "Ellie Wrap-Up Email 4:30pm" job retimed to 5:03pm ET (renamed to match); the existing 5:00pm backup job untouched. `wrap-up.yml`'s GitHub-native backup crons moved off round numbers to 5:04/5:17/5:29pm ET and its "too early" guard moved from 4:45pm to 5:00pm.
- **Midday crons also moved off round numbers** for the same GitHub-delay reason: `phone-sync.yml`'s three daily crons shifted a few minutes off the hour/half-hour (6:34am/1:04pm/4:34pm ET instead of 6:30/1:00/4:30). cron-job.org's own on-time triggers (6:30am, 1pm, 4:30pm) were not touched — they already fire on time.
- Morning briefing was explicitly left untouched this round (Melissa: "right now we don't need to touch the morning briefing") — noted but not acted on: cron-job.org's morning trigger is currently set to 7:00am ET, not the 7:30am the workflow's own comments assume.
- All changes pushed to `missophs/Executive-Assistant` main: commits `018dba6` and `89564c1`.

## 2026-09-29 — Ellie emails match the Melissa Daily Briefing design (Melissa)
- Ellie replaces Melissa's Daily Briefing once Ellie is confirmed issue-free; Melissa stops the old one herself.
- All Ellie emails (morning, midday, wrap-up) share the briefing's design: icon section bars, greeting header with stat tiles, cards, tables — **keep Ellie's purple colors**. Shared file: `scripts/ellie_ui.py`.
- Morning email carries every briefing section: Inbox Triage, Executive Summary (3 cards), Action Required, Draft Replies, Full 7-Day Calendar, Prepare (blue TODAY/TOMORROW cards), Job Search & Interview Pipeline, Full Email Review by Category, Trash Review, Promo, Newsletters, Email Accounting, Dashboard, Action Items, Top 3 & Follow Up.
- **No email triage at night** (costs money). Wrap-up and midday get the design only, zero new AI.
- Email review cap stays at **100** (Melissa: if 200 costs more, leave it at 100). Duplicate calendar entries (same start + title) are merged.
- Prep from the phone: "prep for interview with X tomorrow" builds `Meetings/<date> <Company> prep.md` from the vault + calendar only (no AI, "not in vault" where unknown). Runs **only when she asks**.
- Company history / About Me / STAR questions prep: approved as **on-demand only** ("prep for X"). Not built yet. Source for her background: iCloud Drive (resume/profile PDFs; folder `Melissa res/2025/2026/cai` exists but is empty). She said NOT to use "Melissa Profile".
- Live on `missophs/Executive-Assistant` main (merge commit 90a4c7a). Dry run on real data passed 9/29: 100 emails, 24 pipeline roles, ~19k in / 4k out Haiku tokens. First real send: 9/30 morning.

## 2026-09-29 (later): send-a-document command and CAI prep files
- Melissa wants to tell Ellie from her phone to **email her a Google Drive document**. Built: capture `send CAI talking points` / `email me the X notes` (Mail app subject `Tell Ellie: send ...` or the Tell Ellie Drive doc). Ellie searches Drive by name, sends to melissaw212@gmail.com only, subject `Ellie - Doc - <name>`. Google Docs arrive as the email body; other files (docx, pdf, up to 15 MB) as attachments. Read-only: creates and replaces nothing.
- No match: Ellie emails a list of the 10 most recent Drive docs (`Ellie - Doc - which one?`) so she can text back a name. She does NOT want "Needs Your Call" lines for this. iCloud is not readable by Ellie; only Drive files work.
- Live on main (commits 63b2149, 6811b71). First real run 9/29: the CAI talking points email arrived. Not yet tested: the "which one?" no-match list.
- CAI prep files (Drive: Ellie Files / Meetings & Prep, and git `Meetings/`): "CAI talking points - Wed 9-30 2:30pm" (Google Doc id 1paRd5MkT_Hz6rGhSMxW_bZz2X9eKD7CyEnjIKmeFZ2w) and "CAI STAR questions and resume examples - Wed 9-30 2:30pm" (Google Doc id 19iYvovV1X917IXTGhhu1b6j4V-rFJFe2gfeO_tRv-Tw; git `Meetings/2026-09-30 CAI STAR questions.md`, commit f0722d1). Built from resume "MELISSA A WEISS926" and the pasted job description only. [ADD] lines mark where she must supply a real detail; nothing invented.
- Rule reaffirmed: do not delete anything; new files or appends only.
