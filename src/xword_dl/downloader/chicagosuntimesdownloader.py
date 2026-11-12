from .amuselabsdownloader import AmuseLabsDownloader

class ChicagoSunTimesDownloader(AmuseLabsDownloader):
    url_base = "https://chicagopm.amuselabs.com/puzzleme/"
    url_set = None
    id_prefix = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.picker_url = f"{self.url_base}date-picker?set={self.url_set}"
        self.url_from_id = (
            f"{self.url_base}crossword?id={{puzzle_id}}&set={self.url_set}"
        )

    def find_by_date(self, dt):
        url_formatted_date = dt.strftime("%Y%m%d")
        self.id = f"{self.id_prefix}{url_formatted_date}"

        return self.find_puzzle_url_from_id(self.id)


class ChicagoSunTimesMiniDownloader(ChicagoSunTimesDownloader):
    command = "cstm"
    outlet = "Chicago Sun-Times Chicago Mini"
    outlet_prefix = "Chicago Mini"
    url_set = "chicagopm-chicago-mini"
    id_prefix = "chicagopm_"
