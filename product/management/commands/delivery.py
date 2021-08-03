"""Command to manage product delivery"""

from django.core.management.base import BaseCommand
from django.utils import timezone
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from product.models import Product
from group_member.models import GroupMember


class Command(BaseCommand):
    """Attributes and method useful for
    product delivery"""

    def handle(self, *args, **kwargs):
        """Method to compare current datetime
        and end rental product datetime to
        delete product tenant at the end
        of rental and send an email
        to let it be known"""

        products = Product.objects.all()
        today = timezone.now()

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

                    subject = f'Il est temps de rendre {product} !'
                    html_message = render_to_string(
                        'product/render_product_mail.html',
                        {
                            'username': f'{group_member.user.username}',
                            'product': product,
                        }
                    )
                    plain_message = strip_tags(html_message)
                    from_email = 'favoccia.c@live.fr'
                    to = f'{group_member.user.email}'

                    send_mail(
                        subject,
                        plain_message,
                        from_email,
                        [to],
                        html_message=html_message
                    )

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
