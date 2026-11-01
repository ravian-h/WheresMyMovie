import os

import requests
from dotenv import load_dotenv

from wheresmymovie.letterboxd import fetch_watchlist
from wheresmymovie.tmdb import search_movie, get_providers
from wheresmymovie.providers import get_films_by_provider, filter_by_subscription


COUNTRY = "NL"
MY_SUBSCRIPTIONS = {"Netflix", "Videoland"}

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
        movie["providers"] = get_providers(s, movie["tmdb_id"], COUNTRY)
    else:
        movie["providers"] = None
    print(f'{movie["title"]} ({movie["year"]}) -> {movie["tmdb_id"]}')
    print(movie["providers"])

films_by_provider = get_films_by_provider(movies) 
set_films_by_provider = set(films_by_provider)

my_films = filter_by_subscriptions(MY_SUBSCRIPTIONS, films_by_provider)