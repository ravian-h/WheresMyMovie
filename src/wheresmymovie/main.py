import os

import requests
from dotenv import load_dotenv

from wheresmymovie.letterboxd import fetch_watchlist
from wheresmymovie.tmdb import search_movie
from wheresmymovie.tmdb import get_providers


load_dotenv()
token = os.getenv("TMDB_READ_TOKEN")

# Every request made with this session sends the token, so we only set it once
s = requests.Session()
s.headers.update({"Authorization": f"Bearer {token}"})

movies = fetch_watchlist()
print(f"{len(movies)} movies on watchlist")

for movie in movies:
    movie["tmdb_id"] = search_movie(s, movie["title"], movie["year"])
    if movie["tmdb_id"] is not None:
        providers = get_providers(s, movie["tmdb_id"], "NL")
    print(f'{movie["title"]} ({movie["year"]}) -> {movie["tmdb_id"]}')
    print(providers)

