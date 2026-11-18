import datetime
import json
import urllib.parse

import puz
import requests

import re

from bs4 import BeautifulSoup, Tag

from collections import deque
from typing import List

from .basedownloader import BaseDownloader
from ..util import XWordDLException, unidecode


class SlateDownloader(BaseDownloader):
    command = "slate"
    outlet = "Slate"
    outlet_prefix = "Slate" 

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.id = None

        # these values must be overridden by subclasses, if used
        self.landing_url = "https://slate.com/life/crossword"
        self.play_url_prefix = "crossword-slate-daily-puzzle"

    def find_latest(self) -> str:
        
        link_regex = rf"^https://slate.com/life/\d{{4}}/\d{{2}}/.*?{self.play_url_prefix}-[a-z]{{3}}-\d{{2}}-\d{{4}}\.html"

        res = self.session.get(self.landing_url)
        soup = BeautifulSoup(res.text, 'html.parser')
        link_tag = soup.find('a', href=re.compile(link_regex))
        
        if link_tag:
            link = link_tag['href']
            match = re.search(r"([a-z]{3}-\d{1,2}-\d{4})\.html$", link, re.IGNORECASE)
            if match:
                self.date  = datetime.datetime.strptime(match.group(1), "%b-%d-%Y")
                print(self.date)
            return link
        else:
            raise XWordDLException(
                    "Could not find any appropriate links on {self.landing_url}. Please report this as a bug."
                )


    def find_solver(self, url):
        res = self.session.get(url)
        soup = BeautifulSoup(res.text, 'html.parser')
        embed_link = soup.find('div', attrs={"data-embed-url": True})['data-embed-url']
        if embed_link:
            return embed_link 
        else:
            raise XWordDLException(
                    f"No embed URL found on puzzle page {url}. Please report this as a bug."
                )

    def fetch_data(self, solver_url):
        res = self.session.get(solver_url)
        if res.status_code != 200:
            raise XWordDLException(f"Could not fetch solver at {solver_url}")

        soup = BeautifulSoup(res.text, "html.parser")
        if not isinstance(soup, Tag):
            raise XWordDLException(
                f"Crossword puzzle not found. Could not parse HTML at {solve_url}."
            )

        script_tag = soup.find("script", id="__NEXT_DATA__")
        if not isinstance(script_tag, Tag):
             raise XWordDLException(
                f"Crossword puzzle not found. Could not find script tag in {solver_url}. Please report this as a bug."
            )

        try:
            return json.loads(script_tag.text)['props']['pageProps']['puzzle']
        except (json.JSONDecodeError, KeyError):
            raise XWordDLException(f"Unable to find JSON puzzle object in {solver_url}. Please report this as a bug.")

    def parse_xword(self, xw_data):
        puzzle = puz.Puzzle()
        puzzle.title = xw_data.get("title", "").strip()
        # Slate has a generic author and lists author under guestConstructor
        puzzle.author = xw_data.get("authorName", '').strip() if xw_data.get("guestConstructor", '') == '' else xw_data.get("guestConstructor").strip()
        puzzle.width, puzzle.height = xw_data.get("size", {}).values()

        timestamp = int(xw_data.get("publishTime", 0)) // 1000
        if timestamp and not self.date:
            self.date = datetime.date.fromtimestamp(timestamp)

        grid = xw_data.get('grid', [])
        puzzle.solution = "".join([cell[0] for cell in grid])
        puzzle.fill = re.sub(r"[^.]","-",puzzle.solution)

        no_rebus = all(len(cell) == 1 for cell in grid)

        if not no_rebus:
            rebus_index = count(1)
            rebus_board = [0 if len(cell) <= 1 else next(rebus_index) for cell in xw_data.get('grid', [])]
            rebus_index = count(1)
            rebus_table = "".join([f'{next(rebus_index):2d}:{unidecode(cell)};' if len(cell) > 1 else '' for cell in xw_data.get(grid, [])]) 
            puzzle.extensions[b"GRBS"] = bytes(rebus_board)
            puzzle.extensions[b"RTBL"] = rebus_table.encode(puz.ENCODING)
            puzzle._extensions_order.extend([b"GRBS", b"RTBL"])
            puzzle.rebus()

        circled = xw_data.get('cellStyles', {}).get('circle', [])
        no_circles = len(circled) == 0

        if not no_circles:
            markup = b'\x00' * puzzle.width * puzzle.height
            for index in circled:
                markup[index] = b'\x80'
            puzzle.extensions[b"GEXT"] = markup
            puzzle._extensions_order.append(b"GEXT")
            puzzle.markup()
            
        if xw_data.get('isContest'): 
            puzzle.solution_state = 0x0002
            puzzle.title += " - no solution provided"

        puzzle.clues.extend([c["clue"] for c in sorted(xw_data.get("clues"), key = lambda c: (c['num'], c['dir']))])
        
        return puzzle

    def pick_filename(self, puzzle, **kwargs):
        if not self.date and self.id:
            self.guess_date_from_id(self.id)
        return super().pick_filename(puzzle, **kwargs)

