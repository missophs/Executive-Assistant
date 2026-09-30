"""Shared look for every Ellie email (morning, midday, wrap-up): coloured section bars with icons and a
greeting header with stat tiles, matching the old Melissa Daily Briefing but in Ellie's purple.
No gradients (Gmail strips them); every background carries bgcolor + inline style.
"""
F = "font-family:Helvetica,Arial,sans-serif;"
B = "@B@"  # row border placeholder: filled for every row except the last of a box

ICONS = {
    "Executive Summary": "⚡", "Inbox Triage — Quick List": "📋", "Action Required": "🚨", "Draft Replies — Awaiting Your OK": "✍️",
    "Full 7-Day Calendar": "📅", "Prepare": "🎯", "Job Search &amp; Interview Pipeline": "💼", "Full Email Review by Category": "🗂",
    "Trash Review": "🗑", "Promotional / Retail Summary": "🛍", "Newsletters &amp; Subscriptions": "📰", "Email Accounting": "🧮",
    "Dashboard": "📊", "Action Items": "✅", "Top 3 &amp; Follow Up": "🏆", "Rescued From Trash": "♻️", "Ellie Commands": "⌨️",
    "Inbox Trash (undo from Gmail Trash if wrong)": "🗑",
    "Prepare — Next 7 Days": "🎯", "Closed Out Today": "✅", "Filed Into Ellie Today": "📥", "Added To Your Calendar": "📅", "Carrying Into Tomorrow": "🔥",
    "Also Open This Week": "📋", "Slipping": "⚠️", "Calendar - Week Ahead": "📅", "Reminders - Next 7 Days": "⏰",
    "Waiting On": "⏳", "Job Pipeline": "💼", "Where To Look": "🧭",
    "Filed Your Notes": "📥", "Marked Done": "✅", "Needs Your Call": "❓",
}
BAR = {"#FFAA00": "#E0860B", "#00D68F": "#12A06B", "#8994A3": "#6B7889", "#A239FF": "#8A2BD9"}  # darker so white text reads

# Melissa Daily Briefing colours (2026-09-30): title -> (bar, title text, body tint, border). Anything not listed keeps its accent colour on white.
_RED, _YEL, _BLU, _GRN, _PUR, _GRY, _DRK = (("#C0392B", "#FFFFFF", "#FFF5F5", "#F5C6CB"), ("#D4A017", "#FFFFFF", "#FFFDF0", "#F0E0A0"), ("#1A6FB3", "#FFFFFF", "#F0F6FF", "#B8D4F0"),
                                            ("#1A7A4A", "#FFFFFF", "#F0FFF6", "#B0E0C8"), ("#6A3093", "#FFFFFF", "#FAF0FF", "#D8B4F8"), ("#555E6E", "#FFFFFF", "#F8F9FA", "#DEE2E6"),
                                            ("#1A1A2E", "#E0C97F", "#F8F9FA", "#DEE2E6"))
THEME = {"Inbox Triage — Quick List": _DRK, "Executive Summary": _RED, "Action Required": _YEL, "Draft Replies — Awaiting Your OK": _GRN, "Full 7-Day Calendar": _BLU,
         "Calendar - Week Ahead": _BLU, "Prepare — Next 7 Days": _BLU, "Prepare": _BLU, "Job Search &amp; Interview Pipeline": _GRN, "Job Pipeline": _GRN,
         "Full Email Review by Category": _PUR, "Trash Review": _GRY, "Promotional / Retail Summary": _YEL, "Newsletters &amp; Subscriptions": _PUR, "Email Accounting": _GRY,
         "Dashboard": _BLU, "Action Items": _GRN, "Top 3 &amp; Follow Up": _YEL, "Ellie Commands": _GRY, "Closed Out Today": _GRN, "Carrying Into Tomorrow": _YEL,
         "Slipping": _RED, "Waiting On": _YEL, "Reminders - Next 7 Days": _YEL, "Where To Look": _GRY}


def box(title: str, accent: str, rows: list[str], first: bool, colspan: bool | int = False) -> str:
    """One section: full-width coloured bar with an icon, then the rows. colspan = number of columns the rows use (True = 2)."""
    border = "border-bottom:1px solid #E9EDF2;"
    rows = [r.replace(B, border) for r in rows[:-1]] + [rows[-1].replace(B, "")]
    span = f' colspan="{2 if colspan is True else colspan}"' if colspan else ""
    bar, ink, tint, edge = THEME.get(title) or (BAR.get(accent, accent), "#FFFFFF", "#FFFFFF", "#D7DEE7")
    if tint != "#FFFFFF":
        rows = [r.replace('bgcolor="#FFFFFF" style="background-color:#FFFFFF;', f'bgcolor="{tint}" style="background-color:{tint};') for r in rows]
    return (f'<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="border:1px solid {edge};border-radius:8px;{"" if first else "margin-top:16px;"}">'
            f'<tr><td{span} bgcolor="{bar}" style="background-color:{bar};padding:12px 16px;border-radius:7px 7px 0 0;{F}font-size:13px;font-weight:bold;letter-spacing:2px;text-transform:uppercase;color:{ink};">'
            f'{ICONS.get(title, "")}&nbsp; {title}</td></tr>' + "".join(rows) + "</table>")


def header(kicker: str, now, greeting: str, sub: str, tiles: list[tuple[str, str, str]], mast: str) -> str:
    """Navy masthead like the Melissa Daily Briefing: kicker, greeting, date, one-line sub, and stat pills [(icon, value, label)]."""
    cells = "".join(
        f'<td align="center" bgcolor="#2A3A63" style="background-color:#2A3A63;padding:10px 6px;border-radius:16px;">'
        f'<div style="{F}font-size:16px;font-weight:bold;color:#E0C97F;">{icon}&nbsp;{value}</div>'
        f'<div style="{F}font-size:11px;line-height:14px;color:#E0E8F0;padding-top:3px;">{label}</div></td>'
        for icon, value, label in tiles)
    mast = "#16213E"
    return (f'<tr><td bgcolor="{mast}" style="background-color:{mast};padding:28px 22px 20px 22px;border-radius:7px 7px 0 0;">'
            '<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0">'
            f'<tr><td style="{F}font-size:10px;font-weight:bold;letter-spacing:2.4px;text-transform:uppercase;color:#E0C97F;padding-bottom:8px;">{kicker}</td></tr>'
            f'<tr><td style="{F}font-size:28px;line-height:34px;font-weight:300;color:#FFFFFF;">{greeting}</td></tr>'
            f'<tr><td style="{F}font-size:15px;color:#A8C8F0;padding:6px 0 4px 0;">{now.strftime("%A, %B")} {now.day}, {now.year}</td></tr>'
            f'<tr><td style="{F}font-size:13px;line-height:19px;color:#C9D6EA;padding:2px 0 16px 0;">{sub}</td></tr>'
            f'<tr><td><table role="presentation" width="100%" cellpadding="0" cellspacing="5" border="0"><tr>{cells}</tr></table></td></tr>'
            '</table></td></tr>')
