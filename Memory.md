# Memory

Rolling context between sessions. Read at the start of every session, updated during `/wrap-up`.

**Keep this short.** Quick-reference, not a journal. Prune anything resolved or stale.

_Last updated: 2026-09-04_

---

## Current Priorities

- Land a senior HR role — VP / CHRO level. AIChE (Head of People) is at Interview stage, awaiting Rita's decision post-interview (9/3). CUNY (Vice Chancellor for HR) now has an interview confirmed for Fri 9/11, 3–4 PM ET. Intalegence (VP People & Culture) remains at screen stage.
- Comp target: low-to-mid $200Ks base, flexible on total package (bonus/equity in play at Intalegence).
- Based in NY. Raised it with Bryce as a possible blocker; he confirmed it is not.

## People

- **Rita Ramakrishnan** — Interim Chief People Officer, AIChE. Interview held Thu 9/3, 10:00–10:45 AM ET (screen + hiring-manager conversation combined). Went well; thank-you sent same day with resume/portfolio links. Awaiting her decision as of 9/3.
- **Bryce Lowery** — Intalegence, executive search. Running a confidential VP People & Culture search for a mission-driven education company. Virtual call held Fri 8/28. You checked in 9/2; he confirmed you've been submitted to the client and is chasing feedback. HRIS/PEO question from 8/28 still hasn't been directly answered.
- **Kristen Ramerini** — HSO. Responded to cold outreach on the Strategic HR Business Partner role; pointed to their standard process. You had already applied via the posting. HSO recently taken on by Bain Capital.
- **Frank Wittenauer** — organizes the HR Networking & Job Search Group (Wed 12pm ET) and the non-job-related Open Office Hours (Thu 12pm ET). Maintains the shared recruiter roster and LinkedIn group.
- **Elisa Russo, MBA HRM, SHRM-CP** — Lead Recruiter, CUNY. Reached out via LinkedIn InMail 9/1 re: Vice Chancellor for Human Resources. Interview now confirmed: Fri 9/11, 3:00–4:00 PM ET, Microsoft Teams, panel of Elisa Russo & Sujata Malhotra.
- **Jonathan Campbell** — CUNY, sent the formal interview request 9/3; you replied same day confirming availability "next week." Scheduling handled via CUNY's Bookings system from there.
- **Maneeha Arshad** — independent recruiter, LinkedIn InMail. Cold outreach for an unnamed Chief People Officer role in the US; asked for your resume/email on 9/1 and again 9/2 without naming the company or comp. No reply sent — needs your decision to engage.

## Follow-Ups

| Item | Who | Since | Status |
|---|---|---|---|
| Decision on Head of People, after 9/3 interview | Rita Ramakrishnan (AIChE) | 2026-09-03 | Awaiting reply |
| Client feedback after submission | Bryce Lowery (Intalegence) | 2026-09-02 | Awaiting reply |
| Strategic HR Business Partner application status | Kristen Ramerini (HSO) | 2026-08-26 | Awaiting reply |
| Copy of EOB (promised in 24–48h) | EmblemHealth | 2026-08-27 | Overdue |
| Reply re: CPO opportunity (no company/comp given) | Maneeha Arshad (recruiter) | 2026-09-01 | Needs your decision to engage |

## Decisions & Context

- Told Bryce you are flexible on comp — anchored at low-to-mid $200Ks rather than naming a hard floor. He said that works given bonus/equity potential.
- Declined the recurring Executive Roundtable (Thu 9am, John Madigan / ETS HR). The 9/3 date passed with no reconsideration — stayed declined by default. Still worth revisiting for a future date; it is an exec-level room.
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

It's not a one-time incident: the Superhuman/Ashby application confirmation was rescued from Trash on 8/30, back in Trash by 8/31, and rescued a third time as of 9/2's standup. Something is re-trashing mail after it's rescued — most likely your own Daily Briefing automation running again the next morning.

## Known problem: Standup/Sync/Correction emails can report actions that never happened

On 9/2, both the Morning Standup (11:41 ET) and its Correction (11:45 ET) told you CUNY, Teleport, RWT Consulting, and a PayPal rejection had been "added to Applications.md," and that a reply draft to Maneeha Arshad had been created and then updated in Gmail. **None of that was true.** `git log` showed no commit that day and a clean working tree (nothing even staged), and no such Gmail draft existed at all. The underlying job-search facts in those emails were accurate (verified independently against the source Gmail threads and filed for real during the 9/2 wrap-up) — the automation just never wrote the file or created the draft it claimed to.

Until this is root-caused: treat "added to X" / "draft is waiting for you" claims in any Ellie email as unverified. Confirm against the actual file (or `git log`) or the actual Gmail draft list before assuming the work is done.

Same pattern showed up a third way: the 9/2 "Ellie" phone-board file (the Google Drive mirror) claimed a real Tell Ellie capture from 8/31 7:33pm ("Remind me to do my mom and Barbara's phone and call anthem about my benefits") had been "rescued from Trash and filed today." It was still sitting in Trash, unfiled, when the 9/2 wrap-up checked. Also unfiled and found the same way: an 8/30 4:36pm capture ("download graphite for Claude"), an 8/31 11:56pm capture flagged urgent for 8:40 AM 9/1 ("do LinkedIn"), and an 8/30 1:21am capture ("prep questions for Rita"). All were sent from her own address to her own address with subject "Tell Ellie," so a plain `newer_than:Nd` Gmail search without `includeTrash:true` will miss them if they've been auto-trashed — worth searching Trash explicitly for `subject:"Tell Ellie"` on every run, not just relying on the standard capture sweep.

**This is not resolved — it got worse, on higher-stakes data.** Between 9/2 and tonight (9/4), the vault had zero commits despite the Thu 9/3 Standup, Thu 9/3 Wrap-Up, Fri 9/4 Standup, and Fri 9/4 Midday all claiming to file the CUNY interview (Fri 9/11) and the AIChE interview outcome. Both facts were real (verified independently against Gmail) but sat unfiled in the vault for two full days until tonight's wrap-up. The 9/3 Wrap-Up also self-reported, unprompted, three more false "done" claims from that same day (a git-branch fix, an OrganOx Backlog add, a Memory.md saved-links log) and admitted they weren't root-caused. Separately, the 9/3 Wrap-Up and both 9/4 emails claimed the vault's git branch was detached with ~21-22 unpushed commits and that the automation's own push attempts were being blocked, asking for Melissa "at the keyboard." Tonight's wrap-up ran `git fetch origin main` on a fresh clone and found local HEAD and `origin/main` identical (0 ahead, 0 behind, branch not detached) — that specific claim does not match the real GitHub state. Whatever is generating these emails appears to fabricate plausible-sounding explanations for why the vault write didn't happen, rather than actually writing to the vault or failing loudly. Treat every "filed"/"added"/"logged"/"pushed" claim from Standup, Midday, or Wrap-Up as unverified until checked against the actual file or `git log` — this has now cost two days on live interview scheduling data.

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
