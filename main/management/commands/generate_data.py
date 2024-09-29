from django.core.management.base import BaseCommand
from main.models import User
import random


class Command(BaseCommand):
    help = 'Populate database with random users'

    def handle(self, *args, **kwargs):
        cities = ['Mumbai', 'Nashik', 'Thane', 'Dehli', 'Chennai']
        professionals = ['Management', 'Doctors', 'SDE', 'Professor']
        users_to_create = []
        total_users = 100
        user = 0
        age = 0

        self.stdout.write(self.style.SUCCESS('Starting population...'))

        for i in range(total_users):
            user = user + 1

            # get age and professionals 
            random_age = str(random.randint(10, 75))
            if(int(random_age)<= 22):
                prof = 'student'
            else:
                prof = random.choice(professionals)
            users_to_create.append(User(
                username=f'user_{user}',
                contact_number=str(random.randint(1000000000, 9999999999)),
                address = f'Sample-{user} address',
                city=random.choice(cities),
                age = random_age,
                professional = prof
            ))

            
        User.objects.bulk_create(users_to_create)
        self.stdout.write(self.style.SUCCESS("Users created"))

        # Insert remaining users if remains
        if users_to_create:
            User.objects.bulk_create(users_to_create)

        self.stdout.write(self.style.SUCCESS('Population complete.'))
