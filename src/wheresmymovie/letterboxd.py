import time

import requests
import re
from bs4 import BeautifulSoup

def fetch_watchlist(username="ravianmh"):
    """
    Requests the HTML page of the watchlist of a user (username) from Letterboxd.
    Extracts details from each movie into a dictionary, and adding them to a list.

    Args:
        username: The Letterboxd username from which the watchlist will get fetched

    Returns: 
        A list of dicts, each with the keys: title (str), year (str or None), slug (str)
    """
    page_number = 1
    all_movies = []
    headers = {
        "User-Agent": "WheresMyMovie/0.1 (personal project)"
    }   

    while True:
        url = f"https://letterboxd.com/{username}/watchlist/page/{page_number}/"
        response = requests.get(url, headers=headers)

        soup = BeautifulSoup(response.text, "html.parser")

        # Each movie poster on the watchlist page is a div like:
        #   <div data-component-class="LazyPoster"...
        #        data-item-slug="rocky"...
        #        data-item-full-display-name="Rocky (1976)"... >
        # An empty result means we've gone past the last page   
        movies = soup.find_all("div", attrs={"data-component-class": "LazyPoster"})

        if not movies:
            break
    
        for movie in movies:
            slug = movie["data-item-slug"]
            movie_and_year = movie["data-item-full-display-name"]

            # Letterboxd's titles look like "Title (year)". Extract title and year (4 digits at the end) seperatly
            match = re.search(r"\((\d{4})\)$", movie_and_year)
            if match:
                year = match.group(1)  # the captured 4 digits
                title = movie_and_year[:match.start()].strip()  # everything before the match
            else: 
                year = None
                title = movie_and_year

            all_movies.append({"title": title, "year": year, "slug": slug})
        page_number += 1
        time.sleep(1) # used to not hammer Letterboxd's servers with rapid requests

    return all_movies