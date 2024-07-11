from django.db.models import Manager, Count


class DirectorManager(Manager):
    def get_directors_by_movies_count(self):
        return self.annotate(
            movie_count=Count("movies_directed")
        ).order_by(
            "-movie_count",
            "full_name"
        )


class ActorManager(Manager):
    def get_actors_by_movies_count(self):
        return self.annotate(
            movie_count=Count("movies_starring")
        ).order_by(
            "-movie_count",
            "full_name"
        )