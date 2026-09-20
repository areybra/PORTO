from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()


class Command(BaseCommand):
    help = "Create or update superuser areybra"

    def handle(self, *args, **options):
        user, created = User.objects.get_or_create(
            username="areybra",
            defaults={
                "email": "areyaradjawali@gmail.com",
                "is_staff": True,
                "is_superuser": True,
                "first_name": "Areta",
                "last_name": "Radjawali",
            },
        )
        if created:
            user.set_password("radjawali2009!")
            user.save()
            self.stdout.write(self.style.SUCCESS("Superuser 'areybra' created successfully."))
        else:
            self.stdout.write(self.style.WARNING("Superuser 'areybra' already exists."))