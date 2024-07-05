import os
from datetime import timedelta, date

import django
from django.db.models import Avg

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()


# Import your models here
from main_app.models import Author, Book, Artist, Song, Product, Review, DrivingLicense, Driver, Owner, Registration, \
    Car


# Create queries within functions
def show_all_authors_with_their_books():
    result = []
    authors = Author.objects.exclude(book__isnull=True)

    for a in authors:
        author_books = Book.objects.filter(author=a).order_by('author_id')
        auth_books = ', '.join(str(b) for b in author_books)
        result.append(f"{a.name} has written - {auth_books}!")

    return '\n'.join(result)


def delete_all_authors_without_books():
    Author.objects.filter(book__isnull=True).delete()


def add_song_to_artist(artist_name: str, song_title: str):
    artist = Artist.objects.get(name=artist_name)
    song = Song.objects.get(title=song_title)

    artist.songs.add(song)


def get_songs_by_artist(artist_name: str):
    # artist = Artist.objects.get(name=artist_name)
    # songs = Song.objects.filter(artists__songs=artist.id).order_by('-id')
    #
    # return songs

    return Artist.objects.get(name=artist_name).songs.all().order_by("-id")


def remove_song_from_artist(artist_name: str, song_title: str):
    artist = Artist.objects.get(name=artist_name)
    song = Song.objects.get(title=song_title)

    artist.songs.remove(song)


def calculate_average_rating_for_product_by_name(product_name: str):
    product = Product.objects.annotate(
        avg_rating=Avg('reviews__rating'),
    ).get(name=product_name)

    return product.avg_rating


def get_reviews_with_high_ratings(threshold: int):
    return Review.objects.filter(rating__gte=threshold)


def get_products_with_no_reviews():
    return Product.objects.filter(reviews__isnull=True).order_by('-name')


def delete_products_without_reviews():
    get_products_with_no_reviews().delete()


def calculate_licenses_expiration_dates():
    result = []
    licenses = DrivingLicense.objects.order_by('-license_number')

    for l in licenses:
        expiration_date = l.issue_date + timedelta(days=365)
        result.append(f"License with number: {l.license_number} expires on {expiration_date}!")

    return '\n'.join(result)


def get_drivers_with_expired_licenses(due_date: date):
    result = []
    drivers = Driver.objects.all()

    for d in drivers:
        if d.license.issue_date + timedelta(days=365) > due_date:
            result.append(d)

    return result


def register_car_by_owner(owner: Owner):
    registration = Registration.objects.filter(car__isnull=True).first()
    car = Car.objects.filter(registration__isnull=True).first()

    car.owner = owner
    car.save()

    registration.registration_date = date.today()
    registration.car = car
    registration.save()

    return f"Successfully registered {car.model} to {owner.name} with registration number {registration.registration_number}."
