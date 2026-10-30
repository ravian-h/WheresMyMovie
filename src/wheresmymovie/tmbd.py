import requests

BASE_URL = "https://api.themoviedb.org/3/search/movie?"

url = "https://api.themoviedb.org/3/search/movie?query=rocky&include_adult=true&language=en-US&primary_release_year=1976&page=1"

def search_movie(s: requests.Session, slug: str, year: int | None):
    title = slug.replace("&", "%26")

    if year == None:
        url = BASE_URL + f"query={slug}&page=1"
    else: 
        url = BASE_URL + f"query={slug}&primary_release_year={year}&page=1"

    response_object = s.get(url)

    movie_id = extract_id(response_object)
    return movie_id

def extract_id(response_object):
    results = response_object.get("results")
    first_movie = results[0]
    movie_id = first_movie.get("id")
    return movie_id