from .amuselabsdownloader import AmuseLabsDownloader


class AtlanticDownloader(AmuseLabsDownloader):
    command = "pp"
    outlet = "People Puzzler"
    outlet_prefix = "People"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.picker_url = (
            "https://pplmag.amuselabs.com/pplmag/date-picker?set=pplmag-site-puzzler"
        )
        self.url_from_id = "https://pplmag.amuselabs.com/pplmag/crossword?id={puzzle_id}&set=pplmag-site-puzzler"

    def find_by_date(self, dt):
        return f"https://pplmag.amuselabs.com/pplmag/crossword?date={dt:%Y-%m-%d}&set=pplmag-site-puzzler"
