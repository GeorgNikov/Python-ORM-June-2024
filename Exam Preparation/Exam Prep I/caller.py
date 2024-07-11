import os

import django
from django.db.models import Q, Count, Avg, F

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()


# Import your models here
from main_app.models import Director, Actor, Movie


# Create queries within functions
def get_directors(search_name=None, search_nationality=None):
    result = []
    if search_name is None and search_nationality is None:
        return ''

    # query = Q()

    if search_name and search_nationality is None:
        query = Q(full_name__icontains=search_name)
    elif search_name is None and search_nationality:
        query = Q(nationality__icontains=search_nationality)
    else:
        query = Q(full_name__icontains=search_name) & Q(nationality__icontains=search_nationality)

    directors = Director.objects.filter(query).order_by('full_name')

    for d in directors:
        result.append(f"Director: {d.full_name}, "
                      f"nationality: {d.nationality}, "
                      f"experience: {d.years_of_experience}")

    if not result:
        return ''

    return '\n'.join(result)


def get_top_director():
    top_director = Director.objects.get_directors_by_movies_count().first()

    if not top_director:
        return ''

    return f"Top Director: {top_director.full_name}, movies: {top_director.movie_count}."


def get_top_actor():
    actor = Actor.objects.annotate(
        movie_count=Count('movies_starring'),
        average_rating=Avg('movies_starring__rating')
    ).order_by(
        '-movie_count',
        'full_name'
    ).first()

    if not actor or not actor.movies_starring.all():
        return ''

    movie_starring = []
    for movie in actor.movies_starring.all():
        movie_starring.append(movie.title)

    return (f"Top Actor: {actor.full_name}, "
            f"starring in movies: {', '.join(movie_starring)}, "
            f"movies average rating: {actor.average_rating:.1f}")


# Django queries 2
def get_actors_by_movies_count():
    actors = Actor.objects.annotate(
        movies_count=Count("movies_actor")
    ).order_by(
        "-movies_count",
        "full_name"
    )[:3]

    result = []
    for actor in actors:
        if actor.movies_count:
            result.append(f"{actor.full_name}, participated in {actor.movies_count} movies")

    return "\n".join(result)


def get_top_rated_awarded_movie():
    movie = (
        Movie.objects.select_related(
            "starring_actor"
        ).prefetch_related(
            "actors"
        ).filter(
            is_awarded=True
        ).order_by(
            "-rating",
            "title"
        ).first()
    )

    if not movie:
        return ''

    staring_actor = movie.starring_actor.full_name if movie.starring_actor else "N/A"

    cast = (actor.full_name for actor in movie.actors.all().order_by("full_name"))

    return (f"Top rated awarded movie: {movie.title}, "
            f"rating: {movie.rating:.1f}. "
            f"Starring actor: {staring_actor}. "
            f"Cast: {', '.join(cast)}.")


def increase_rating():
    query = Q(is_classic=True) & Q(rating__lt=10)
    classic_movies = Movie.objects.filter(query)

    if not classic_movies:
        return f"No ratings increased."

    count = classic_movies.aggregate(count_movies=Count("title"))["count_movies"]
    classic_movies.update(rating=F("rating") + 0.1)

    return f"Rating increased for {count} movies."
