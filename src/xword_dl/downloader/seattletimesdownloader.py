from .amuselabsdownloader import AmuseLabsDownloader


class SeattleTimesDownloader(AmuseLabsDownloader):
    url_base = "https://seattletimes.amuselabs.com/puzzleme/"
    url_set = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.picker_url = f"{self.url_base}date-picker?set={self.url_set}"
        self.url_from_id = (
            f"{self.url_base}crossword?id={{puzzle_id}}&set={self.url_set}"
        )

    def find_by_date(
        self, dt
    ):  # ST allows `date=%Y-%m-%d` instead of `id=prefix_%Y%m%d`
        return f"{self.url_base}crossword?set={self.url_set}&date={dt:%Y-%m-%d}"


class SeattleTimesMiniDownloader(SeattleTimesDownloader):
    command = "stm"
    outlet = "Seattle Times Mini"
    outlet_prefix = "Seattle Times Mini"
    url_set = "crossword-mini"

    def find_by_date(self, dt):
        return f"{self.url_base}crossword?set={self.url_set}&date={dt:%Y-%m-%d}"
