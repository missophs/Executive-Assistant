#!/usr/bin/env python3
"""One-time helper: gets a Google token for Ellie and saves the GitHub secrets itself.

Nothing secret is printed or written to disk. Run:
  ~/.ellie-venv/bin/python ~/Documents/Claude/Executive-Assistant/scripts/get_google_token.py
"""
import getpass
import subprocess
from google_auth_oauthlib.flow import InstalledAppFlow

REPO = "missophs/Executive-Assistant"
DEFAULT_CLIENT_ID = "522559244108-85h0558rv9n4rd8c9q0v33do87uu32ib.apps.googleusercontent.com"
SCOPES = [
    "https://www.googleapis.com/auth/gmail.modify",
    "https://www.googleapis.com/auth/calendar.events",
    "https://www.googleapis.com/auth/drive",
]


def save_secret(name: str, value: str) -> None:
    subprocess.run(["gh", "secret", "set", name, "-R", REPO], input=value.encode(), check=True)
    print(f"  saved {name}")


print("\nEllie Google setup\n")
import glob, json, os
files = sorted(glob.glob(os.path.expanduser("~/Downloads/client_secret*.json")), key=os.path.getmtime)
if files:
    cfg = json.load(open(files[-1]))["installed"]
    client_id, client_secret = cfg["client_id"], cfg["client_secret"]
    print(f"Using {os.path.basename(files[-1])} from Downloads. Nothing to paste.")
else:
    client_id = input("Client ID (press Return to use the daily-briefing-2026-v2 one): ").strip() or DEFAULT_CLIENT_ID
    client_secret = getpass.getpass("Client secret (paste it; nothing will show on screen), then press Return: ").strip()
    if not client_secret:
        raise SystemExit("No secret entered. Nothing was saved.")

flow = InstalledAppFlow.from_client_config(
    {"installed": {
        "client_id": client_id,
        "client_secret": client_secret,
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "redirect_uris": ["http://localhost"],
    }},
    SCOPES,
)
print("\nYour browser will open. Sign in, click Advanced, click 'Go to gws local (unsafe)',")
print("tick every box, click Continue. Then come back here.\n")
creds = flow.run_local_server(port=0, prompt="consent", access_type="offline")
if not creds.refresh_token:
    raise SystemExit("Google did not return a refresh token. Nothing was saved. Run it again.")

print("\nSaving secrets to GitHub:")
save_secret("GOOGLE_CLIENT_ID", client_id)
save_secret("GOOGLE_CLIENT_SECRET", client_secret)
save_secret("GOOGLE_REFRESH_TOKEN", creds.refresh_token)

api_key = getpass.getpass("\nAnthropic API key (paste it, or press Return to skip for now): ").strip()
if api_key:
    save_secret("ANTHROPIC_API_KEY", api_key)
else:
    print("  skipped ANTHROPIC_API_KEY")
print("\nDONE. Nothing secret was printed.")
