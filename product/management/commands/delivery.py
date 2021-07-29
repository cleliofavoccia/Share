"""Command to manage product delivery"""

import datetime

from django.core.management.base import BaseCommand
from django.utils import timezone

from product.models import Product
from group_member.models import GroupMember


class Command(BaseCommand):
    """Attributes and method useful for
    product delivery"""

    def handle(self, *args, **kwargs):
        """Method to compare current datetime
        and end rental product datetime to
        delete product tenant at the end
        of rental"""

        products = Product.objects.all()
        today = timezone.now()

        # To use in test mode
        # today_test = datetime.datetime(2021, 8, 21)

        for product in products:

            try:
                group_member = GroupMember.objects.get(
                    user=product.tenant.user,
                    group=product.tenant.group
                )

                group_member.points_penalty -= 1

                group_member.save()

                if product.rental_end.day == today.day:

                    group_member.points_penalty = 0

                    group_member.save()

                    product.tenant = None
                    product.delivered = False

                    product.save()

                    self.stdout.write(
                        self.style.SUCCESS(
                            '"%s" rent ended' % product.name
                        )
                    )

            except AttributeError:
                self.stdout.write(
                    '"%s" is not rent ot rent is not ended' % product.name
                )
                continue
