# Executive Assistant

A file-based EA that runs in Claude Code. Three commands, one vault, no app to log into.

The premise: I want to have ideas and execute on them. The sorting, pruning, and reorganizing in between is friction. This absorbs it.

## Daily Rhythm

| When | Command | What it does |
|---|---|---|
| Morning | `/start` | Reads the board, memory, and calendar. Gives a ranked plan and asks what to clear. |
| Throughout | `/sync` | Empties the Scratch Pad, summarizes new meeting notes, updates the board and daily note. |
| End of day | `/wrap-up` | Final sweep, day summary, writes memory so tomorrow starts warm. |

## Files

```
CLAUDE.md          EA persona — loaded automatically every session
Task Board.md      Open work. Single source of truth.
Scratch Pad.md     Raw inbox. Dump here; /sync empties it.
Meetings/          Drop transcripts here. /sync summarizes them.
Daily Notes/       One YYYY-MM-DD.md per day. The permanent record.
.claude/memory.md  Rolling context between sessions.
```

## Setup (once)

1. **Open the folder in Claude Code.** In Terminal:
   ```
   cd ~/Executive-Assistant
   claude
   ```
2. **Say yes to the trust dialog.** It appears the first time only. Until you do, the permissions in `.claude/settings.json` are ignored and the assistant cannot write to `.claude/memory.md` — meaning nothing carries over between days.
3. **Connect Google Calendar** if you want `/start` to see your day. Without it, `/start` falls back to scanning the board and memory for dates.
4. Run `/start`.

## Working together

**Always work from inside this folder.** `cd ~/Executive-Assistant && claude`. The commands use relative paths, so they only find your board and notes from here.

**Permissions are already set so the boring stuff never interrupts you.** The assistant can freely read and write inside the vault — board, scratch pad, daily notes, meetings, memory. That's the friction it exists to absorb.

Everything else still stops and asks:

| Pre-approved, no prompt | Always asks first |
|---|---|
| Updating `Task Board.md` | Sending or drafting email |
| Clearing `Scratch Pad.md` | Creating or moving calendar events |
| Writing daily notes | Posting to Slack |
| Summarizing files in `Meetings/` | Touching files outside this folder |
| Updating `.claude/memory.md` | Anything on the internet |

`rm` and `git push` are blocked outright.

**The loop:**

- Morning — `/start`
- All day — dump raw thoughts into `Scratch Pad.md`, drop transcripts into `Meetings/`. Don't organize. That's the point.
- Midday, or whenever the pile feels big — `/sync`
- End of day — `/wrap-up`

**If something looks wrong,** press Esc to stop it mid-action. Everything lives in plain Markdown files and in git, so nothing is unrecoverable — `git diff` shows exactly what changed today.

## How to use it

Capture raw. Don't organize. Drop half-sentences in `Scratch Pad.md`, drop transcripts in `Meetings/`, and run `/sync` when the pile gets big. The filing is the assistant's job, not yours.
