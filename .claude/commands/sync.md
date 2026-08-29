---
description: Process the Scratch Pad and new meeting notes, file everything, clear the pad
allowed-tools: Read, Write, Edit, Glob, Bash
---

# /sync — Process the Pile

I've been dumping notes. Sort them properly. This is handing you a pile of loose paper and getting back a clean desk.

## Steps

1. **Read `Scratch Pad.md`.** Process every line. For each item, decide what it actually is:
   - **Task** → goes to `Task Board.md`
   - **Context / decision / person detail** → goes to `.claude/memory.md`
   - **Event or observation** → goes into today's daily note
   - **Ambiguous** → keep it in the pad under `## Needs clarification` and ask me about it at the end
2. **Check `Meetings/`.** Find transcripts or notes not yet summarized (no matching entry in today's daily note, or no `> Processed on YYYY-MM-DD` marker at the top of the file). For each one, write a summary containing:
   - 3–5 bullet key points
   - **Decisions made**
   - **Action items** with an owner and a due date for each
   - Then add `> Processed on YYYY-MM-DD` as the first line of the source file so it isn't re-processed.
3. **Update `Task Board.md`.** Add every new action item assigned to me. Give each a priority and, where one exists, a due date. Don't duplicate anything already on the board — merge instead.
4. **Update today's daily note** at `Daily Notes/YYYY-MM-DD.md`. Create it from the template if it doesn't exist. Append what happened: meetings processed, decisions, notes captured, tasks added.
5. **Clear `Scratch Pad.md`.** Reset it to an empty template — but ONLY for items you successfully filed. Anything under `## Needs clarification` stays.

## Output Format

Short. Four lines plus questions:

```
Filed [n] items from Scratch Pad.
Summarized [n] meetings → [names]
Added [n] tasks to the board: [one-line list]
Daily note updated. Scratch Pad cleared.

Needs your call:
- [ambiguous item] → task, or just context?
```

**Never delete anything from the Scratch Pad that you did not write somewhere else first.**
