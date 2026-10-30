from wheresmymovie.letterboxd import fetch_watchlist
from wheresmymovie.tmdb import search_movie
import requests
import os 
from dotenv import load_dotenv

load_dotenv()
token = os.getenv("TMBD_READ_TOKEN")
url = "https://api.themoviedb.org/3/movie/movie_id?language=en-US"
s = requests.Session()
headers = {
    "accept": "application/json",
    "Authorization": f"Bearer {token}"
}
s.headers.update(headers)

movies = fetch_watchlist()
print(len(movies))
for movie in movies:
    print(movie)

for movie in movies:
    title = movie.get("title")
    year = movie.get("year")
    slug = movie.get("slug")
    movie_id = search_movie(s, slug, year)  