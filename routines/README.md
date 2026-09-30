# Ellie — Cloud Routines (live source)

## Where things are

Start here when Melissa says "where did we leave off" or "pick it up from here".

| What | Where |
|---|---|
| Open tasks, follow-ups, Waiting On | `Task Board.md` |
| Priorities, people, decisions, ideas, saved links, seen cache | `Memory.md` |
| Job pipeline | `Applications.md` |
| Raw notes and daily logs | `Scratch Pad.md`, `Daily Notes/` |
| Meeting notes | `Meetings/` |
| What we changed about Ellie herself, and what is still untested | the Changelog at the bottom of this file |
| Phone captures not yet filed | Google Drive file "Tell Ellie"; self-sent Gmail (`in:anywhere newer_than:2d from:melissaw212@gmail.com to:melissaw212@gmail.com`) |
| The phone board Ellie reads | Google Drive file "Ellie" (rewritten by the routines) |
| Dashboard | `dashboard.html`, published as the artifact `ef023dc5-7573-4ac8-845f-ba8448315a5b` (private, "EA" on her phone) |
| Routine instructions and email look | `routines/*.md`, `routines/email-template.md` |

Rule: a thought is only findable if it was written down. If she describes an idea in chat, add it to `Memory.md` (or `Scratch Pad.md`) before the session ends.


These three routines run in Anthropic's cloud, not on this machine. **These files ARE the routines.**

As of 2026-09-04 each cloud trigger holds only a short loader that says "read
`routines/<name>.md` from the repo and follow it exactly." All the real instructions live here.
Edit the file, push, and the next run picks it up — no trigger update needed.

Before this change the full prompt was pasted into the trigger and these files were only a backup,
so the two drifted apart. Do not go back to that.

Two consequences worth knowing:
- **A change is only live once it is pushed to GitHub.** The cloud clones the repo at run time.
  An uncommitted edit on this machine does nothing.
- **Do not rename or delete these files.** If the loader cannot read its file it sends Melissa a
  `Ellie - routine file missing` email and stops, rather than improvising.

_Last updated: 2026-09-04_

## The three routines — STALE, see 2026-09-27 note below

| File | Name | Trigger ID | Schedule (ET) | Cron (UTC) |
|---|---|---|---|---|
| `morning-standup.md` | Ellie — Morning Standup | `trig_01GfvypZDLQZRM9F7Kphsnp8` | 7:30 AM daily | `30 11 * * *` |
| `midday-sweep.md` | Ellie — EA Midday | `trig_01FEMRhJNPACVqw4HCRd6SNg` | 1:00 PM daily | `0 17 * * *` |
| `wrap-up.md` | Ellie — Wrap-Up | `trig_012SqPZ7Ui5nPFkko73adieN` | 5:00 PM daily | `0 21 * * *` |

All three: **every day**, seven days a week (changed from weekdays-only on 2026-08-30).

**2026-09-27 — table above is out of date.** These same three trigger IDs are now live under
different names/schedules/prompts, repurposed at some point without this file being updated:
`trig_01GfvypZDLQZRM9F7Kphsnp8` is now **Ellie — Phone Sync AM** (6:30am ET, `30 10 * * *`,
runs `routines/phone-sync.md`); `trig_01FEMRhJNPACVqw4HCRd6SNg` is now **Ellie — Midday Check
(brief)** (1pm ET, `0 17 * * *`, runs `routines/midday-light.md`); `trig_012SqPZ7Ui5nPFkko73adieN`
is now **Ellie — Phone Sync PM** (4:30pm ET, `30 20 * * *`, runs `routines/phone-sync.md`). All
three duplicate `.github/workflows/phone-sync.yml`'s cron slots exactly and were racing against
it on live Gmail/Calendar/git writes — likely cause of the 2026-09-27 4:30pm push failure. Per
the standing instruction below ("pause the cloud routine once the Git version is proven, never
delete") Melissa is pausing all three by hand — this session could not disable them itself (they
were created via the web API, not by an agent; only she or their own session can toggle them).
`midday-sweep.md` and `wrap-up.md` in this folder are now orphaned — no live trigger runs them.

## Shared configuration

- **Model:** `claude-sonnet-5`
- **Environment:** `env_01HWgKTueYM8YBsjWL25jF3D`
- **Source repo:** `https://github.com/missophs/Executive-Assistant`
- **Allowed tools:** `Bash`, `Read`, `Write`, `Edit`, `Glob`, `Grep`

## Connectors attached

