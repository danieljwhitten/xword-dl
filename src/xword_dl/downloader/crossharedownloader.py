import datetime
import json

import puz

import re

from bs4 import BeautifulSoup, Tag

from itertools import count

from .basedownloader import BaseDownloader
from ..util import XWordDLException, unidecode


class CrosshareDownloader(BaseDownloader):
    outlet = "CROSSHARE"
    outlet_prefix = "CROSSHARE"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # these values must be overridden by subclasses, if used
        self.landing_url = "https://slate.com/tag/crossword"

    @classmethod
    def matches_url(cls, url_components):
        return ("crosshare.org" in url_components.netloc) and any(
            p in url_components.path for p in ["embed", "crosswords"]
        )

    def find_solver(self, url):
        return url

    def fetch_data(self, solver_url):
        res = self.session.get(solver_url)
        if res.status_code != 200:
            raise XWordDLException(f"Could not fetch solver at {solver_url}")

        soup = BeautifulSoup(res.text, "html.parser")

        script_tag = soup.find("script", id="__NEXT_DATA__")
        if not isinstance(script_tag, Tag):
            raise XWordDLException(
                f"Crossword puzzle not found. Could not find script tag in {solver_url}. Please report this as a bug."
            )

        try:
            return json.loads(script_tag.get_text())["props"]["pageProps"]["puzzle"]
        except (json.JSONDecodeError, KeyError):
            raise XWordDLException(
                f"Unable to find JSON puzzle object in {solver_url}. Please report this as a bug."
            )

    def parse_xword(self, xw_data):
        puzzle = puz.Puzzle()
        puzzle.set_version(b"2.0")
        puzzle.title = xw_data.get("title", "").strip()
        puzzle.author = xw_data.get("authorName", "").strip()
        puzzle.width, puzzle.height = xw_data.get("size", {}).values()

        timestamp = int(xw_data.get("publishTime", 0)) // 1000
        if timestamp and not self.date:
            self.date = datetime.date.fromtimestamp(timestamp)

        grid = xw_data.get("grid", [])
        puzzle.solution = "".join([cell[0] for cell in grid])
        puzzle.fill = re.sub(r"[^.]", "-", puzzle.solution)

        no_rebus = all(len(cell) == 1 for cell in grid)

        if not no_rebus:
            rebus_board_index = count(1)
            rebus_board = [
                0 if len(cell) <= 1 else next(rebus_board_index)
                for cell in xw_data.get("grid", [])
            ]
            rebus_table_index = count(
                0
            )  # rebus table is 0-indexed, rebus board is 1-indexed
            rebus_table = "".join(
                [
                    f"{next(rebus_table_index):2d}:{unidecode(cell)};"
                    if len(cell) > 1
                    else ""
                    for cell in grid
                ]
            )
            puzzle.extensions[b"GRBS"] = bytes(rebus_board)
            puzzle.extensions[b"RTBL"] = rebus_table.encode(puz.ENCODING)
            puzzle._extensions_order.extend([b"GRBS", b"RTBL"])
            puzzle.rebus()

        circled = xw_data.get("cellStyles", {}).get("circle", [])

        if circled:
            markup = bytearray(puzzle.width * puzzle.height)
            for index in circled:
                markup[index] = 0x80
            puzzle.extensions[b"GEXT"] = bytes(markup)
            puzzle._extensions_order.append(b"GEXT")
            puzzle.markup()

        if xw_data.get("isContest"):
            puzzle.solution_state = 0x0002
            puzzle.title += " - no solution provided"

        puzzle.clues.extend(
            [
                c["clue"]
                for c in sorted(
                    xw_data.get("clues", []), key=lambda c: (c["num"], c["dir"])
                )
            ]
        )

        return puzzle
