from datetime import datetime as dt

from django.contrib.auth.models import User
from django.db.transaction import atomic
from django.core.management.base import BaseCommand

from reservation.models import Room, Reserve


class Command(BaseCommand):
    help = 'Puts sample data into the database and prepares the service for testing.'

    def handle(self, *args, **options):
        self.stdout.write(f'>>> Start seeding database...\n')

        try:
            with atomic():
                if not User.objects.filter(username='admin').exists():
                    User.objects.create_superuser(username='admin', password='admin')

                Room.objects.bulk_create([Room() for _ in range(6)])
                rooms = Room.objects.all()[:4]
                reserve_data = [
                    {
                        'room': rooms[0],
                        'customer_fullname': 'Customer 1',
                        'from_dt': dt(2022, 12, 2, 12, 30),
                        'to_dt': dt(2022, 12, 5, 14),
                    },
                    {
                        'room': rooms[0],
                        'customer_fullname': 'Customer 2',
                        'from_dt': dt(2022, 12, 5, 15),
                        'to_dt': dt(2022, 12, 15, ),
                    },
                    {
                        'room': rooms[1],
                        'customer_fullname': 'Customer 2',
                        'from_dt': dt(2022, 12, 5, 15),
                        'to_dt': dt(2022, 12, 15, ),
                    },
                    {
                        'room': rooms[2],
                        'customer_fullname': 'Customer 3',
                        'from_dt': dt(2023, 1, 5, 15),
                        'to_dt': dt(2023, 1, 15, ),
                    },
                    {
                        'room': rooms[3],
                        'customer_fullname': 'Customer 3',
                        'from_dt': dt(2023, 5, 20, 20),
                        'to_dt': dt(2023, 5, 25, 20),
                    },
                    {
                        'room': rooms[3],
                        'customer_fullname': 'Customer 4',
                        'from_dt': dt(2023, 5, 19, 8),
                        'to_dt': dt(2023, 5, 20, 18),
                    },

                ]
                Reserve.objects.bulk_create([Reserve(**obj) for obj in reserve_data], ignore_conflicts=True)

            self.stdout.write(f'>>> {self.style.SUCCESS("All done successfully.")}')
        except Exception as e:
            print(e)
            self.stdout.write(self.style.ERROR('Some things went wrong while seeding!!!\n\tPlease try again...'))
