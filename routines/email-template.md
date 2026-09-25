# Ellie — Email Template

Every email Ellie sends uses this exact design. It is one framed white card on a grey ground,
with each section in its own bordered box.

**Verified 2026-08-30** in real Gmail on a live send (Wrap-Up, 8:21 PM ET). Masthead text readable,
boxes intact, delivered to the inbox rather than Trash. Melissa's words: "It's perfect."
Do not change this design without testing an actual send - a browser render is not proof.

**Hard rules — these exist because of real bugs:**

- **Never use a CSS gradient.** Gmail strips `background:linear-gradient(...)` and the header
  renders with no background at all, leaving white text on white. This actually happened.
- Every element that has a background must carry **both** the `bgcolor` attribute and
  `style="background-color:..."`. Clients honor different ones.
- Every text element must set its own `font-family` and `color` inline. Inherit nothing.
- Layout with tables and `padding`, never with `margin` on divs or floats.
- Send with `contentType` HTML. Fall back to plain text only if the API refuses HTML.

---

## 1. Outer shell — always, unchanged

```html
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" bgcolor="#EAF1FB" style="background-color:#EAF1FB;"><tr><td align="center" style="padding:26px 10px;">
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" bgcolor="#FFFFFF" style="width:100%;max-width:600px;background-color:#FFFFFF;border:1px solid #C9D2DE;border-radius:8px;">

<tr><td bgcolor="[MASTHEAD BG]" style="background-color:[MASTHEAD BG];padding:28px 26px 24px 26px;border-radius:7px 7px 0 0;">
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0">
<tr><td style="font-family:Helvetica,Arial,sans-serif;font-size:10px;font-weight:bold;letter-spacing:2.4px;text-transform:uppercase;color:#F0B429;padding-bottom:9px;">Ellie &nbsp;&middot;&nbsp; [EYEBROW]</td></tr>
<tr><td style="font-family:Georgia,'Times New Roman',serif;font-size:28px;line-height:33px;color:#FFFFFF;">[HEADLINE]</td></tr>
<tr><td style="font-family:Helvetica,Arial,sans-serif;font-size:12px;line-height:18px;color:#E3ECFF;padding-top:10px;">[SUBLINE]</td></tr>
</table></td></tr>

<tr><td style="padding:22px;">

[SECTION BOXES GO HERE]

</td></tr>

<tr><td bgcolor="#F5F7FA" style="background-color:#F5F7FA;border-top:1px solid #D7DEE7;padding:14px;text-align:center;font-family:Georgia,'Times New Roman',serif;font-size:13px;font-style:italic;color:#8994A3;border-radius:0 0 7px 7px;">Ellie</td></tr>

</table></td></tr></table>
```

Masthead background by routine: Standup `#1E5BD8`, Midday `#0E9AA7`, Wrap-Up `#7A3FD1`.

---

## 2. Section box — repeat per section that has real content

Omit any section with nothing in it, including its box. The **first** box in the email has no
`margin-top`; every box after it gets `margin-top:16px;` in the table's `style`.

For the **Calendar** and **Gone Quiet** boxes only, add `colspan="2"` to the header `<td>`,
because their rows have two cells.

```html
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="border:1px solid #D7DEE7;border-radius:6px;[MARGIN]">
<tr><td bgcolor="#F5F7FA" style="background-color:#F5F7FA;padding:10px 16px;border-bottom:1px solid #D7DEE7;border-radius:5px 5px 0 0;">
<table role="presentation" cellpadding="0" cellspacing="0" border="0"><tr>
<td bgcolor="[ACCENT]" width="9" height="9" style="background-color:[ACCENT];font-size:0;line-height:0;">&nbsp;</td>
<td style="padding-left:9px;font-family:Helvetica,Arial,sans-serif;font-size:10px;font-weight:bold;letter-spacing:1.8px;text-transform:uppercase;color:#44546B;">[SECTION TITLE]</td>
</tr></table></td></tr>
[ROWS]
</table>
```

