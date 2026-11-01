def get_films_by_provider(movies: list[dict]) -> dict[str, list[dict]]:
    """
    Groups the movies by streaming platform, so you can see which movies
    each platform has. The movie dicts aren't copied; each list holds
    references to the same dicts as `movies`.

    Args:
        movies: The watchlist movies, each with a "providers" list
            (or None if the movie had no TMDB match)

    Returns:
        A dict from provider name to its movies, e.g.
        {"Netflix": [{"title": "Rocky", ...}, ...], "Videoland": [...]}
    """
    films_by_provider = {}
    for movie in movies:
        providers = movie["providers"]
        # Skip movies without a TMDB match; an empty list just loops zero times
        if providers is not None:
            for provider in providers:
                # First time we see this provider, start it with an empty list
                films_by_provider.setdefault(provider, []).append(movie)
    return films_by_provider

def filter_by_subscriptions(user_subscriptions: set[str], films_by_provider: dict[str, list[dict]]) -> dict[str, list[dict]]:
    """
    Keeps only the platforms the user is subscribed to.

    Args:
        user_subscriptions: The names of the user's streaming services, e.g. {"Netflix", "Videoland"}
        films_by_provider: A dict from provider name to its movies, from get_films_by_provider

    Returns:
        The same dict with only the user's platforms, e.g.
        {"Netflix": [{"title": "Rocky", ...}], "Videoland": [...]}
    """
    # Set lookup is O(1), so this is one pass over the platforms
    return {provider: films for provider, films in films_by_provider.items() if provider in user_subscriptions}
