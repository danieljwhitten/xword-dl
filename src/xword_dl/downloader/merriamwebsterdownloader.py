from .amuselabsdownloader import AmuseLabsDownloader


class MerriamWebsterDownloader(AmuseLabsDownloader):
    command = "mw"
    outlet = "Merriam Webster Missing Letter"
    outlet_prefix = "Merriam Webster"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.picker_url = "https://cdn2.amuselabs.com/mw/date-picker?set=mw-tml-daily"
        self.url_from_id = (
            "https://cdn2.amuselabs.com/mw/crossword?id={puzzle_id}&set=mw-tml-daily"
        )

    def find_by_date(self, dt):
        url_formatted_date = dt.strftime("%Y%m%d")
        self.id = "mw_" + url_formatted_date

        return self.find_puzzle_url_from_id(self.id)
