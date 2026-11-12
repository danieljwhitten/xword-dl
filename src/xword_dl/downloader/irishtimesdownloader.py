from datetime import datetime
from zoneinfo import ZoneInfo

from .amuselabsdownloader import AmuseLabsDownloader


class IrishTimesDownloader(AmuseLabsDownloader):
    url_base = "https://cdn-ie.amuselabs.com/irishtimes/"
    url_set = None
    id_prefix = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.picker_url = f"{self.url_base}date-picker?set={self.url_set}"
        self.url_from_id = (
            f"{self.url_base}crossword?id={{puzzle_id}}&set={self.url_set}"
        )

    def find_by_date(
        self, dt
    ):  # IT allows `date=%Y-%m-%d` instead of `id=prefix_%Y%m%d`
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


class IrishTimesMiniDownloader(IrishTimesDownloader):
    command = "it8"
    outlet = "Irish Times Daily Eight"
    outlet_prefix = "Irish Times Daily Eight"
    url_set = "irishtimes-daily8"


class IrishTimesSimplexDownloader(IrishTimesDownloader):
    command = "its"
    outlet = "Irish Times Simplex"
    outlet_prefix = "Irish Times Simplex"
    url_set = "irishtimes-simplex"


class IrishTimesCrosaireDownloader(IrishTimesDownloader):
    command = "itc"
    outlet = "Irish Times Crosaire"
    outlet_prefix = "Irish Times Crosiare"
    url_set = "irishtimes-crosaire"
