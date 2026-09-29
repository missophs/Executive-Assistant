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
    "Closed Out Today": "✅", "Filed Into Ellie Today": "📥", "Added To Your Calendar": "📅", "Carrying Into Tomorrow": "🔥",
    "Also Open This Week": "📋", "Slipping": "⚠️", "Calendar - Week Ahead": "📅", "Reminders - Next 7 Days": "⏰",
    "Waiting On": "⏳", "Job Pipeline": "💼", "Where To Look": "🧭",
    "Filed Your Notes": "📥", "Marked Done": "✅", "Needs Your Call": "❓",
}
BAR = {"#FFAA00": "#E0860B", "#00D68F": "#12A06B", "#8994A3": "#6B7889", "#A239FF": "#8A2BD9"}  # darker so white text reads


def box(title: str, accent: str, rows: list[str], first: bool, colspan: bool | int = False) -> str:
    """One section: full-width coloured bar with an icon, then the rows. colspan = number of columns the rows use (True = 2)."""
    border = "border-bottom:1px solid #E9EDF2;"
    rows = [r.replace(B, border) for r in rows[:-1]] + [rows[-1].replace(B, "")]
    span = f' colspan="{2 if colspan is True else colspan}"' if colspan else ""
    bar = BAR.get(accent, accent)
    return (f'<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="border:1px solid #D7DEE7;border-radius:6px;{"" if first else "margin-top:16px;"}">'
            f'<tr><td{span} bgcolor="{bar}" style="background-color:{bar};padding:12px 16px;border-radius:5px 5px 0 0;{F}font-size:12px;font-weight:bold;letter-spacing:1.6px;text-transform:uppercase;color:#FFFFFF;">'
            f'{ICONS.get(title, "")}&nbsp; {title}</td></tr>' + "".join(rows) + "</table>")


def header(kicker: str, now, greeting: str, sub: str, tiles: list[tuple[str, str, str]], mast: str) -> str:
    """Masthead row: kicker, date, greeting, one-line sub, and stat tiles [(icon, value, label)]."""
    cells = "".join(
        f'<td align="center" width="{100 // len(tiles)}%" bgcolor="#F3F1FB" style="background-color:#F3F1FB;padding:12px 4px;border-radius:5px;">'
        f'<div style="{F}font-size:22px;font-weight:bold;color:{mast};">{icon}&nbsp;{value}</div>'
        f'<div style="{F}font-size:9px;font-weight:bold;letter-spacing:0.8px;text-transform:uppercase;color:#5C6B7F;padding-top:4px;">{label}</div></td>'
        for icon, value, label in tiles)
    return (f'<tr><td bgcolor="{mast}" style="background-color:{mast};padding:26px 22px 20px 22px;border-radius:7px 7px 0 0;">'
            '<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0">'
            f'<tr><td style="{F}font-size:10px;font-weight:bold;letter-spacing:2.4px;text-transform:uppercase;color:#FFAA00;padding-bottom:8px;">{kicker}</td></tr>'
            f'<tr><td style="{F}font-size:12px;color:#E3D4FA;padding-bottom:6px;">{now.strftime("%A, %B")} {now.day}, {now.year}</td></tr>'
            f'<tr><td style="font-family:Georgia,\'Times New Roman\',serif;font-size:28px;line-height:33px;color:#FFFFFF;">{greeting}</td></tr>'
            f'<tr><td style="{F}font-size:13px;line-height:19px;color:#F5E9FF;padding:8px 0 16px 0;">{sub}</td></tr>'
            f'<tr><td><table role="presentation" width="100%" cellpadding="0" cellspacing="6" border="0"><tr>{cells}</tr></table></td></tr>'
            '</table></td></tr>')