| Connector | UUID | URL | Used by |
|---|---|---|---|
| Gmail | `4dc3c0a1-e385-4ef1-bedf-7cfac77411e9` | `https://gmailmcp.googleapis.com/mcp/v1` | all three |
| Google-Calendar | `083868ca-e8e1-4cb4-83a6-921fd09dc003` | `https://calendarmcp.googleapis.com/mcp/v1` | standup, wrap-up |
| Google-Drive | `780c2173-aa30-4e5c-ac3c-cace4c75d706` | `https://drivemcp.googleapis.com/mcp/v1` | all three |

Note: the Midday Sweep does not have Calendar attached. It does not need it.

## Standing safety rules (present in all three prompts — do not remove)

- Never send, reply to, or forward mail to anyone except the one status email to Melissa.
  Replies to other people are **drafts only** (`create_draft`, never `send_message` or `reply`).
- Never accept or decline a calendar invite. The only events Ellie may create are ones Melissa explicitly asked for ("remind me I have the vet Thursday"), on her primary calendar with no attendees; never edit or delete events.
- Never permanently delete or trash her mail. Rescuing from Trash is allowed; trashing is not.
- The only Drive files that may be trashed are the previous `Ellie` board and the previous
  `Tell Ellie` note.
- Never invent a company, person, role, date, or number.
- Drafts go out under her name — never signed as Ellie.

## Two API quirks the prompts work around

1. **Gmail:** `untrash_message` and `untrash_thread` return "The caller does not have permission."
   The working way to rescue mail from Trash is `label_thread` adding `["INBOX","STARRED","IMPORTANT"]`.
2. **Google Drive:** `update_file` only changes title and parent — it **cannot** rewrite a file's
   contents. To refresh a file you must `create_file` a new one with the same title, then
   `trash_file` the old id.

## How to restore a routine

Ask Claude Code: "recreate the Ellie <name> routine from `routines/<file>.md`" and give it the
schedule and connectors from the tables above. It uses the `RemoteTrigger` tool with
`action: "create"`.

---

## Changelog — 2026-09-25 (Ellie - EA)

**Why the standup arrived twice on 9/25:** the Gmail send tool does not run shell substitution, so the first send went out as the literal text `$(cat /tmp/.../standup.html)` and a second, real send followed. Fixed with a SEND ONCE rule in every routine (literal HTML body only; search `in:sent` for the subject before sending; never resend after a success).

**Routines (`routines/*.md`)**
- Seen cache: `## Seen Cache` in `Memory.md` (`<id> | <latest-message-date> | <what was done>`), so already-handled mail is skipped unless newer. Pruned after 7 days.
- Recall: the phone board tells the chat to check Gmail self-sends and the Drive file "Tell Ellie" when asked "where did we leave off".
- Interview prep box in the standup (vault and Gmail only; "not in vault" if missing; never invent).
- Wrap-up STEP 3b reads tomorrow's calendar for the `Tomorrow` box; only says "Calendar is clear." if `list_events` returned nothing.
- Calendar captures: "Ellie remind me I have X on <date>" creates an event on the primary calendar (America/New_York, no attendees, no invites, create-only). Needs a clear date; otherwise asks under "Needs Your Call". Reported under "Added To Your Calendar". Never accepts or declines invites.
- Waiting-On captures: "Nasreen replied", "stop waiting on Chime" removes the item from `Task Board.md` Waiting On and the Memory follow-ups table, logs "No longer waiting on X" under Done.
- Email subjects renamed: `Ellie - EA Morning - <Weekday>, <Month> <Day>`, `Ellie - EA Midday - …`, `Ellie - EA Wrap-Up - …`.
- Email palette matches the dashboard: mastheads Standup `#6D21C9`, Midday `#D6249E`, Wrap-Up `#3B1B8F` (each with a gradient and a solid fallback), brighter accent colours, page background `#F3F1FB`.
- Midday sweep (1pm) is **paused** by the user to save tokens. Captures wait for the 7:30am or 5pm run.

**Dashboard (`dashboard.html`, published to the artifact `ef023dc5-7573-4ac8-845f-ba8448315a5b`, pinned as "EA" on her phone)**
- Palette is the purple/pink/orange one; title "Ellie - EA". The Waiting On and People panels were removed.
- Calendar panel reads her own Google Calendar live at open time through the artifact `mcp` capability (server "Google Calendar", tool `list_events`, refresh every 5 min, no tokens). Falls back to the calendar baked in by the last `/dashboard`.
- Tasks, follow-ups and priorities are still copied from the vault only when `/dashboard` runs (after the 7:30am and 5pm routines).
- Sharing must stay "Only people invited". Pages on this private repo was rejected: it would publish the job-search data publicly.
- The live-calendar version shows each viewer their own calendar, so it is for her only.

