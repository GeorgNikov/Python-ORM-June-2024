# Generated by Django 5.0.4 on 2024-07-10 18:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0003_product_alter_book_options_alter_movie_options_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='DiscountedProduct',
        ),
        migrations.CreateModel(
            name='DiscountedProduct',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('main_app.product',),
        ),
    ]
