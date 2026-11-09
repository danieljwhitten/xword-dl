import datetime
from urllib.parse import urlsplit, parse_qsl, urlencode

import dateparser.search

from .amuselabsdownloader import AmuseLabsDownloader


class DailyBeastDownloader(AmuseLabsDownloader):
    command = "db"
    outlet = "Daily Beast"
    outlet_prefix = "Daily Beast"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.picker_url = "https://cdn3.amuselabs.com/tdb/date-picker?set=tdb"
        self.url_from_id = (
            "https://cdn3.amuselabs.com/tdb/crossword?id={puzzle_id}&set=tdb"
        )

    # Replace id= query compenent with date= query component and add token
    def find_by_date(self, dt):
        self.get_and_add_picker_token()
        latest_url_split = urlsplit(self.url_from_id)
        query = parse_qsl(latest_url_split.query)
        query = dict(query)
        del query["id"]
        query["date"] = f"{dt:%Y-%m-%d}"
        print(query)
        date_url = latest_url_split._replace(
            query=urlencode(list(query.items()))
        ).geturl()
        print(date_url)
        return date_url

    def parse_xword(self, xw_data):
        puzzle = super().parse_xword(xw_data)

        # Daily Beast puzzle IDs don't include the date.
        # This pulls it out of the puzzle title (with periods removed because
        # they mess with the date parser)

        possible_dates = dateparser.search.search_dates(puzzle.title.replace(".", ""))

        if possible_dates:
            self.date = possible_dates[-1][1]
        else:
            self.date = datetime.datetime.today()

        return puzzle
