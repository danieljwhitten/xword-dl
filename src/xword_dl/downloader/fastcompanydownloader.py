from datetime import datetime
from zoneinfo import ZoneInfo


from .amuselabsdownloader import AmuseLabsDownloader


class FastCompanyMiniDownloader(AmuseLabsDownloader):
    command = "fcm"
    outlet = "Fast Company Mini"
    outlet_prefix = "Fast Company Mini"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.picker_url = "https://cdn2.amuselabs.com/puzzleme/date-picker?set=mansueto-minicrossword"
        self.url_from_id = (
            "https://cdn2.amuselabs.com/puzzleme/crossword?id={puzzle_id}&set=mansueto-minicrossword"
        )

    def parse_xword(self, xw_data):
        puzzle = super().parse_xword(xw_data)
        # FC doesn't have date in title or anywhere in puzzle data except a milisecond
        # timestamp buried in the puzzle JSON under 'publishTime'. Assuming today if
        # it is None for a puzzle (like most other fields) [TypeError] or if it passes
        # a string that could have an unknown date format [ValueError]
        try:
            self.date = datetime.fromtimestamp(
                xw_data["publishTime"] / 1000, tz=ZoneInfo(xw_data["publishTimeZone"])
            ).date()
        except (TypeError, ValueError):
            print(f"Could not establish date, assuming today: {datetime.now: %d-$m-%Y}")
            self.date = datetime.today()

        return puzzle


#class YourPuzzleSourceWeekendDownloader(YourPuzzleSourceDownloader):
#    command = "ypsw"
#    outlet = "Your Puzzle Source Weekend"
#    outlet_prefix = "Your Puzzle Source Weekend"
#
#    def __init__(self, **kwargs):
#        super().__init__(**kwargs)
#
#        self.picker_url += "-15x15"
#
#        self.url_from_id = (
#            "https://app.amuselabs.com/app/crossword?id={puzzle_id}&set=yps-15x15"
#        )
