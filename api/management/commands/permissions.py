from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from api.helpers.permission import SYSTEM_PERMISSIONS
from api.models.authorization import Permission


class Command(BaseCommand):
    help = "Load system permissions"

    def handle(self, *args, **options):
        try:
            created_count = 0

            with transaction.atomic():
                for permission_name in SYSTEM_PERMISSIONS:

                    permission, created = Permission.objects.get_or_create(
                        name=permission_name[0], defaults={"description": permission_name[1]}
                    )

                    if created:
                        created_count += 1
                        self.stdout.write(
                            self.style.SUCCESS(
                                f'Created permission: "{permission_name[0]}"'
                            )
                        )

            self.stdout.write(
                self.style.SUCCESS(
                    f"Successfully loaded {created_count} permissions."
                )
            )

        except Exception as e:
            raise CommandError(f"An error occurred: {str(e)}")