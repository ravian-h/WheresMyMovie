import time

import requests
import re
from bs4 import BeautifulSoup




def fetch_watchlist(username="ravianmh"):
    """
    Requests the html page of the watchlist of the username from Letterboxd.
    Finds the movies on the watchlist and adds them to a dictionary
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
        movies = soup.find_all("div", attrs={"data-component-class": "LazyPoster"})

        if not movies:
            break
        else:
            for movie in movies:
                slug = movie["data-item-slug"]
                movie_and_year = movie["data-item-full-display-name"]

                match = re.search(r"\((\d{4})\)$", movie_and_year)
                if match:
                    year = match.group(1)  # the captured 4 digits
                    title = movie_and_year[:match.start()].strip()  # everything before the match

                all_movies.append({"title": title, "year": year, "slug": slug})
            page_number += 1
        time.sleep(3)

    return all_movies