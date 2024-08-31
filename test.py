import os
import requests

# print(os.environ["DJANGO_OMDB_KEY"])

# params = {"apikey": os.environ["DJANGO_OMDB_KEY"], "t": "star wars"}
# resp = requests.get("https://www.omdbapi.com/", params=params)

# print(resp.json())

# shell >>> exec(open('test.py').read())
class OmdbMovie:
    """A simple class to represent movie data coming back from OMDb
    and transform to Python types."""

    def __init__(self, data):
        """Data is the raw JSON/dict returned from OMDb"""
        self.data = data

    def check_for_detail_data_key(self, key):
        """Some keys are only in the detail response, raise an
        exception if the key is not found."""
        
        if key not in self.data:
            raise AttributeError(
                f"{key} is not in data, please make sure this is a detail response."
            )

    @property
    def imdb_id(self):
        return self.data["imdbID"]

    @property
    def title(self):
        return self.data["Title"]

    @property
    def year(self):
        return int(self.data["Year"])

    @property
    def runtime_minutes(self):
        self.check_for_detail_data_key("Runtime")

        rt, units = self.data["Runtime"].split(" ")

        if units != "min":
            raise ValueError(f"Expected units 'min' for runtime. Got '{units}")

        return int(rt)

    @property
    def genres(self):
        self.check_for_detail_data_key("Genre")

        return self.data["Genre"].split(", ")

    @property
    def plot(self):
        self.check_for_detail_data_key("Plot")
        return self.data["Plot"]