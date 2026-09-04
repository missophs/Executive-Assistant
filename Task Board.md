# Task Board

Single source of truth for open work. Updated by `/start`, `/sync`, and `/wrap-up`.

Format: `- [ ] Task — owner · due YYYY-MM-DD · #project`

---

## 🔥 Today
<!-- Must know today. Keep to 3. -->

- [ ] Insurance calls, both overdue — EmblemHealth for the EOB (1-800-447-8255, promised 24–48h on 8/27) and Anthem re: your benefits. Call, don't email — EmblemHealth's own reply confirms their inbox is unmonitored · due 2026-08-31 · #admin
- [ ] Call the dentist — captured via Tell Ellie 8/29 evening ("Monday"), missed, now overdue · due 2026-08-31 · #admin
- [ ] **Vault-write/reporting bug — now 3 days deep, hit real interview data.** Standup/Wrap-Up emails on 9/3 and 9/4 all claimed the CUNY interview and AIChE outcome were filed to the vault. None of it was — `git log` shows no commit since 9/2 until tonight. Real facts recovered from Gmail and filed for real tonight (see Applications.md). Same emails also claimed a "detached branch with 21+ unpushed commits" blocking push — a fresh clone + `git fetch origin main` tonight shows local HEAD and `origin/main` are identical, 0 ahead/0 behind. That specific claim does not match the actual GitHub state · due 2026-09-04 · #tooling

## ⏭ This Week

- [ ] Book nail appointment with Dana — for "next Tuesday" (assuming 9/8, confirm if you meant 9/1) · due 2026-09-01 · #personal
- [ ] **Investigate: Standup/Wrap-Up emails keep reporting vault updates that never happened** — Confirmed again on 9/3 and 9/4 (see Today item above). The 9/3 Wrap-Up also admitted, unprompted, 3 more false "done" claims from that same day (a git-branch fix, an OrganOx Backlog add, a Memory.md saved-links log) — none were root-caused. Until this is fixed, treat every "filed"/"added"/"logged" claim in these emails as unverified against the actual file or `git log` · due 2026-09-02 · #tooling
- [ ] Reply re: CUNY thank-you follow-through — none needed now, but watch for Rita's (AIChE) decision and CUNY's next-round scheduling · #aiche

## 📋 Backlog

- [ ] Triage 2 unread LinkedIn alerts — Head of People @ advisorey ($200–275K), Head of HR Real Estate · #sourcing
- [ ] Triage new leads — OrganOx, VP HR North America (LinkedIn alert, 9/2); Head of People @ Empathy, $180–200K (Indeed, 9/4, landed in swm3016@ — a fourth inbox not previously tracked) · #sourcing
- [ ] Amanda Greene (C-Suite Career Corp) — you asked scam-verification questions 8/25, no reply since (8+ days) · #sourcing
- [ ] Respond to Maneeha Arshad (recruiter, LinkedIn InMail) — Chief People Officer opportunity, no company or comp disclosed. She's asked for your resume/email twice (9/1 and 9/2). No reply sent yet — needs your decision to engage before a reply gets drafted · #sourcing
- [ ] Clarify "do my mom and Barbara's phone" — exact wording from your 8/31 7:33pm Tell Ellie capture ("Remind me to do my mom and Barbara's phone and call anthem about my benefits"). Meaning unclear — confirm what this means · #personal
- [ ] Confirm "do LinkedIn" task from 8/31 11:56pm capture (flagged urgent for 8:40 AM on 9/1) — that window passed 2 days ago with no record either way. Still needed, or drop it? · #sourcing
- [ ] Download Graphite (for Claude Code) — captured via Tell Ellie 8/30, never filed until tonight · #personal

## ⏳ Waiting On
<!-- Blocked on someone else. Note who and since when. -->

- [ ] Decision on Head of People — Rita Ramakrishnan, AIChE, after 9/3 interview + same-day thank-you · since 2026-09-03
- [ ] Client feedback after submission — Bryce Lowery, Intalegence · since 2026-09-02
- [ ] Application status, Strategic HR Business Partner — Kristen Ramerini, HSO · since 2026-08-26
- [ ] Copy of EOB — EmblemHealth · since 2026-08-27
- [ ] Verification response — Amanda Greene, C-Suite Career Corp · since 2026-08-25

## ✅ Done
<!-- Cleared during /start and /wrap-up. Archive monthly. -->

- [x] AIChE interview held with Rita, 10:00–10:45 AM ET — screen + hiring-manager conversation combined, went well; thank-you sent same day with resume/portfolio links. Real, verified against Gmail; the vault had never been updated with this despite 3 days of automations claiming it was — 2026-09-03
- [x] CUNY interview scheduled — Fri 9/11, 3:00–4:00 PM ET, Microsoft Teams, panel Elisa Russo & Sujata Malhotra. Same situation — real, verified against the CUNY Bookings confirmation and your reply to Jonathan Campbell, never actually filed until tonight — 2026-09-03
- [x] Executive Roundtable Thu 9/3 — date passed with no reconsideration; stayed declined by default, no further action needed — 2026-09-03
- [x] Followed up with Bryce Lowery (Intalegence) — he confirmed you've been submitted to the client and is chasing feedback — 2026-09-02
- [x] Filed CUNY (Vice Chancellor, HR), Teleport (Sr. People BP – GTM), and RWT Consulting applications to Applications.md — real applications from 8/31–9/1 that this morning's automation claimed to file but never did — 2026-09-02
- [x] Closed out PayPal (Sr. Manager, People Business Partner) — rejected 8/31, filed for pattern-spotting — 2026-09-02
- [x] Closed out IPC Systems (Global People Partner) — inbound interview invite, you engaged, recruiter declined same day — 2026-09-02
- [x] Confirmed Daily Job Search Sweep automation is still firing daily (verified sends on 8/31, 9/1, 9/2) — 2026-09-02
- [x] Rescued and actually filed the 8/30–8/31 Tell Ellie captures that were sitting in Trash (Anthem/mom-Barbara, urgent LinkedIn task, Graphite download, Rita prep questions) — previously claimed filed but weren't — 2026-09-02
- [x] Virtual call with Bryce Lowery re: VP, People & Culture — 2026-08-28
- [x] Sent additional background to Bryce for candidate profile — 2026-08-28
- [x] Replied to Bryce with HRIS / PEO question — 2026-08-28
- [x] Replied to Rita Ramakrishnan at AIChE, confirmed Thursday — 2026-08-29
- [x] Rescued the AIChE invite from Trash and accepted it — Thu 9/3 10:00 ET — 2026-08-29
