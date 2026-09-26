#!/usr/bin/env python3
"""
Run this script ONCE on your local machine to get your GOOGLE_REFRESH_TOKEN.
Works without a localhost redirect — paste the URL from your browser.

Prerequisites (run in your terminal first):
  pip3 install google-auth-oauthlib

Usage:
  python3 get_google_token.py
"""

import urllib.parse
from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = [
    "https://www.googleapis.com/auth/gmail.modify",
    "https://www.googleapis.com/auth/calendar.events",
    "https://www.googleapis.com/auth/drive",
]

print()
print("=" * 60)
print("  Google OAuth Token Helper")
print("=" * 60)
print()

client_id     = input("Paste GOOGLE_CLIENT_ID:     ").strip()
client_secret = input("Paste GOOGLE_CLIENT_SECRET: ").strip()
print()

client_config = {
    "installed": {
        "client_id":     client_id,
        "client_secret": client_secret,
        "auth_uri":      "https://accounts.google.com/o/oauth2/auth",
        "token_uri":     "https://oauth2.googleapis.com/token",
        "redirect_uris": ["http://localhost"],
    }
}

flow = InstalledAppFlow.from_client_config(client_config, SCOPES)
flow.redirect_uri = "http://localhost"
auth_url, _ = flow.authorization_url(prompt="consent", access_type="offline")

print("STEP 1 — Open this URL in your browser:")
print()
print(auth_url)
print()
print("STEP 2 — Log in and approve access.")
print("         The browser will show a 'This site can't be reached' error.")
print("         That is NORMAL. Don't close it.")
print()
print("STEP 3 — Copy the FULL URL from the browser address bar")
print("         (it starts with http://localhost/?state=...&code=...)")
print()

callback_url = input("Paste the full URL from the address bar: ").strip()

parsed = urllib.parse.urlparse(callback_url)
params = urllib.parse.parse_qs(parsed.query)
code = params.get("code", [None])[0]

if not code:
    print()
    print("ERROR: No authorization code found in that URL. Make sure you copied the full URL.")
else:
    flow.fetch_token(code=code)
    print()
    print("=" * 60)
    print("  SUCCESS")
    print("=" * 60)
    print()
    print("Add this as the GOOGLE_REFRESH_TOKEN secret in GitHub:")
    print()
    print(flow.credentials.refresh_token)
    print()
