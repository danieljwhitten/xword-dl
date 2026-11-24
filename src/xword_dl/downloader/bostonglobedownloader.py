import requests


from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from .puzzmodownloader import PuzzmoDownloader
from ..util import join_bylines, XWordDLException


class BostonGlobeDownloader(PuzzmoDownloader):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        headers = headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:156.0) Gecko/20100101 Firefox/156.0",
            "Accept": "*/*",
            "Content-Type": "application/json",
            "Origin": "https://www.puzzmo.com",
            "Referer": "https://www.puzzmo.com/",
            "auth-provider": "custom",
            "authorization": "Bearer ~",
        }

        self.session.headers.update(headers)

        self.puzzle_set = ""
        self.date_string = ""

    # Not relevant as solver is pulled from endpoint in fetch_data
    def find_solver(self, url):
        if not self.date_string:
            return self.find_latest()
        return url

    def fetch_data(self, solver_url):
        ENDPOINT = "https://api.puzzmo.com/graphql"

        QUERY = """
            mutation embedConfigBootstrapQueryMutation($id: ID!, $options: JSON) {
                createGameplayForEmbedConfig(id: $id, options: $options) {
                    config { id puzzleTitle redirectTo flags hostContext type }
                    gameplay {
                        slug completed pointsAwarded
                        puzzle {
                            id name emoji difficulty seriesNumber puzzle
                            game { displayName assetsBaseURL assetsPath jsPath cssPath }
                            authors { name publishingName }
                        }
                    }
                    userStateID
                    embedSessionToken
                }
            }   
        """

        payload = {
            "query": QUERY,
            "variables": {
                "id": self.puzzle_set,
                "options": {
                    "embedID": self.puzzle_set,
                    "dateKey": self.date_string,
                },
            },
        }

        try:
            resp = self.session.post(
                ENDPOINT,
                params={
                    "op": "embedConfigBootstrapQueryMutation"
                },  # matches ?op=... in the curl URL
                json=payload,
                timeout=30,
            )
            resp.raise_for_status()
        except requests.exceptions.HTTPError as http_err:
            raise XWordDLException(f"HTTP error occurred: {http_err}")
        except requests.exceptions.RequestException as err:
            raise XWordDLException(f"Network or connection error occurred: {err}")

        response = resp.json()
        if response.get("errors"):
            error = response["message"]
            raise XWordDLException(f"Puzzmo error: {error}")

        try:
            node = response["data"]["createGameplayForEmbedConfig"]
            xw_data = node["gameplay"]["puzzle"]
        except KeyError:
            raise XWordDLException("Unable to extract puzzle data.")

        return xw_data

    def parse_xword(self, xw_data):
        xd_data = xw_data["puzzle"]
        puzzle = self.parse_xd_format(xd_data)
        # Override xd metadata with more reliable API results
        puzzle.title = xw_data.get("name", "")
        puzzle.author = join_bylines(
            [a.get("publishingName") or a.get("name") for a in xw_data["authors"]]
        )
        return puzzle


class BostonGlobeSundayDownloader(BostonGlobeDownloader):
    command = "bgs"
    outlet = "Boston Globe Sunday"
    outlet_prefix = "Boston Globe"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.puzzle_set = "bg-crossword"

    def find_latest(self):
        # BG only publishes unique puzzle on Sundays, other days syndicate Universal
        today = datetime.now(ZoneInfo("America/New_York")).date()
        offset = (
            today.weekday() - 6
        ) % 7  # 0 if today is Sunday, else days since last Sunday
        latest_sunday = today - timedelta(days=offset)
        self.date = latest_sunday
        return self.find_by_date(latest_sunday)

    def find_by_date(self, dt):
        self.date_string = dt.isoformat()

        # In practice, setting the date_string above does everything we need here.
        return ""
