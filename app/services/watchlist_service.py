import json
from pathlib import Path


class WatchlistService:

    def __init__(self):
        self.file = Path("app/config/watchlist.json")

    def get_symbols(self) -> list[str]:

        with open(self.file, "r") as f:
            return json.load(f)