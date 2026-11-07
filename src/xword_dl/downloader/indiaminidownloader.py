from .amuselabsdownloader import AmuseLabsDownloader


class IndiaMiniDownloader(AmuseLabsDownloader):
    command = "im"
    outlet = "India Mini"
    outlet_prefix = "India Mini"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.picker_url = "https://puzzleme.amuselabs.com/pmm/date-picker?set=pm-content-crossword-india-mini"
        self.url_from_id = "https://puzzleme.amuselabs.com/pmm/crossword?id={puzzle_id}&set=pm-content-crossword-india-mini"

    def find_by_date(self, dt):
        url_formatted_date = dt.strftime("%Y%m%d")
        self.id = "al-crossword-mini-" + url_formatted_date

        return self.find_puzzle_url_from_id(self.id)
