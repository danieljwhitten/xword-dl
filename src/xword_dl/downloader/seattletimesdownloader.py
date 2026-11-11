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
    command = "stmn"
    outlet = "Seattle Times Mini"
    outlet_prefix = "Seattle Times Mini"
    url_set = "seattletimes-crossword-mini"


class SeattleTimesMidiDownloader(SeattleTimesDownloader):
    command = "stmd"
    outlet = "Seattle Times Midi"
    outlet_prefix = "Seattle Times Midi"
    url_set = "seattletimes-crossword-midi"


class SeattleTimesModernMidiDownloader(SeattleTimesDownloader):
    command = "stmmd"
    outlet = "Seattle Times Modern Midi"
    outlet_prefix = "Seattle Times Modern Midi"
    url_set = "seattletimes-contemporary-midi-crossword"


# ST syndicates Penny Dell for its 'Large' crossword via Amuselabs
class PennyDellDownloader(SeattleTimesDownloader):
    command = "pd"
    outlet = "Penny Dell"
    outlet_prefix = "Penny Dell"
    url_set = "seattletimes-crossword-large"
