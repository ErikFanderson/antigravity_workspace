#!/usr/bin/env python3
"""
Google OAuth2 authentication script.
Generates credentials/google/token.json with access to:
  - Calendar
  - Gmail
  - Slides
  - Docs
  - Sheets
  - Drive
"""

import os
from pathlib import Path

from google_auth_oauthlib.flow import InstalledAppFlow

# All requested scopes
SCOPES = [
    "https://www.googleapis.com/auth/calendar",
    "https://www.googleapis.com/auth/gmail.modify",
    "https://www.googleapis.com/auth/presentations",
    "https://www.googleapis.com/auth/documents",
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]

CREDS_DIR = Path(__file__).resolve().parent.parent / "credentials" / "google"
CLIENT_SECRET = CREDS_DIR / "client_secret.json"
TOKEN_PATH = CREDS_DIR / "token.json"


def main():
    if not CLIENT_SECRET.exists():
        raise FileNotFoundError(f"Client secret not found at: {CLIENT_SECRET}")

    print(f"Using client secret: {CLIENT_SECRET}")
    print(f"Requested scopes:\n  " + "\n  ".join(SCOPES))
    print("\nStarting OAuth flow — your browser will open for authentication...")

    flow = InstalledAppFlow.from_client_secrets_file(str(CLIENT_SECRET), SCOPES)
    creds = flow.run_local_server(port=0)

    TOKEN_PATH.write_text(creds.to_json())
    print(f"\n✅ Token saved to: {TOKEN_PATH}")


if __name__ == "__main__":
    main()
