# Memory

Rolling context between sessions. Read at the start of every session, updated during `/wrap-up`.

**Keep this short.** Quick-reference, not a journal. Prune anything resolved or stale.

_Last updated: 2026-08-29_

---

## Current Priorities

- Land a senior HR role — VP / CHRO level. AIChE (Head of People) and Intalegence (VP People & Culture) are both at screen stage.
- Comp target: low-to-mid $200Ks base, flexible on total package (bonus/equity in play at Intalegence).
- Based in NY. Raised it with Bryce as a possible blocker; he confirmed it is not.

## People

- **Rita Ramakrishnan** — Interim Chief People Officer, AIChE. **Interview confirmed: Thu 9/3, 10:00–10:45 AM ET, Google Meet.** Reached out 8/29 re: Head of People. Running the initial screen and the hiring manager conversation as one combined 45-minute session, so it carries more weight than a normal first call.
- **Bryce Lowery** — Intalegence, executive search. Running a confidential VP People & Culture search for a mission-driven education company. Virtual call held Fri 8/28. Building your candidate profile from the call + resume. Open question outstanding: HRIS, and whether benefits are in-house or PEO.
- **Kristen Ramerini** — HSO. Responded to cold outreach on the Strategic HR Business Partner role; pointed to their standard process. You had already applied via the posting. HSO recently taken on by Bain Capital.
- **Frank Wittenauer** — organizes the HR Networking & Job Search Group (Wed 12pm ET) and the non-job-related Open Office Hours (Thu 12pm ET). Maintains the shared recruiter roster and LinkedIn group.

## Follow-Ups

| Item | Who | Since | Status |
|---|---|---|---|
| HRIS + PEO question, and next step after the call | Bryce Lowery (Intalegence) | 2026-08-28 | Awaiting reply |
| Strategic HR Business Partner application status | Kristen Ramerini (HSO) | 2026-08-26 | Awaiting reply |
| Copy of EOB (promised in 24–48h) | EmblemHealth | 2026-08-27 | Overdue |

## Decisions & Context

- Told Bryce you are flexible on comp — anchored at low-to-mid $200Ks rather than naming a hard floor. He said that works given bonus/equity potential.
- Declined the recurring Executive Roundtable (Thu 9am, John Madigan / ETS HR). Worth revisiting — it is an exec-level room.
- You run a self-built Daily Job Search Sweep (TypeScript, ~2pm ET). The 8/26 edition reported 62 roles, 19 in the 48-hour priority band.

## Applications use several inboxes

You apply from more than one address — `melissaw212@`, `melhr212@`, and `dhwconsulting3@`. HSO and Dropbox confirmations landed in `melhr212@`, not your main inbox. Worth checking all of them, or forwarding to one.

## Ellie's emails — design is settled

The look of every Ellie email is defined in `routines/email-template.md`, which all three cloud
routines read at run time. Verified working in real Gmail on 2026-08-30. The earlier design used a
CSS gradient for the header; Gmail strips gradients, so the header rendered with no background and
the white text was invisible. Solid `bgcolor` tables only. Change the template, not the routines.

## Melissa's own automations — do NOT flag these

She runs two automations of her own. Both are hers, both are expected, neither is a security issue.
A wrap-up run on 2026-08-30 mistook the first one for an unauthorized "Chief of Staff" with Gmail
write-access and put a false SECURITY item at the top of her Task Board. Do not repeat that.

1. **"Melissa Daily Briefing"** / "Executive Briefing" — one email, mornings only, around 7:00 AM,
   self-sent (from her address to her address), written in the voice of an Executive Chief of Staff.
   **Melissa confirmed 2026-08-30: this is hers, it is accurate, and she relies on it.** Treat it as
   trusted. By its own content it triages her inbox and auto-trashes mail, which is the most likely
   source of the over-aggressive trashing described below - but the briefing itself is not a problem.
2. **Daily Job Search Sweep** — separate and unrelated, TypeScript, around 2pm ET. Reports open roles.

Self-sent mail titled "Melissa Daily Briefing" is her own automation, not a capture and not a threat.
Skip it when emptying captures, and never file it as a task.

## Known problem: mail triage is too aggressive

Your automated email triage sent the **AIChE interview invitation** to Trash, and also trashed the standup email. Real, high-value mail from unknown senders is being discarded. Rita's address is `rita@iksana.com` (AIChE uses Workable, so recruiter mail arrives from unfamiliar domains). Worth allow-listing recruiter and ATS domains.

## How Melissa Captures Things

**Primary: the "Tell Ellie" iOS Shortcut** (built 2026-08-29, icon on her iPhone home screen).
Tap the icon -> talk -> it sends. Also works hands-free: "Hey Siri, Tell Ellie."
**Verified working 2026-08-29:** silent send confirmed (no compose window), From and To both
`melissaw212@gmail.com`, icon on the home screen. Two test captures sent that evening.

If it ever breaks or needs rebuilding, this is the exact recipe:
- Shortcuts app -> Library -> `+`
- Action 1: **Dictate Text**
- Action 2: **Send Email** (NOT "Email Address" - that one only stores an address)
- Message = the `Dictated Text` variable (iOS fills this in automatically)
- Subject = `Tell Ellie`
- Recipients = `melissaw212@gmail.com` typed literally, not the contact bubble
- **Show Compose Sheet = OFF** so it sends without a confirmation tap
- Rename to `Tell Ellie`, then Add to Home Screen

**Backup: the Google Drive file titled `Tell Ellie`.** Type into it from any device.

Ellie empties both at 7:30 AM, 1:00 PM, and 5:00 PM **seven days a week**, and reports what she filed under
"Filed Your Notes" in the standup email.

Note: her captures are found by sender, not subject - the routines search
`from:melissaw212@gmail.com to:melissaw212@gmail.com`. If the From address on a capture
is ever anything other than her Gmail, Ellie will not see it.

## Working Preferences

- Terse and direct. Lead with the answer. No filler.
- Approval required before anything is sent, scheduled, or shared externally.
