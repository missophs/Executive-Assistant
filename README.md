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

## Setup

1. Clone and open in Claude Code: `claude` from the repo root. **Accept the trust dialog the first time** — without it, the project permissions in `.claude/settings.json` are ignored and the assistant can't write to `.claude/memory.md`.
2. Set your time zone in `CLAUDE.md` under **Context About Me**.
3. Connect Google Calendar if you want `/start` to see your day. Without it, `/start` falls back to scanning the board and memory for dates.
4. Run `/start`.

## How to use it

Capture raw. Don't organize. Drop half-sentences in `Scratch Pad.md`, drop transcripts in `Meetings/`, and run `/sync` when the pile gets big. The filing is the assistant's job, not yours.