**Still untested (no routine has run since these changes):** send-once guard, new email look, calendar capture, waiting-on capture, interview prep, seen cache. First real check: the 9/26 7:30am email should be a single email in the new colours and list "Doctor's appointment, Mon 9/28, 1:00–5:30 PM" under Added To Your Calendar (captured 9/25 7:00 PM ET). Event "Elle" on 9/30 9:30 AM was renamed "Elle-Hair" by chat.

**Chat vs routines:** in a chat session with Google Calendar connected, events can be read, added and renamed immediately. Routine runs use their own connection and act only at their scheduled times. Events with guests always need her yes first in chat.

## Changelog — 2026-09-26 (phone + wrap)
- `phone-sync.md`: added DAILY WRAP on the phone board (what happened today, calendar for the rest of the week, read-only inbox triage, prep pointers), `Prep:` captures that write `Meetings/<date> <title>.md`, and fixed the `Tell Ellie` placeholder times (6:30am / 4:30pm ET).
- New `improve.md`: on-demand vault audit, run via the "Ellie Improve" routine (no schedule).
- Correction: Phone Sync AM/PM and Ellie Improve are loaders for their repo file; the old email routines' triggers were not.
- Wrap-up inbox triage now trashes per `routines/trash-rules.md` (copied from the briefing lists; refresh if they change). Trash only, never permanent delete, every trashed thread listed on the board.
- Standing Instructions.md (repo root) holds every instruction Melissa has given; Ellie appends new ones. Dashboard: whole-week calendar, date first, color-coded, past events hidden, check-boxes removed (close by telling Ellie).

- 2026-09-26 (late): phone_sync.py now rescues important mail from Trash (Haiku, high bar, Do Not Rescue learned, cached in .ellie-state.json), updates Drive docs in place instead of trashing old copies, turns dated "remind me" into 30-minute calendar entries with a popup. cron-job.org wrap-up 4:45pm + 5:15pm backup and midday 1pm light sync created.

## Changelog — 2026-09-27 (single combined morning email — build)

Built `scripts/morning_briefing.py` + `scripts/morning_briefing_email.py` + `.github/workflows/morning-briefing.yml` per Melissa's confirmed plan (combined email, daily-briefing turned off only once proven). This is meant to eventually replace both the "Melissa Daily Briefing" email (missophs/daily-briefing) and the old cloud "Ellie — Morning Standup" trigger — **neither was touched or disabled**; both keep running until this is proven over a few days.

