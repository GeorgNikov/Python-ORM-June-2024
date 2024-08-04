import os

import django
from django.db.models import Q, Count, Sum, F, Avg

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from main_app.models import Astronaut, Mission, Spacecraft


# Create queries within functions
def get_astronauts(search_string=None):
    if search_string is not None:
        query = Q(name__icontains=search_string) | Q(phone_number__icontains=search_string)
    else:
        return ''

    astronauts = Astronaut.objects.filter(query).order_by('name')

    result = []
    for a in astronauts:
        result.append(f"Astronaut: {a.name}, "
                      f"phone number: {a.phone_number}, "
                      f"status: {'Active' if a.is_active else 'Inactive'}")

    return '\n'.join(result) if astronauts else ''


def get_top_astronaut():
    top_astronaut = Astronaut.objects.get_astronauts_by_missions_count().first()

    if not top_astronaut or top_astronaut.missions_count == 0:
        return 'No data.'

    return f"Top Astronaut: {top_astronaut.name} with {top_astronaut.missions_count} missions."


def get_top_commander():
    astronaut = Astronaut.objects.annotate(
        commanded_count=Count('commanded_missions')
    ).filter(
        commanded_count__gt=0
    ).order_by(
        '-commanded_count',
        'phone_number'
    ).first()

    return (f"Top Commander: {astronaut.name} "
            f"with {astronaut.commanded_count} "
            f"commanded missions.") if astronaut else 'No data.'


# 2
def get_last_completed_mission():
    last_mission = Mission.objects.filter(
        status=Mission.StatusChoices.COMPLETED
    ).order_by(
        '-launch_date'
    ).first()

    if not last_mission:
        return 'No data.'

    commander_name = last_mission.commander.name if last_mission.commander else 'TBA'
    astronauts = last_mission.astronauts.order_by('name').values_list('name', flat=True)
    all_astronauts = ", ".join(astronauts)
    total_spacewalks = last_mission.astronauts.aggregate(total_spacewalks=Sum('spacewalks'))['total_spacewalks']

    return (f"The last completed mission is: {last_mission.name}. "
            f"Commander: {commander_name}. "
            f"Astronauts: {all_astronauts}. "
            f"Spacecraft: {last_mission.spacecraft.name}. "
            f"Total spacewalks: {total_spacewalks}.")


def get_most_used_spacecraft():
    spacecraft = Spacecraft.objects.annotate(
        missions_count=Count('spacecraft_missions')
    ).order_by(
        '-missions_count',
        'name'
    ).first()

    if not spacecraft or spacecraft.missions_count == 0:
        return "No data."

    num_astronauts = Astronaut.objects.filter(
        astronauts_missions__spacecraft__exact=spacecraft
    ).distinct().count()

    return (f"The most used spacecraft is: {spacecraft.name}, "
            f"manufactured by {spacecraft.manufacturer}, "
            f"used in {spacecraft.missions_count} missions, "
            f"astronauts on missions: {num_astronauts}.")


def decrease_spacecrafts_weight():
    spacecrafts = Spacecraft.objects.filter(
        spacecraft_missions__status=Mission.StatusChoices.PLANNED,
        weight__gte=200.0
    ).distinct()

    if not spacecrafts.exists():
        return 'No changes in weight.'

    spacecraft_count = spacecrafts.update(weight=F('weight') - 200.0)
    average_weight = Spacecraft.objects.aggregate(avg_weight=Avg('weight'))['avg_weight']

    if not spacecraft_count:
        return 'No changes in weight.'

    return (f"The weight of {spacecraft_count} spacecrafts has been decreased. "
            f"The new average weight of all spacecrafts is {average_weight:.1f}kg")

# For test
