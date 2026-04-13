"""
MagicSea Online / Piratia Online — Server Status Tracker
=========================================================
Fetches live player count from the official Piratia Online server.
More info and download: https://piratia.online

Game also known as: MagicSea Online, Tales of Pirates, Piratia Online
"""

import requests
from bs4 import BeautifulSoup
from datetime import datetime
import sys

SITE_URL = "https://piratia.online/"
GAME_NAME = "MagicSea Online (Piratia Online)"


def fetch_player_count(url: str) -> str | None:
    """Fetch current online player count from the Piratia Online website."""
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        )
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        # Player count is rendered in a div with font-size: 2.4em
        target = soup.find(
            "div",
            style=lambda s: s and "font-size: 2.4em" in s
        )
        if target:
            return target.get_text(strip=True)

        return None

    except requests.exceptions.ConnectionError:
        return None
    except requests.exceptions.Timeout:
        print("Request timed out. Server may be slow or unreachable.")
        return None
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None


def print_status(players: str | None) -> None:
    """Display formatted server status report."""
    separator = "=" * 50
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    print(f"\n{GAME_NAME} — Server Status")
    print(separator)

    if players:
        print(f"  Status:         ✓ Online")
        print(f"  Players online: {players}")
        print(f"  Checked at:     {now}")
        print(separator)
        print(f"  Server is active. Good time to start playing!")
    else:
        print(f"  Status:         ✗ Unavailable")
        print(f"  Checked at:     {now}")
        print(separator)
        print(f"  Could not retrieve player count.")
        print(f"  The site may be temporarily unavailable.")

    print(f"\n  Download free:  {SITE_URL}")
    print(f"  Available on Google Play and App Store as MagicSea Online\n")


def main() -> None:
    print(f"Connecting to {SITE_URL} ...")
    players = fetch_player_count(SITE_URL)
    print_status(players)


if __name__ == "__main__":
    main()
