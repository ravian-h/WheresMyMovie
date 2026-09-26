from wheresmymovie.letterboxd import fetch_watchlist

movies = fetch_watchlist()
print(len(movies))
for movie in movies:
    print(movie)
