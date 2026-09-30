"""Shared sections for the Ellie morning email and wrap-up, in the format of the Melissa Daily Briefing
(Melissa, 2026-09-30): Inbox Triage list with auto-trash counts, Executive Summary as three labelled cards,
and Action Required cards with Source / Why it matters / Next step / Due (RSVP pending, declined, mail to review).

Pure functions returning box rows (HTML). Rows use the @B@ border placeholder that ellie_ui.box fills.
"""
import html
import re
from datetime import datetime

F = "font-family:Helvetica,Arial,sans-serif;"
B = "@B@"
_URL = re.compile(r"(https?://[^\s<]+)")


def _e(t: str) -> str:
    return html.escape(t, quote=False)


def _link(t: str) -> str:
    return _URL.sub(lambda m: f'<a href="{m.group(1)}" style="color:#2F6BFF;">{m.group(1)}</a>', _e(t))


def action_card(icon: str, title: str, source: str, why: str, nxt: str, due: str, bar: str) -> str:
    def line(label: str, text: str) -> str:
        return (f'<tr><td valign="top" width="100" style="{F}font-size:12px;font-weight:bold;color:#44546B;padding:4px 8px 0 0;">{label}</td>'
                f'<td valign="top" style="{F}font-size:13px;line-height:19px;color:#33404F;padding-top:4px;">{_link(text)}</td></tr>')
    return (f'<tr><td bgcolor="#FFFDF5" style="background-color:#FFFDF5;padding:14px 16px;{B}">'
            '<table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%"><tr>'
            f'<td width="4" bgcolor="{bar}" style="background-color:{bar};font-size:0;line-height:0;">&nbsp;</td><td style="padding-left:12px;">'
            f'<div style="{F}font-size:15px;font-weight:bold;color:#12233C;">{icon} {_e(title)}</div>'
            f'<div style="{F}font-size:12px;color:#8994A3;padding-top:3px;">Source: {_e(source)}</div>'
            '<table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%" style="padding-top:4px;">'
            + line("Why it matters:", why) + line("Next step:", nxt) + line("Due:", due) + "</table></td></tr></table></td></tr>")


def summary_cards(risk: str, job: str, cal: str) -> list[str]:
    def card(label: str, dot: str, text: str) -> str:
        return (f'<tr><td bgcolor="#FFFFFF" style="background-color:#FFFFFF;padding:14px 16px;{B}">'
                '<table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%"><tr>'
                f'<td width="4" bgcolor="{dot}" style="background-color:{dot};font-size:0;line-height:0;">&nbsp;</td><td style="padding-left:12px;">'
                f'<div style="{F}font-size:10px;font-weight:bold;letter-spacing:1.6px;color:{dot};">&#9679; {label}</div>'
                f'<div style="{F}font-size:14px;line-height:21px;font-weight:bold;color:#12233C;padding-top:5px;">{_e(text)}</div>'
                "</td></tr></table></td></tr>")
    return [card("BIGGEST RISK / URGENT", "#FF3B3B", risk), card("BIGGEST JOB SEARCH / OPPORTUNITY", "#12A06B", job),
            card("BIGGEST CALENDAR / DEADLINE", "#2F6BFF", cal)]


_HC = f"background-color:#F5F7FA;padding:8px 12px;{F}font-size:10px;font-weight:bold;letter-spacing:0.6px;text-transform:uppercase;color:#8994A3;{B}"
_CELL = f"background-color:#FFFFFF;padding:10px 12px;{F}font-size:12px;color:#33404F;vertical-align:top;{B}"


def triage_rows(rescued: list[tuple[str, str]], inbox_rows: list[tuple[bool, str, str, str]], auto: list[tuple[int, str]], trash_left: int) -> list[str]:
    """Status / From / Subject / Summary table. auto = (count, what) per auto-trashed group, e.g. (5, "phishing/scams").
    trash_left = other emails sitting in Trash/Spam. Empty inbox + nothing trashed -> caller shows its own empty row."""
    def tr(cells: list[str], bg: str = "#FFFFFF") -> str:
        return "<tr>" + "".join(f'<td bgcolor="{bg}" style="{_CELL}">{c}</td>' for c in cells) + "</tr>"

    def wide(text: str, bg: str) -> str:
        return f'<tr><td colspan="4" bgcolor="{bg}" style="background-color:{bg};padding:10px 12px;{F}font-size:12px;color:#44546B;{B}">{text}</td></tr>'
    out = ["<tr>" + "".join(f'<td bgcolor="#F5F7FA" style="{_HC}">{h}</td>' for h in ("Status", "From", "Subject", "Summary")) + "</tr>"]
    out += [tr(['<b style="color:#12A06B;">✅ RESCUED</b>', _e(w), _e(s), "Rescued from Trash — back in your inbox, starred."], "#F0FBF6") for w, s in rescued[:10]]
    out += [tr(['<b style="color:#FF3B3B;">🚨 NEEDS YOU</b>' if n else "📥 INBOX", _e(f), _e(s), _e(ln)]) for n, f, s, ln in inbox_rows[:15]]
    out += [wide(f'🗑 <b style="color:#FF3B3B;">AUTO-TRASHED</b> &nbsp; <b>{n}</b> email{"s" if n != 1 else ""} auto-trashed ({_e(what)}) — see Trash Review', "#FDF0EE") for n, what in auto if n]
    if trash_left:
        out.append(wide(f'📁 <b>TRASH</b> &nbsp; <b>{trash_left}</b> email{"s" if trash_left != 1 else ""} in Trash/Spam — see Trash Review', "#FDF6EC"))
    return out


