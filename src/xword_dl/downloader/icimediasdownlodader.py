from .amuselabsdownloader import AmuseLabsDownloader


class ICIMediasDownloader(AmuseLabsDownloader):
    command = "ici"
    outlet = "ICI Médias"
    outlet_prefix = "ICI Médias"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.picker_url = "https://cdn2.amuselabs.com/pmm/date-picker?set=icimedias"
        self.url_from_id = (
            "https://cdn2.amuselabs.com/pmm/crossword?id={puzzle_id}&set=icimedias"
        )

    def find_by_date(self, dt):
        return (
            f"https://cdn2.amuselabs.com/pmm/crossword?set=icimedias&date={dt:%Y-%m-%d}"
        )
