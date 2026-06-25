# Roblox Presence Tracker → Discord Webhook

Checks 5 Roblox accounts every 5 minutes and pings your Discord webhook when
someone goes online, starts/stops playing a game, or goes offline.

## Setup (5 min)

1. Create a **new GitHub repo** (can be private), e.g. `roblox-tracker`.
2. Upload these 3 files keeping the same folder structure:
   - `track.py`
   - `state.json`
   - `.github/workflows/track.yml`
3. That's it — GitHub Actions will automatically start running it every
   5 minutes once it's pushed to the repo (uses your repo's free Actions
   minutes, this script costs basically nothing to run).

## Notes

- The webhook URL and usernames are hardcoded at the top of `track.py`.
  Edit that list any time to add/remove people you're tracking.
- The bot tracks state in `state.json` and commits updates to it automatically
  so it remembers who was online last check (so you don't get spammed every
  5 minutes while someone stays online — only on status *changes*).
- If you ever want to check immediately instead of waiting for the next
  5-min run: go to your repo → **Actions** tab → **Roblox Presence Tracker**
  → **Run workflow**.
- Roblox's presence API is public and doesn't need login, so no extra
  credentials needed.

## Changing who's tracked

Open `track.py`, edit the `USERNAMES` list near the top:

```python
USERNAMES = [
    "freddyfazbearcool091",
    "rar56705",
    "FalcoEve",
    "holabrandon2020",
    "Desne1207",
]
```