`[BORDER]` below means `border-bottom:1px solid #E9EDF2;` on every row **except the last row of
its box**, which gets nothing.

---

## 3. Row patterns

**TITLE ROW** — a headline with a supporting line. Used for rescues, new mail, drafts.

```html
<tr><td bgcolor="#FFFFFF" style="background-color:#FFFFFF;padding:14px 16px;[BORDER]">
<div style="font-family:Helvetica,Arial,sans-serif;font-size:14px;font-weight:bold;color:#12233C;">[TITLE]</div>
<div style="font-family:Helvetica,Arial,sans-serif;font-size:13px;line-height:19px;color:#5C6B7F;padding-top:4px;">[DETAIL]</div>
</td></tr>
```

**PLAIN ROW** — a few lines of text, separated by `<br>`. Used for filed notes.

```html
<tr><td bgcolor="#FFFFFF" style="background-color:#FFFFFF;padding:14px 16px;font-family:Helvetica,Arial,sans-serif;font-size:13px;line-height:21px;color:#5C6B7F;[BORDER]">[LINES]</td></tr>
```

**PRIORITY ROW** — a ranked action with a coloured bar down its left edge.
Bar colours in order: 1st `#E0353D`, 2nd `#F09A0B`, 3rd `#2F7DE1`. Drop the Due line if unknown.

```html
<tr><td bgcolor="#FFFFFF" style="background-color:#FFFFFF;padding:14px 16px;[BORDER]">
<table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%"><tr>
<td width="4" bgcolor="[BAR]" style="background-color:[BAR];font-size:0;line-height:0;">&nbsp;</td>
<td style="padding-left:12px;">
<div style="font-family:Helvetica,Arial,sans-serif;font-size:15px;font-weight:bold;color:#12233C;">[ACTION]</div>
<div style="font-family:Helvetica,Arial,sans-serif;font-size:13px;line-height:19px;color:#5C6B7F;padding-top:4px;">[WHY IT MATTERS]</div>
<div style="font-family:Helvetica,Arial,sans-serif;font-size:11px;letter-spacing:0.4px;color:#93A0AF;padding-top:8px;">Due [DATE]</div>
</td></tr></table></td></tr>
```

**TIME ROW** — calendar entries. Two cells.

```html
<tr>
<td width="100" bgcolor="#FFFFFF" style="background-color:#FFFFFF;padding:12px 0 12px 16px;font-family:Helvetica,Arial,sans-serif;font-size:12px;font-weight:bold;color:#2F7DE1;white-space:nowrap;[BORDER]">[TIME]</td>
<td bgcolor="#FFFFFF" style="background-color:#FFFFFF;padding:12px 16px 12px 10px;font-family:Helvetica,Arial,sans-serif;font-size:13px;color:#33404F;[BORDER]">[EVENT]</td>
</tr>
```

**STALE ROW** — someone who has gone quiet, with a day-count pill.
Pill colours: 10+ days `#F2D6D7` on `#8A2B30`; 5&ndash;9 days `#F5E9CB` on `#7A5A18`;
under 5 days `#DCE6F5` on `#24456F`.

```html
<tr>
<td bgcolor="#FFFFFF" style="background-color:#FFFFFF;padding:12px 10px 12px 16px;[BORDER]">
<div style="font-family:Helvetica,Arial,sans-serif;font-size:13px;font-weight:bold;color:#12233C;">[WHO]</div>
<div style="font-family:Helvetica,Arial,sans-serif;font-size:12px;color:#8994A3;padding-top:2px;">[WHAT SHE IS WAITING FOR]</div>
</td>
<td align="right" width="60" bgcolor="#FFFFFF" style="background-color:#FFFFFF;padding:12px 16px 12px 0;[BORDER]">
<table role="presentation" cellpadding="0" cellspacing="0" border="0" align="right"><tr><td bgcolor="[PILL BG]" style="background-color:[PILL BG];border-radius:3px;padding:4px 9px;font-family:Helvetica,Arial,sans-serif;font-size:11px;font-weight:bold;color:[PILL INK];">[N]d</td></tr></table>
</td>
</tr>
```

