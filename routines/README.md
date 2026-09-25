# Ellie — Cloud Routines (live source)

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
| `midday-sweep.md` | Ellie — Midday Sweep | `trig_01FEMRhJNPACVqw4HCRd6SNg` | 1:00 PM daily | `0 17 * * *` |
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