def _join_link(e: dict) -> str:
    for ep in e.get("conferenceData", {}).get("entryPoints", []):
        if ep.get("entryPointType") == "video" and ep.get("uri"):
            return ep["uri"]
    if e.get("hangoutLink"):
        return e["hangoutLink"]
    m = re.search(r"https://[\w.-]*zoom\.us/j/\d+[^\s\"<]*", f"{e.get('location', '')} {e.get('description', '')}")
    return m.group(0) if m else ""


def calendar_action_cards(events: list[dict], now: datetime) -> list[str]:
    """RSVP-pending cards (next 7 days) and declined-invite cards (today + tomorrow) from raw Calendar API events."""
    cards: list[str] = []
    for e in events:
        me = next((a for a in e.get("attendees", []) if a.get("self")), None)
        s = e["start"].get("dateTime")
        if not me or not s or e.get("status") == "cancelled" or e.get("organizer", {}).get("self"):
            continue
        d = datetime.fromisoformat(s).astimezone(now.tzinfo)
        days = (d.date() - now.date()).days
        if d < now:
            continue
        title, clock = e.get("summary", "(no title)"), d.strftime("%-I:%M%p").lower()
        when = f"{d.strftime('%a %-m/%-d')} {clock}"
        link = _join_link(e)
        who = e.get("organizer", {}).get("displayName") or e.get("organizer", {}).get("email", "")
        if me.get("responseStatus") == "needsAction":
            n = len(e.get("attendees", []))
            cards.append(action_card("⚠️", f"RSVP Pending — {title}", f"Google Calendar · {'Today ' + clock if days == 0 else when}",
                                     'Your status is "needsAction" on this event.' + (f" {n // 10 * 10}+ attendees are listed." if n >= 10 else ""),
                                     "Accept or decline the calendar invite now." + (f" Join link: {link}" if link else ""),
                                     "Today, before it starts" if days == 0 else f"Before {when}", "#FFAA00"))
        elif me.get("responseStatus") == "declined" and days <= 1:
            cards.append(action_card("⚠️", f"{title} — You Declined ({when})", "Google Calendar" + (f" · {who}" if who else "") + (" · Zoom" if "zoom" in link else ""),
                                     f"You declined this event for {'today' if days == 0 else 'tomorrow'}. Verify this was intentional. If it's a networking/professional opportunity, you may want to reconsider.",
                                     "Confirm your declination was intentional. If you'd like to attend, update your RSVP before it starts.",
                                     "By end of today", "#FFAA00"))
    return cards


REVIEW_CATS = {"Financial / Billing": ("🟢", "#12A06B", "This week"), "Security / Risk": ("🔵", "#2F6BFF", "Within 7 days"), "Medical / Health": ("🔵", "#2F6BFF", "This week")}


def mail_action_cards(mail: list[dict], cat_action: dict[str, str]) -> list[str]:
    """One card per financial / security / medical email still worth a look (inbox, rescued, or sitting in Trash)."""
    cards = []
    for m in mail:
        if m["cat"] in REVIEW_CATS and m["loc"] in ("inbox", "rescued", "trash"):
            icon, bar, due = REVIEW_CATS[m["cat"]]
            where = {"inbox": "In your inbox", "rescued": "Rescued from Trash", "trash": "In Trash — restore if you need it"}[m["loc"]]
            cards.append(action_card(icon, f"Review {m['subj'][:80]}", f"{m['frm']} · {where}", m["line"] or m["subj"], m.get("next") or cat_action[m["cat"]], m.get("due") or due, bar))
    return cards[:6]
