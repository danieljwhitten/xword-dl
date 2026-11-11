from datetime import datetime
from zoneinfo import ZoneInfo

from .amuselabsdownloader import AmuseLabsDownloader


class HindustanTimesDownloader(AmuseLabsDownloader):
    url_set = None
    url_base = "https://cdn-in.amuselabs.com/pmm/"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.picker_url = f"{self.url_base}date-picker?set={self.url_set}"
        self.url_from_id = (
            f"{self.url_base}crossword?id={{puzzle_id}}&set={self.url_set}"
        )

    def find_by_date(
        self, dt
    ):  # HT allows `date=%Y-%m-%d` instead of `id=prefix_%Y%m%d`
        return f"{self.url_base}crossword?set={self.url_set}&date={dt:%Y-%m-%d}"

    def parse_xword(self, xw_data):
        puzzle = super().parse_xword(xw_data)
        # Time zone can throw off date processing, try to extract timestamp and time
        # zone from data, otherwise leave as-is
        try:
            self.date = datetime.fromtimestamp(
                xw_data["publishTime"] / 1000, tz=ZoneInfo(xw_data["publishTimeZone"])
            ).date()
        except (TypeError, ValueError):
            pass

        return puzzle


class HindustanTimesMiniDownloader(HindustanTimesDownloader):
    command = "htm"
    outlet = "Hindustan Times Mini"
    outlet_prefix = "Hindustan Times Mini"
    url_set = "hindustantimes-crossword-mini"
