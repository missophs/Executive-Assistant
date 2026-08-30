# Ellie — Cloud Routines (backup)

These three routines run in Anthropic's cloud, not on this machine. They are configured at
https://claude.ai/code/routines and live only there — **this folder is the only backup of their
prompts.** If a routine is deleted or corrupted, recreate it from the matching file here.

Edits made here do **not** take effect. Editing the live routine is a separate step.

_Backed up: 2026-08-30_

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
- Never book, accept, or decline a calendar invite.
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