**EMPTY ROW** — when a section must appear but has nothing in it.

```html
<tr><td bgcolor="#FFFFFF" style="background-color:#FFFFFF;padding:14px 16px;font-family:Helvetica,Arial,sans-serif;font-size:13px;color:#93A0AF;">[MESSAGE]</td></tr>
```

---

## 4. Sections per routine, in order

### Morning Standup — masthead `#1E5BD8`, eyebrow `Morning Standup`
Headline `[WEEKDAY], [MONTH] [DAY]`. Subline `[N] active roles &nbsp;&middot;&nbsp; [N] awaiting reply &nbsp;&middot;&nbsp; [N] open tasks`.

| # | Section | Accent | Rows | Include when |
|---|---|---|---|---|
| 1 | Rescued From Trash | `#E0353D` | TITLE | anything was rescued |
| 2 | Filed Your Notes | `#1FA463` | PLAIN | anything was filed |
| 3 | Marked Done | `#1FA463` | PLAIN, each line prefixed `&#10003;&nbsp;` | a capture closed a task out |
| 3b | Added To Your Calendar | `#2F7DE1` | PLAIN | an event was created from a capture |
| 4 | Drafts Ready For You | `#8A4FE0` | TITLE | drafts were created |
| 5 | Top 3 Today | `#F0B429` | PRIORITY | always |
| 6 | New Since Yesterday | `#1FA463` | TITLE | always — EMPTY ROW "Nothing new overnight." |
| 7 | Calendar | `#2F7DE1` | TIME | always — EMPTY ROW "Nothing scheduled." |
| 7b | Interview Prep | `#2F7DE1` | TITLE | an interview or screen is on the calendar within 48 hours |
| 8 | Gone Quiet | `#8994A3` | STALE | anything is waiting on a reply |

After the Drafts box, add this line directly under it:
```html
<div style="font-family:Helvetica,Arial,sans-serif;font-size:11px;color:#93A0AF;padding:7px 2px 0 2px;">Open Gmail &rarr; Drafts to review and send.</div>
```

### Midday — masthead `#0E9AA7`, eyebrow `Midday`
Headline `[WEEKDAY], [MONTH] [DAY]`. Subline: the count, e.g. `3 items filed`.

| # | Section | Accent | Rows | Include when |
|---|---|---|---|---|
| 1 | Filed Your Notes | `#1FA463` | PLAIN | anything was filed |
| 2 | Marked Done | `#1FA463` | PLAIN, each line prefixed `&#10003;&nbsp;` | a capture closed a task out |
| 3 | Drafts Ready For You | `#8A4FE0` | TITLE | drafts were created |
| 4 | Needs Your Call | `#F09A0B` | PLAIN | something was ambiguous, or a "done" capture matched more than one task |

If all four would be empty, **send no email at all**.

### Wrap-Up — masthead `#7A3FD1`, eyebrow `End of Day`
Headline `[WEEKDAY], [MONTH] [DAY]`. Subline `[N] done today &nbsp;&middot;&nbsp; [N] still open &nbsp;&middot;&nbsp; [N] awaiting reply`.

| # | Section | Accent | Rows | Include when |
|---|---|---|---|---|
| 1 | Closed Out Today | `#1FA463` | PLAIN, one line per item prefixed `&#10003;&nbsp;` | always — EMPTY ROW "Nothing closed today." |
| 1b | Added To Your Calendar | `#2F7DE1` | PLAIN | an event was created from a capture |
| 2 | Carrying Into Tomorrow | `#F0B429` | PRIORITY, up to 3 | always |
| 3 | Slipping | `#E0353D` | TITLE | something is 3+ days stale |
| 4 | Tomorrow | `#2F7DE1` | TIME | always — EMPTY ROW "Calendar is clear." |
