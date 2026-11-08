from datetime import datetime
from zoneinfo import ZoneInfo

from .amuselabsdownloader import AmuseLabsDownloader


class IndiainExpressMiniDownloader(AmuseLabsDownloader):
    command = "iem"
    outlet = "Indian Express Mini"
    outlet_prefix = "Indian Express Mini"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.picker_url = "https://cdn-in.amuselabs.com/pmm/date-picker?set=indianexpress-crossword-mini"
        self.url_from_id = "https://cdn-in.amuselabs.com/pmm/crossword?id={puzzle_id}&set=indianexpress-crossword-mini"

    def find_by_date(
        self, dt
    ):  # IE mini uses `date=%Y-%m-%d` instead of `id=prefix_%Y%m%d`
        url_formatted_date = dt.strftime("%Y-%m-%d")
        src_formatted_date = dt.strftime("%Y%m%d")
        url = f"https://cdn-in.amuselabs.com/pmm/crossword?set=indianexpress-crossword-mini&date={url_formatted_date}&src=https%3A%2F%2Findianexpress.com%2Fpuzzles-and-games%2Fmini-crossword%2Fie-mini-{src_formatted_date}%2F&uid="

        return url

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
