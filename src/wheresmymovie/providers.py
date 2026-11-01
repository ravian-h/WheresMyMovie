
def get_films_by_provider(movies: dict):
    provider_list = {}
    for movie in movies:
        providers = movie["providers"]
        if providers is not None:
            for provider in providers:
                provider_list.setdefault(provider, []).append(movie)
    return provider_list