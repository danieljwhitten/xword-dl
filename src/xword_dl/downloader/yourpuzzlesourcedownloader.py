from datetime import datetime, timezone


from .amuselabsdownloader import AmuseLabsDownloader


class YourPuzzleSourceDownloader(AmuseLabsDownloader):
    command = "yps"
    outlet = "Your Puzzle Source"
    outlet_prefix = "Your Puzzle Source"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.picker_url = "https://app.amuselabs.com/app/date-picker?set=yps"
        self.url_from_id = (
            "https://app.amuselabs.com/app/crossword?id={puzzle_id}&set=yps"
        )

    def parse_xword(self, xw_data):
        puzzle = super().parse_xword(xw_data)

        # YPS doesn't have date in title or anywhere in puzzle data except a milisecond
        # timestamp buried in the puzzle JSON under 'publishTime'. Assuming today if
        # it is None for a puzzle (like most other fields) [TypeError] or if it passes
        # a string that could have an unknown date format [ValueError]
        try:
            self.date = datetime.fromtimestamp(
                xw_data["publishTime"] / 1000, tz=timezone.utc
            ).date()
        except (TypeError, ValueError):
            print(f"Could not establish date, assuming today: {datetime.now: %d-$m-%Y}")
            self.date = datetime.today()

        return puzzle
