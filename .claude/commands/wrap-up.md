---
description: End of day — final sweep, day summary, and write memory for tomorrow
allowed-tools: Read, Write, Edit, Glob, Bash
---

# /wrap-up — Close Out the Day

Nothing falls through the cracks. This is the last pass before I stop for the day.

## Steps

1. **Final sweep.** Check `Scratch Pad.md` and `Meetings/` for anything unprocessed. If there is, process it now the same way `/sync` does — don't just report that it's there.
2. **Final board update.** Open `Task Board.md`:
   - Ask me what I finished today, then move those to Done with the date.
   - Flag anything that slipped — on the board 3+ days with no movement.
   - Reorder tomorrow's priorities to the top.
3. **Update today's daily note** at `Daily Notes/YYYY-MM-DD.md`. Add an `## End of Day` section: what got done, what moved, what's still open, and anything notable.
4. **Write memory.** Update `.claude/memory.md` with anything that should survive to tomorrow:
   - New or changed priorities
   - People context (who I'm waiting on, who's waiting on me)
   - Follow-ups with dates
   - Decisions made today and the reasoning behind them

   Keep it a quick-reference file, not a journal. Prune anything that's now resolved or stale — don't let it grow forever.
5. **Give me the end-of-day summary.**

## Output Format

```
## End of Day — [Day, Date]

**Done today:** [n items] — [short list]
**Moved forward:** [items and why]
**Still open:** [count, with the one that matters most]

**Tomorrow's top 3:**
1. ...
2. ...
3. ...

**Flagged:** [anything slipping, anyone waiting on me]
**Memory updated:** [one line on what you wrote]
```

Stop there. Don't start new work.
