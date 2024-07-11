import os

import django
from django.db.models import Q, Count, Avg

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from main_app.models import Author, Article


# Create queries within functions
# Django Queries I
def get_authors(search_name=None, search_email=None):
    result = []

    if search_name is None and search_email is None:
        return ''

    query = Q()

    if search_name and search_email is None:
        query = Q(full_name__icontains=search_name)
    elif search_name is None and search_email:
        query = Q(email__icontains=search_email)
    else:
        query = Q(full_name__icontains=search_name) & Q(email__icontains=search_email)

    authors = Author.objects.filter(query).order_by('-full_name')

    for author in authors:
        result.append(f'Author: {author.full_name}, '
                      f'email: {author.email}, '
                      f'status: {"Banned" if author.is_banned else "Not Banned"}')

    if not result:
        return ''

    return '\n'.join(result)


# print(get_authors('an', 'ne'))

def get_top_publisher():
    author = Author.objects.get_authors_by_article_count().first()

    if author is None or not author.article_count:
        return ""

    return f'Top Author: {author.full_name} with {author.authors_articles.count()} published articles.'


def get_top_reviewer():
    author = (Author.objects.
              prefetch_related('author_reviews').
              annotate(review_count=Count('author_reviews')).
              order_by('-review_count', 'email').
              first())

    if author is None or not author.review_count:
        return ''

    return f'Top Reviewer: {author.full_name} with {author.review_count} published reviews.'


# Django Queries II
def get_latest_article():
    article = (Article.objects.
               prefetch_related('article_reviews').
               annotate(avg_reviews_rating=Avg('article_reviews__rating')).
               order_by('-published_on').
               first())

    if article is None:
        return ''

    avg_rating = article.article_reviews.aggregate(Avg('rating'))['rating__avg']
    avg_rating = 0 if avg_rating is None else avg_rating

    authors_list = ', '.join(a.full_name for a in article.authors.all().order_by('full_name'))

    return (f'The latest article is: {article.title}. '
            f'Authors: {authors_list}. '
            f'Reviewed: {article.article_reviews.count()} times. '
            f'Average Rating: {avg_rating:.2f}.')


def get_top_rated_article():
    article = (Article.objects.
               prefetch_related('article_reviews').
               annotate(avg_reviews_rating=Avg('article_reviews__rating')).
               exclude(avg_reviews_rating__isnull=True).
               order_by('-avg_reviews_rating', 'title').
               first())

    if article is None:
        return ''

    return (f"The top-rated article is: {article.title},"
            f" with an average rating of {article.avg_reviews_rating:.2f},"
            f" reviewed {article.article_reviews.count()} times.")


def ban_author(email=None):
    if email is None:
        return "No authors banned."

    author = Author.objects.prefetch_related("author_reviews").filter(email=email).first()

    if author is None:
        return "No authors banned."

    num_reviews = author.author_reviews.count()
    author.is_banned = True
    author.author_reviews.all().delete()
    author.save()

    return f"Author: {author.full_name} is banned! {num_reviews} reviews deleted."
