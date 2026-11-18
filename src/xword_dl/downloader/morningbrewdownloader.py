import re

import urllib.parse

from bs4 import BeautifulSoup
from requests.exceptions import HTTPError

from .amuselabsdownloader import AmuseLabsDownloader
from ..util import XWordDLException


class MorningBrewDownloader(AmuseLabsDownloader):
    command = "mb"
    outlet = "Morning Brew"
    outlet_prefix = "Morning Brew"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.session.headers.update(
            {
                "User-Agent": "Googlebot",  # needed to get around privacy consent screen
                "DNT": "1",
            }
        )

    @classmethod
    def matches_url(cls, url_components):
        return (
            "morningbrew.com" in url_components.netloc
            and "brew-crossword" in url_components.path
        )

    def find_latest(self):
        index_url = (
            "https://www.morningbrew.com/games/brew-crossword"
        )
        index_res = self.session.get(index_url, timeout=10)
        index_soup = BeautifulSoup(index_res.text, "html.parser")
        print(index_soup)
        latest_fragment = next(a for a in index_soup.find('a', class_=re.compile("^style__PreviewCardLink")))["href"]
        if not isinstance(latest_fragment, str):
            raise XWordDLException(
                "Could not load latest crossword. Fragment not found."
            )

        latest_absolute = urllib.parse.urljoin(
            "https://www.morningbrew.com", latest_fragment
        )

        landing_page_url = latest_absolute

        return landing_page_url

    def find_solver(self, url):
        res = self.session.get(url, timeout=10)

        try:
            res.raise_for_status()
        except HTTPError:
            raise XWordDLException("Unable to load {}".format(url))

        try:
            # html embed content is encoded -> beautifulsoup parsing would not work
            query_id = list(
                re.findall(
                    r"(http)(s)*(:\/\/morningbrew\.amuselabs\.com\/morningbrew\/crossword)(\?id\=)([0-9a-zA-Z\-]+)(&)amp;(set\=[^&]+)",
                    str(res.text),
                )
            )

            if len(query_id) == 0:
                raise XWordDLException(
                    "Cannot find puzzle at {} -> failed to retrieve amuselabs url from encoded html.".format(
                        url
                    )
                )

            self.id = str(query_id[0][-3])
            matched_url = "".join(query_id[0])

        except KeyError:
            raise XWordDLException("Cannot find puzzle at {}.".format(url))

        return matched_url
