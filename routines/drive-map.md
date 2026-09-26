# Drive map and color key (used by phone-sync.md Step 4 and 5)

Drive folder `Ellie Files` (id 18kMOjJuNFY_7u6rEVxsanFRUlX_GXJkh) holds one file per topic named `Where we left off - <Topic>`. Melissa asks "Ellie, where did we leave off on <Topic>?" and Ellie opens that file first.

| Topic | Folder id | Built from |
|---|---|---|
| Job Search | 1EJE9YAHK2pnaLZ8o-VkXF6g1bpq4ydtu | Applications.md, Waiting On |
| Meetings & Prep | 1Y1DKfI-w471txK-t4Zlp6EhXYHW3J5Bm | Meetings/*.md, prep notes |
| Reminders & Tasks | 1K8Aleb9OqEDmroWDQtuF2kbRZdEuXzI9 | Task Board.md, reminders |
| Saved Links | 14nnStHuMg8uPtxvq53GY1UvxqSaMD7td | Memory.md Saved Links |
| Ellie Setup | 1hNbRyq0LmeudaDbPmqlqpSrNHluKfN9F | Standing Instructions.md, routines/README.md changelog |
| Calendar | 1-9RxuHy0MaUD5rpb4I2-CjMixPt_Ghiv | Google Calendar, rest of the week, future events only |

Rebuild rule (saves tokens): Drive cannot rewrite a file. Rebuild a topic only when its source changed in THIS run (Calendar every run). `create_file` a NEW file in the topic folder (contentMimeType `text/html`, it becomes a Google Doc), then `trash_file` the OLD file with the same title in that folder. Never trash anything else. Each file: what is open, the last 5 things that happened (newest first), what is next. Short.

## Color key (same as the morning briefing; use inline color styles in HTML)
- Red #c62828: security, urgent, risk, overdue
- Amber #b26a00: follow-up, RSVP, deadline, waiting on
- Blue #1c4dc4: calendar, appointments, prep
- Green #0c7351: job search, interviews, opportunities, done
- Purple #6d21c9: development, events, other
- Gray #6b6b6b: low priority
