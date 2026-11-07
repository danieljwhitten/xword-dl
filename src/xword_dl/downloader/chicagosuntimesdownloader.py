from .amuselabsdownloader import AmuseLabsDownloader


class ChicagoSunTimesMiniDownloader(AmuseLabsDownloader):
    command = "cstm"
    outlet = "Chicago Sun Times Chicago Mini"
    outlet_prefix = "Chicago Mini"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.picker_url = "https://chicagopm.amuselabs.com/puzzleme/date-picker?set=chicagopm-chicago-mini"
        self.url_from_id = "https://chicagopm.amuselabs.com/puzzleme/crossword?id={puzzle_id}&set=chicagopm-chicago-mini"

    def find_by_date(self, dt):
        url_formatted_date = dt.strftime("%Y%m%d")
        self.id = "chicagopm_" + url_formatted_date

        return self.find_puzzle_url_from_id(self.id)
