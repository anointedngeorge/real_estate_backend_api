from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from api.helpers.permission import SYSTEM_ROLES
from api.models.authorization import Roles 


class Command(BaseCommand):
    help = "Load system permissions"

    def handle(self, *args, **options):
        try:
            created_count = 0

            with transaction.atomic():
                for role_name in SYSTEM_ROLES:

                    role, created = Roles.objects.get_or_create(
                        name=role_name[0], defaults={"description": role_name[1]}
                    )

                    if created:
                        created_count += 1
                        self.stdout.write(
                            self.style.SUCCESS(
                                f'Created role: "{role_name[0]}"'
                            )
                        )

            self.stdout.write(
                self.style.SUCCESS(
                    f"Successfully loaded {created_count} roles."
                )
            )

        except Exception as e:
            raise CommandError(f"An error occurred: {str(e)}")