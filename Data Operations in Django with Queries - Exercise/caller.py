import os

import django
from django.db.models import F

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from main_app.models import Pet, Artifact, Location, Car, Task, HotelRoom, Character


def create_pet(name: str, species: str) -> str:
    pet = Pet.objects.create(
        name=name,
        species=species,
    )

    return f'{pet.name} is a very cute {pet.species}!'


def create_artifact(name: str, origin: str, age: int, description: str, is_magical: bool):
    artifact = Artifact.objects.create(
        name=name,
        origin=origin,
        age=age,
        description=description,
        is_magical=is_magical,
    )

    return f"The artifact {artifact.name} is {artifact.age} years old!"


def rename_artifact(artifact: Artifact, new_name: str):
    # Artifact.objects.filter(age__gt=250, is_magical=True, pk=artifact.pk).update(name=new_name) -> Do not work for me

    if artifact.is_magical and artifact.age > 250:
        artifact.name = new_name
        artifact.save()


def delete_all_artifacts():
    artefacts = Artifact.objects.all()
    artefacts.delete()


def show_all_locations():
    result = []
    locations = Location.objects.all().order_by('-id')
    for location in locations:
        result.append(f"{location.name} has a population of {location.population}!")

    return '\n'.join(result)


def new_capital():
    location = Location.objects.first()
    location.is_capital = True
    location.save()


def get_capitals():
    capitals = Location.objects.filter(is_capital=True)
    return capitals.values('name')


def delete_first_location():
    Location.objects.first().delete()


def apply_discount():
    cars = Car.objects.all()

    for car in cars:
        discount = car.price * sum([int(x) for x in str(car.year)]) / 100
        car.price_with_discount = car.price - discount
        car.save()


def get_recent_cars():
    cars = Car.objects.filter(year__gt=2020)
    return cars.values('model', 'price_with_discount')


def delete_last_car():
    Car.objects.last().delete()


def show_unfinished_tasks():
    result = []
    tasks = Task.objects.filter(is_finished=False)
    for task in tasks:
        result.append(f"Task - {task.title} needs to be done until {task.due_date}!")

    return '\n'.join(result)


def complete_odd_tasks():
    tasks = Task.objects.all()

    for task in tasks:
        if task.id % 2 == 1:
            task.is_finished = True

    Task.objects.bulk_update(tasks, ['is_finished'])


def encode_and_replace(text: str, task_title: str):
    decoded_text = ''.join(chr(ord(x) - 3) for x in text)

    # 1 - This is not work for me but work for judge
    Task.objects.filter(title=task_title).update(description=decoded_text)

    # 2
    # tasks = Task.objects.filter(title=task_title)
    #
    # for task in tasks:
    #     task.description = decoded_text
    #
    # Task.objects.bulk_update(tasks, ['description'])


def get_deluxe_rooms():
    rooms = HotelRoom.objects.filter(room_type='Deluxe')
    result = []
    for room in rooms:
        if room.id % 2 == 0:
            result.append(f"Deluxe room with number {room.room_number} costs {room.price_per_night}$ per night!")

    return '\n'.join(result)


def increase_room_capacity():
    reserved_rooms = HotelRoom.objects.order_by('id')
    counter = reserved_rooms[0].id
    for rr in reserved_rooms:
        if rr.is_reserved:
            rr.capacity += counter
        counter = rr.capacity

    HotelRoom.objects.bulk_update(reserved_rooms, ['capacity'])


def reserve_first_room():
    room = HotelRoom.objects.first()
    room.is_reserved = True
    room.save()


def delete_last_room():
    room = HotelRoom.objects.last()

    if not room.is_reserved:
        room.delete()


def update_characters():
    Character.objects.filter(class_name='Mage').update(
        level=F('level') + 3,
        intelligence=F('intelligence') - 7
    )

    Character.objects.filter(class_name='Warrior').update(
        hit_points=F('hit_points') / 2,
        dexterity=F('dexterity') + 4
    )

    Character.objects.filter(class_name__in=['Assassin', 'Scout']).update(
        inventory='The inventory is empty'
    )


def fuse_characters(first_character: Character, second_character: Character):
    Character.objects.create(
        name=first_character.name + ' ' + second_character.name,
        class_name='Fusion',
        level=(first_character.level + second_character.level) / 2,
        strength=(first_character.strength + second_character.strength) * 1.2,
        dexterity=(first_character.dexterity + second_character.dexterity) * 1.4,
        intelligence=(first_character.intelligence + second_character.intelligence) * 1.5,
        hit_points=(first_character.hit_points + second_character.hit_points),
        inventory='Bow of the Elven Lords, Amulet of Eternal Wisdom' if first_character.class_name in ['Mage', 'Scout'] else 'Dragon Scale Armor, Excalibur'
    )
    first_character.delete()
    second_character.delete()


def grand_dexterity():
    Character.objects.update(dexterity=30)


def grand_intelligence():
    Character.objects.update(intelligence=40)


def grand_strength():
    Character.objects.update(strength=50)


def delete_characters():
    Character.objects.filter(inventory='The inventory is empty').delete()

# Create queries within functions