- Subject `Ellie - EA - <Weekday>, <Month> <Day>` (not "Melissa Daily Briefing", not "Standup"). Masthead reuses the Standup purple (`#6D21C9`), solid only, no gradient (matches wrap_up.py's proven pattern, not the gradient the template text describes — Gmail strips it).
- Sections, in order: Rescued From Trash, Inbox Triage, Inbox Trash, Calendar — Next 7 Days (every day shown, even empty ones — shape ported from daily-briefing's `generate_briefing.py`), Prepare (checklists built only from `Applications.md`/`Memory.md`/`Meetings/*.md`, "not in vault" fallback, logic ported from the same file's Prepare/Interview-Prep approach), Draft Replies — Awaiting Your OK (proposes only, never drafts or sends; tells her the literal `Tell Ellie: draft <n>` reply), Top 3 & Follow Up (merged, "Gone Quiet" not used), Ellie Commands (`/ea:*` table ported from daily-briefing, `/ea:inbox` dropped per Standing Instructions).
- Send-once guard: `.last_morning_date` file (workflow-level, same shape as `.last_wrapup_date`/wrap-up.yml) plus a Gmail `in:sent` subject search in the script itself (same as wrap_up.py). Concurrency group `ellie-morning`. Backup crons 11:30 and 12:00 UTC, skip before 7:45am ET unless it's the on-time `workflow_dispatch` (cron-job.org).
- Own cache file `.morning-briefing-state.json` (thread-triage cache + rescue-judged ids), separate from `.ellie-state.json` on purpose — phone_sync.py and this workflow can both write to the repo without racing on the same JSON file.
- Inbox triage and Trash rescue duplicate phone_sync.py's approach (same `routines/trash-rules.md`, same `## Do Not Rescue` list, same Haiku high-bar rescue prompt) rather than sharing code, matching this repo's existing convention of each script owning its own copy (wrap_up.py/wrapup_email.py do the same). This email never trashes anything itself — trashing stays with phone_sync.py/wrap-up; it only reports and rescues.
- Tested with a real vault dry run (`DRY_RUN=1`, no live Gmail/Calendar — the Google API layer was faked to run the actual vault-parsing/Prepare/Calendar/HTML-assembly logic against this repo's real Task Board.md/Applications.md/Memory.md; a true DRY_RUN GitHub Actions run against live Gmail/Calendar still needs to happen once the secrets run in CI, same rollout order phone_sync.py and wrap_up.py followed). `scripts/morning_briefing_email.py` has its own runnable self-test (`python scripts/morning_briefing_email.py`), same pattern as `wrapup_email.py`.
- cron-job.org job still needs to be created by Melissa (or a future session) — see the "one email" entry in `Standing Instructions.md` for the exact job spec. Not wired up by this session.

**Flag — likely still-live old cloud trigger:** the old "Ellie — Morning Standup" Claude cloud trigger (`trig_01GfvypZDLQZRM9F7Kphsnp8`, `30 11 * * *` UTC = 7:30am ET) is a fully working routine (`routines/morning-standup.md`) that sends its own email, subject `Ellie - EA Morning - <Weekday>, <Month> <Day>`, with its own send-once guard. Nothing in this repo's docs confirms it was ever actually disabled — Standing Instructions.md says only that it's meant to be paused once proven, and the most recent Memory.md entries (9/26 evening, 9/27 morning) show the *phone-sync* cloud routine was still confirmed live well after its Git replacement was working, with no changelog entry anywhere recording an actual pause action for Standup, Midday, or Wrap-Up either. If `trig_01GfvypZDLQZRM9F7Kphsnp8` is still enabled, Melissa will get three separate emails some mornings (old Standup + new "Ellie - EA" + Melissa Daily Briefing) until she disables it herself — this session did not attempt to touch it.

## 2026-09-29 changelog
- Added `scripts/ellie_ui.py` (shared section bars, icons, header tiles). `morning_briefing_email.py`, `wrapup_email.py`, `midday_email.py` now import it.
- `morning_briefing.py` reviews all mail from the last day (max 100, inbox/archive/Trash/Spam), sorts each into a category with Haiku (cache `.morning-briefing-state.json` now stores 5 fields), merges duplicate calendar entries, builds the job pipeline from Applications.md.
- `prep_doc.py` + `phone_sync.py` prep branch: "prep for X" capture -> `Meetings/` prep doc (vault + calendar only).
- Rollback: `git revert -m 1 90a4c7a && git push origin main`.

## 2026-09-29 changelog (phone: send a Drive doc)
- `phone_sync.py`: new capture kind `send`. Finds a Drive file by name words (Google Doc -> HTML email body, other files <=15 MB -> attachment), emails it to Melissa only, subject `Ellie - Doc - <name>`. No match -> emails the 10 most recent Drive docs (`Ellie - Doc - which one?`). Dry runs send nothing. Drive scope was already full `drive`.
- Known: a real run on 9/29 hit a transient Google read timeout writing the "Ellie" status doc (existing code, `replace_doc`); the re-run succeeded, so one CAI doc email was sent twice.
- Rollback: revert commits 6811b71 and 63b2149.

## 2026-09-30 changelog (Ellie matches the Melissa Daily Briefing)
- New `scripts/briefing_cards.py`: Inbox Triage list (with AUTO-TRASHED and TRASH counts), Executive Summary as three cards (Biggest Risk / Job Search / Calendar), Action Required cards (Source, Why it matters, Next step, Due) for RSVP Pending, declined invites, and financial/security/medical mail.
- Wired into the morning email (`morning_briefing_email.py`, `morning_briefing.py`) and the wrap-up (`wrapup_email.py`, `wrap_up.py`). `phone_sync.py` saves `state["wrap"]`; the morning run saves `state["review"]` in `.morning-briefing-state.json`; the wrap-up reads both.
- Morning run now rescues financial/security/medical/order mail from Trash itself (never phishing, never Do Not Rescue senders, never the same thread twice) and writes a per-email next step and due date.
- Rollback: revert commits c899826 and the follow-up "Ellie auto-rescues financial/security/medical mail" commit.
- 2026-09-30 (later): calendar now in the Daily Briefing layout (`briefing_cards.rich_events` + `calendar_rows`: day banner, time range, status Confirmed/DECLINED/RSVP PENDING, host, attendees, Zoom link/ID/password, Prep line, named red conflict). Draft Replies in the Daily Briefing look (`draft_rows`). Morning caches Prep lines (one Haiku call, event's own text only) and the draft list in `.morning-briefing-state.json`; wrap-up reuses both. Rollback: revert the commit titled "Calendar and Draft Replies in Daily Briefing layout".
- 2026-09-30 (later): calendar Prep and warning lines now come from one Sonnet call per change (sees the week, open pipeline, last day's mail), cached per event in .morning-briefing-state.json, to match the Daily Briefing. Trash Review unchanged (Melissa: fine). Rollback: revert the commit titled "Prep and warnings from full-context call".
