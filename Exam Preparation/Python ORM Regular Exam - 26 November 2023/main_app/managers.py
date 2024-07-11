from django.db import models
from django.db.models import Count


class AuthorManager(models.Manager):
    def get_authors_by_article_count(self):
        return (self.
                prefetch_related("authors_articles").
                annotate(article_count=Count("authors_articles")).
                order_by("-article_count", "email")
                )
