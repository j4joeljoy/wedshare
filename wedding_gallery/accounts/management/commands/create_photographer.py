from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = "Create default photographer user"

    def handle(self, *args, **kwargs):
        username = "photographer"
        password = "photographer@123"

        if not User.objects.filter(username=username).exists():
            User.objects.create_user(
                username=username,
                password=password
            )
            self.stdout.write(
                self.style.SUCCESS("Photographer user created successfully")
            )
        else:
            self.stdout.write(
                self.style.WARNING("Photographer user already exists")
            )
