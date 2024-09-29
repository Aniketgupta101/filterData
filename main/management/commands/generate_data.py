from django.core.management.base import BaseCommand
from main.models import User
import random

class Command(BaseCommand):
    help = 'Populate database with random users'

    def handle(self, *args, **kwargs):
        cities = ['Mumbai', 'Nashik', 'Thane', 'Delhi', 'Chennai']
        professionals = ['Management', 'Doctors', 'SDE', 'Professor']
        total_users = 100000
        batch_size = 10
        user = 0

        self.stdout.write(self.style.SUCCESS('Starting population...'))

        for page in range(0, total_users, batch_size):
            users_to_create = []
            
            for i in range(batch_size):
                user += 1
                random_age = str(random.randint(10, 75))
                if int(random_age) <= 22:
                    prof = 'student'
                else:
                    prof = random.choice(professionals)
                    
                users_to_create.append(User(
                    username=f'user_{user}',
                    contact_number=str(random.randint(1000000000, 9999999999)),
                    address=f'Sample-{user} address',
                    city=random.choice(cities),
                    age=random_age,
                    professional=prof
                ))

            # Bulk insert every batch of 10 users
            User.objects.bulk_create(users_to_create)
            self.stdout.write(self.style.SUCCESS(f'Page {page // batch_size + 1}: {len(users_to_create)} users created'))

        self.stdout.write(self.style.SUCCESS('Population complete.'))
