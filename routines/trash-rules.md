# Trash rules (used by the daily wrap inbox triage)

Copied from `generate_briefing.py` in the daily-briefing repo, so the wrap-up trashes exactly what the morning briefing trashes. If the briefing's lists change, refresh this file. Matching is a case-insensitive substring match against the full From header.

Trash = Gmail Trash only (`trash_thread`), recoverable for 30 days. Never permanent delete.

## Order of checks

1. PROTECTED sender, or subject/snippet mentions claude or anthropic: NEVER trash.
2. Sender matches ALWAYS TRASH, or is on `## Do Not Rescue` in `Memory.md`: trash.
3. Otherwise trash ONLY if it is clearly a marketing newsletter, promotional digest or subscription content she has no ongoing need to read, from an automated or bulk sender. Not personal or professional correspondence, job alerts, recruiter or networking mail, calendar, travel, financial, medical, receipts, government, account-security alerts, or an application status/rejection from a company. When unsure, do NOT trash: list it under INBOX TRIAGE instead. A false trash is the worst outcome (the AIChE interview invitation was trashed 8/29).
4. List every thread you trashed on the phone board under INBOX TRIAGE (sender, subject) so she can undo it.

## PROTECTED (never trash)

- match.com
- jobs-noreply@linkedin.com
- jobalerts-noreply@linkedin.com
- chatgpt
- openai.com
- claude
- anthropic.com
- united.com
- delta.com
- aa.com
- americanairlines
- southwest.com
- jetblue.com
- spirit airlines
- spiritairlines
- frontier airlines
- frontierairlines
- alaskaair
- hawaiianairlines
- lufthansa
- britishairways
- emirates
- airline
- air canada
- air france
- airfrance
- merrilllynch
- merrill lynch
- ml.com
- merrilledge
- chase.com
- bankofamerica
- bank of america
- wellsfargo
- wells fargo
- citibank
- citi.com
- usbank
- us bank
- tdbank
- td bank
- pnc.com
- pncbank
- capitalone
- capital one
- schwab.com
- fidelity.com
- vanguard.com
- synchrony
- ally.com
- discover.com
- barclays
- regions.com
- suntrust
- truist
- navyfederal
- navy federal
- usaa.com

## NEVER TRASH if subject/snippet mentions

- claude
- anthropic

## ALWAYS TRASH (sender contains)

- cooldeep
- medium daily digest
- @medium.com
- the average joe
- averagejoecrypto
- 1% better
- 1percentbetter
- the ai report
- theaireport
- optery
- christopher rainey
- giulia guerrieri
- tradealgo
- j.t. o'donnell
- jt o'donnell
- jtodonnell
- sophia davis
- fred from fireflies
- fireflies.ai
- experteer
- eharmony
- pranit naik
- quillbot
- phil strazzulla
- limitless creator
- 16handles
- techpresso
- stephanie adams
- ifttt
- tldr newsletter
- tldrnewsletter
- yesstyle
- kohls
- kohl's
- melissa westgate
- gap factory
- gapfactory
- gemma bonham
- info@skincareessentials.com
- hello@digistore24newsletter.com
- community@transform.us
- talentrealist@substack.com
- talent realist
- email.nextdoor.com
- emailreplies@messages.classmates.com
- team@craft.do
- insider monkey
- hattislaw.com
- lisa rangel
- chameleonresumes.com
- fractional in a box
- fractionalpowerhouse.com
- car shield
- carshield
- tractorsupply
- uncovering ai
- uncoverai@mail.beehiiv.com
- ai with mariah
- dreamtuesday.com
- newsletter@lg.behindthemarkets.com
- shopify
- quince
- david green
- newsletters-noreply@linkedin.com
- alison.com
- mail.lemon8-app.com
- no-reply@otter.ai
- students.udemy.com
- email.shoestation.com
- thepeoplepeoplegroup.com
- send.zapier.com
- redroosterharlem
- sarmail.cuddly.com
- anyaandniki.com
- mindstream.news
- cultivatedculture.com
- m.themuse.com
- 3percentconf.com
- leapsome.com
- jackcocchiarella@substack.com
- jointhecolab@substack.com
- ridethroo.ai
- mail.promptmates.ai
- microsoftstore.microsoft.com
- tealhq.com
- careerevolved=oliviagamber.com@f.kajabimail.net
- endeavorexecutive.com
- patient-voices.com
- kickresume.com
- peoplestrategycollective.org
- linktr.ee
- mycitizenshr.com
- theskimm.com
- workweek.com
- mail.apollo.io
- allevents.in
- emails.zappos.com
- marketing.landsend.com
- mail.shein.com
- mgs.opentable.com
- openart.ai
- noreply@glassdoor.com
- donaldjtrump.com
- e.targetoptical.com
- 360learning.com
- m.send.coursera.org
- make.com
- email.openai.com
- email.shoecarnival.com
- via rng tampa bay
- qapital.com
- skinlaundry.com
- softr.io
