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

## The three routines

| File | Name | Trigger ID | Schedule (ET) | Cron (UTC) |
|---|---|---|---|---|
| `morning-standup.md` | Ellie — Morning Standup | `trig_01GfvypZDLQZRM9F7Kphsnp8` | 7:30 AM daily | `30 11 * * *` |
| `midday-sweep.md` | Ellie — EA Midday | `trig_01FEMRhJNPACVqw4HCRd6SNg` | 1:00 PM daily | `0 17 * * *` |
| `wrap-up.md` | Ellie — Wrap-Up | `trig_012SqPZ7Ui5nPFkko73adieN` | 5:00 PM daily | `0 21 * * *` |

All three: **every day**, seven days a week (changed from weekdays-only on 2026-08-30).

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
