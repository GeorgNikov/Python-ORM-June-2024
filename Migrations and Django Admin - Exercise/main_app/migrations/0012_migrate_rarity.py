# Generated by Django 5.0.4 on 2024-06-23 07:16

from django.db import migrations


class Migration(migrations.Migration):

    def set_rarity(apps, schema_editor):
        item_model = apps.get_model('main_app', 'Item')
        items = item_model.objects.all()

        for i in items:
            if i.price <= 10:
                i.rarity = 'Rare'
            elif i.price <= 20:
                i.rarity = 'Very Rare'
            elif i.price <= 30:
                i.rarity = 'Extremely Rare'
            else:
                i.rarity = 'Mega Rare'

        item_model.objects.bulk_update(items, ['rarity'])

    def set_rarity_default(apps, schema_editor):
        item_model = apps.get_model('main_app', 'Item')
        items = item_model.objects.all()

        rarity_default = item_model._meta.get_field('rarity').default

        for i in items:
            i.rarity = rarity_default

        item_model.objects.bulk_update(items, ['rarity'])

    dependencies = [
        ('main_app', '0011_item'),
    ]

    operations = [
        migrations.RunPython(set_rarity, reverse_code=set_rarity_default)
    ]
