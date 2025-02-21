from django.db.models import Manager, Count


class ProfileManager(Manager):

    def get_regular_customers(self):
        return self.annotate(
            order_count=Count('profile_orders')
        ).filter(
            order_count__gt=2
        ).order_by(
            '-order_count'
        )
