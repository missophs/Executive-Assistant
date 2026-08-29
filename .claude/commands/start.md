---
description: Morning standup — review the board, memory, and calendar, then plan the day
allowed-tools: Read, Write, Edit, Glob, Bash, mcp__claude_ai_Google_Calendar__list_events
---

# /start — Morning Standup

Run this as a **fast verbal standup**, not a report. Aim for something I can read in 60 seconds.

## Steps

1. **Read the board.** Open `Task Board.md`. Summarize what's on my plate — grouped, not listed one by one. Call out anything overdue or stale (untouched for 3+ days).
2. **Check the pipeline.** Open `Applications.md`. Flag anything with no contact in 7+ days, and any interview or deadline landing in the next 3 days.
3. **Read memory.** Open `Memory.md`. Surface any open follow-ups, waiting-on items, or context I'll need today. If something there is now stale, say so.
4. **Check time-sensitive items.** Pull today's events from Google Calendar. If the calendar isn't available, say so in one line and instead scan `Task Board.md` and `Memory.md` for dates, deadlines, and "waiting on" items landing today or tomorrow.
5. **Prioritize.** Give me a ranked plan for the day:
   - **Top 3** — what actually has to move today, and why.
   - **Deep work block** — the largest uninterrupted gap on my calendar, and what to spend it on.
   - **Conflicts / risks** — double-bookings, back-to-backs with no prep time, deadlines colliding.
6. **Prune.** Ask: *"Anything from yesterday you finished that I should clear off the board?"* Wait for my answer, then update `Task Board.md` — move completed items to Done with today's date.

## Output Format

```
## Standup — [Day, Date]

**Calendar:** [n meetings, first at X, last at Y] — or "not available"
**Deep work:** [time window]

### Top 3
1. [Task] — [one-line why]
2. ...
3. ...

### Also on the board
- [grouped one-liners]

### Watch out for
- [conflicts, deadlines, stale items]

### From memory
- [open follow-ups needing action today]
```

Then ask the pruning question and stop. Don't start executing tasks until I tell you which one.
