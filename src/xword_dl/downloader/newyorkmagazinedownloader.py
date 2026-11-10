from .amuselabsdownloader import AmuseLabsDownloader


class NewYorkMagazineDownloader(AmuseLabsDownloader):
    command = "nym"
    outlet = "New York Magazine"
    outlet_prefix = "New York Magazine"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.picker_url = (
            "https://cdn3.amuselabs.com/nymag/date-picker?set=nymag-nym weekly"
        )
        self.url_from_id = "https://cdn3.amuselabs.com/nymag/crossword?id={puzzle_id}&set=nymag-nym weekly"
