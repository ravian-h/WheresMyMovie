import requests

def search_movie(s: requests.Session, title: str, year: str | None, api_key: str) -> int | None:
    """
    Searches TMDB for a movie by its title (and year, if known).
    Passes the search results to pick_best_match to choose the right movie.

    Args:
        s: The requests Session used to make the request to TMDB
        title: The title of the movie as shown on Letterboxd
        year: The release year as a 4-digit string, or None if unknown
        api_key: The TMDB API key, loaded from the .env file

    Returns:
        The TMDB ID (int) of the best matching movie, or None if no match was found
    """
    # requests builds and URL-encodes the query string from this dict,
    # so titles with spaces or special characters (&, ?, é) work as-is.
    # If year is None, requests leaves primary_release_year out of the URL.
    params={"api_key": api_key, "query": title, "primary_release_year": year}

    response = s.get(
        "https://api.themoviedb.org/3/search/movie",
        params=params
    )
    # Raise an error on a bad response (e.g. 401 for a wrong API key),
    # instead of failing later with a confusing KeyError
    response.raise_for_status()

    # Turn the JSON text of the response into a Python dict:
    #   {"page": 1, "results": [{"id": 1366, "title": "Rocky", ...}, ...], ...}
    data = response.json()

    best_movie_match = pick_best_match(data, title, year)
    return best_movie_match

def pick_best_match(data: dict, title: str, year: str | None) -> int | None:
    """
    Picks the movie from the TMDB search results that best matches the Letterboxd movie.
    A movie matches if its title and release year are the same. If several movies
    match (e.g. a famous film and an obscure one with the same name), the one with
    the most votes is chosen.

    Args:
        data: The TMDB search response as a dict, with the matching movies under "results"
        title: The title of the movie as shown on Letterboxd
        year: The release year as a 4-digit string, or None if unknown

    Returns:
        The TMDB ID (int) of the best matching movie, or None if no movie matched
    """
    results = data["results"]

    # Match on title (English or original) and year; release_date looks like "1976-12-03"
    matches = []
    for movie in results:
        if (movie["original_title"].lower() == title.lower() or movie["title"].lower() == title.lower()) and (movie["release_date"][:4] == year or year is None):
            matches.append(movie)

    # Pick the match with the most votes; -1 so a movie with 0 votes can still win
    max_votes = -1
    max_movie_id = None
    for movie in matches: 
        if movie["vote_count"] > max_votes:
            max_votes = movie["vote_count"]
            max_movie_id = movie["id"]
    return max_movie_id