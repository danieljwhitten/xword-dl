import datetime
import re
from bs4 import BeautifulSoup, Tag

from .crossharedownloader import CrosshareDownloader
from ..util import XWordDLException

class SlateDownloader(CrosshareDownloader):
    command = "sla"
    outlet = "Slate"
    outlet_prefix = "Slate"
    play_url_prefix = "crossword-slate-daily-puzzle"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.landing_url = "https://slate.com/tag/crossword"

    @classmethod
    def matches_url(cls, url_components):
        return ("slate.com" in url_components.netloc) and (
            cls.play_url_prefix in url_components.path
        )

    def date_from_url(self, url):
        match = re.search(r"([a-z]{3}-\d{1,2}-\d{4})\.html$", url, re.IGNORECASE)
        if match:
            self.date = datetime.datetime.strptime(match.group(1), "%b-%d-%Y").date()

    def find_latest(self) -> str:
        link_regex = rf"^https://slate.com/life/\d{{4}}/\d{{2}}/.*?{self.play_url_prefix}-[a-z]{{3}}-\d{{2}}-\d{{4}}\.html"

        res = self.session.get(self.landing_url)
        soup = BeautifulSoup(res.text, "html.parser")
        link_tag = soup.find("a", href=re.compile(link_regex))

        if not isinstance(link_tag, Tag):
            raise XWordDLException(
                f"Could not find any appropriate links on {self.landing_url}. Please report this as a bug."
            )
        link = str(link_tag.get("href", ""))
        self.date_from_url(link)
        return link

    def find_by_date(self, dt):
        return f"https://slate.com/life/{dt:%Y}/{dt:%m}/{self.play_url_prefix}-{dt.strftime('%b').lower()}-{dt.day}-{dt:%Y}.html"

    def find_solver(self, url) -> str:
        self.date_from_url(url)
        res = self.session.get(url)
        soup = BeautifulSoup(res.text, "html.parser")
        embed_tag = soup.find("div", attrs={"data-embed-url": True})

        if not isinstance(embed_tag, Tag):
            raise XWordDLException(
                f"No embed URL found on puzzle page {url}. Please report this as a bug."
            )
        return str(embed_tag.get("data-embed-url", ""))
   
    def parse_xword(self, xw_data):
        puzzle = super().parse_xword(xw_data)
        # Slate has a generic author and lists author under guestConstructor
        puzzle.author = (
            xw_data.get("authorName", "").strip()
            if xw_data.get("guestConstructor", "") == ""
            else xw_data.get("guestConstructor").strip()
        )
        return puzzle

class SlateMiniDownloader(SlateDownloader):
    command = "slam"
    outlet = "Slate Mini"
    outlet_prefix = "Slate Mini"
    play_url_prefix = "crossword-slate-mini-daily-puzzle"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.landing_url = "https://slate.com/tag/mini-crossword"
