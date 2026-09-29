"""Builds a Meetings/<date> <title>.md prep doc from the vault only (no AI, no web). Anything not in the vault says "not in vault".
Pure function; phone_sync.py passes in the capture text, the calendar event it found (or None), Applications.md and Memory.md.
"""
import html
import re

STOP = {"prep", "prepare", "for", "interview", "with", "tomorrow", "today", "the", "my", "a", "an", "call", "meeting", "screen", "to", "on", "at",
        "me", "please", "ellie", "tell", "and", "of", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday", "next", "this"}


def keywords(text: str) -> list[str]:
    return [w for w in re.findall(r"[A-Za-z0-9&]+", text) if w.lower() not in STOP and len(w) >= 2]


def build_prep(text: str, day: str, event: dict | None, apps_md: str, memory_md: str) -> tuple[str, str] | None:
    """Returns (title, markdown) or None when the vault has nothing on it and there is no calendar event."""
    kws = keywords(text)
    rows = [[x.strip() for x in l.strip().strip("|").split("|")] for l in apps_md.splitlines() if l.startswith("|") and not l.startswith("|---")]
    rows = [c for c in rows if len(c) >= 7 and c[0] not in ("Company", "---")]
    app = next((c for c in rows if any(k.lower() in c[0].lower().split() or k.lower() == c[0].lower() for k in kws)), None)
    if not app and not event:
        return None
    company = app[0] if app else (event or {}).get("summary", text)
    lines_mem = [l.strip() for l in memory_md.splitlines()
                 if l.strip().startswith("- ") and any(re.search(rf"\b{re.escape(k)}\b", l, re.I) for k in ([company] + kws[:3])) and not re.match(r"- [0-9a-f]{16} \|", l.strip())]
    lead = [re.sub(r"\s+", " ", l[2:])[:300] for l in lines_mem[:4]]
    title = f"{company} prep"
    who = []
    when = "not in vault (no matching calendar event found — check your calendar app, or tell Ellie the time)"
    where = "not in vault"
    if event:
        s = event["start"].get("dateTime") or event["start"].get("date")
        when = s.replace("T", " ")[:16] if s else when
        where = event.get("hangoutLink") or event.get("location") or "not in vault"
        who = [a.get("displayName") or a.get("email", "") for a in event.get("attendees", []) if not a.get("self")]
    if app:
        who = who or [app[6]]
    md = [f"# Prep: {company} — {day}", "", "## When and where",
          f"- When: {when}", f"- Where: {where}", f"- Who: {', '.join(who) if who else 'not in vault'}", "",
          "## Where things stand",
          f"- Role: {app[1] if app else 'not in vault'}",
          f"- Stage / last contact: {app[2] + ' / ' + app[4] if app else 'not in vault'}",
          f"- What you owe them / notes: {app[5].replace('**', '')[:400] if app else 'not in vault'}", "",
          "## Lead with (from your notes)"] + ([f"- {l}" for l in lead] or ["- not in vault"]) + [
          "", "## Questions to ask", "- not in vault (Ellie does not invent questions — tell her the ones you want listed)", "",
          "## Logistics checklist", "- Confirm the time and link the night before", "- Have your resume and the job description open", ""]
    return title, "\n".join(md)


def to_html(md: str) -> str:
    """Prep markdown -> simple email HTML (headings, bullets, bold), so the doc can be read on a phone."""
    out, in_ul = [], False
    inline = lambda t: re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", html.escape(t, quote=False))
    for l in md.splitlines():
        if l.startswith("- "):
            out.append(("" if in_ul else "<ul>") + f"<li>{inline(l[2:])}</li>")
            in_ul = True
            continue
        if in_ul:
            out.append("</ul>")
            in_ul = False
        if l.startswith("# "):
            out.append(f'<h2 style="font-family:Georgia,serif;color:#3B1B8F;">{inline(l[2:])}</h2>')
        elif l.startswith("## "):
            out.append(f'<h3 style="font-family:Helvetica,Arial,sans-serif;color:#6D21C9;margin-bottom:4px;">{inline(l[3:])}</h3>')
        elif l.strip():
            out.append(f"<p>{inline(l)}</p>")
    return '<div style="font-family:Helvetica,Arial,sans-serif;font-size:14px;line-height:21px;color:#12233C;max-width:600px;">' + "\n".join(out) + ("</ul>" if in_ul else "") + "</div>"


if __name__ == "__main__":  # runnable check: python scripts/prep_doc.py — synthetic data only
    apps = "| Company | Role | Stage | Applied | Last contact | Notes | Contact |\n|---|---|---|---|---|---|---|\n" \
           "| Acme Corp | HR Director (Req X) | Screen | unknown | 2026-09-27 | Teams booked | Jane Roe, Recruiter |\n"
    mem = "- **Jane Roe** — Recruiter, Acme Corp. Emailed 9/27.\n- Unrelated line\n1a0e3ab151b94e41 | 2026-09-27 | Acme Corp filed\n"
    r = build_prep("prep for interview with Acme tomorrow", "2026-09-30", None, apps, mem)
    assert r and r[0] == "Acme Corp prep"
    for needle in ("Jane Roe", "Screen / 2026-09-27", "not in vault (no matching calendar event", "HR Director"):
        assert needle in r[1], needle
    assert "Unrelated" not in r[1] and "1a0e3ab" not in r[1]
    assert build_prep("prep for interview with Zzz", "2026-09-30", None, apps, mem) is None
    ev = {"summary": "Acme call", "start": {"dateTime": "2026-09-30T14:00:00-04:00"}, "hangoutLink": "https://teams/x", "attendees": [{"email": "j@acme.com", "displayName": "Jane R"}]}
    assert "2026-09-30 14:00" in build_prep("prep Acme", "2026-09-30", ev, apps, mem)[1]
    h = to_html(r[1])
    assert h.startswith("<div") and "<li>" in h and "<h2" in h and "Jane Roe" in h
    print("ok")
