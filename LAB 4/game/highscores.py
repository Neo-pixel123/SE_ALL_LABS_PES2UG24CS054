import json
import os
from datetime import date

# Top-5 high score table persisted across sessions (Task 3).
MAX_ENTRIES = 5
DEFAULT_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "highscores.json")


class HighScores:
    def __init__(self, path=DEFAULT_PATH):
        self.path = path
        self.entries = self._load()

    def _load(self):
        try:
            with open(self.path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError, OSError):
            return []
        # Keep only well-formed entries in case the file was edited by hand.
        valid = [e for e in data if isinstance(e, dict) and isinstance(e.get("score"), int)]
        return sorted(valid, key=lambda e: e["score"], reverse=True)[:MAX_ENTRIES]

    def _save(self):
        try:
            with open(self.path, "w", encoding="utf-8") as f:
                json.dump(self.entries, f, indent=2)
        except OSError:
            pass  # A read-only folder shouldn't crash the game.

    def best(self):
        return self.entries[0]["score"] if self.entries else 0

    def submit(self, score):
        """Add a score; returns its rank index (0-4) if it made the table, else None."""
        entry = {"score": score, "date": date.today().isoformat()}
        self.entries.append(entry)
        self.entries.sort(key=lambda e: e["score"], reverse=True)
        self.entries = self.entries[:MAX_ENTRIES]
        self._save()
        for i, e in enumerate(self.entries):
            if e is entry:
                return i
        return None
