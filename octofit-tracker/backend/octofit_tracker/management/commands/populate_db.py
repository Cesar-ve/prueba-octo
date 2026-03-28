from django.core.management.base import BaseCommand
from octofit_tracker.models import User, Team, Activity, Workout, Leaderboard
from django.db import connection

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING('Deleting old data...'))
        Leaderboard.objects.all().delete()
        Workout.objects.all().delete()
        Activity.objects.all().delete()
        Team.objects.all().delete()
        User.objects.all().delete()

        self.stdout.write(self.style.SUCCESS('Creating users...'))
        marvel = Team.objects.create(name='Marvel')
        dc = Team.objects.create(name='DC')

        users = [
            User(username='ironman', email='ironman@marvel.com', first_name='Tony', last_name='Stark'),
            User(username='spiderman', email='spiderman@marvel.com', first_name='Peter', last_name='Parker'),
            User(username='batman', email='batman@dc.com', first_name='Bruce', last_name='Wayne'),
            User(username='superman', email='superman@dc.com', first_name='Clark', last_name='Kent'),
        ]
        for user in users:
            user.set_password('password123')
            user.save()

        marvel.members = [users[0], users[1]]
        marvel.save()
        dc.members = [users[2], users[3]]
        dc.save()

        self.stdout.write(self.style.SUCCESS('Creating activities...'))
        Activity.objects.create(user=users[0], type='Run', duration=30, calories=300, date='2023-01-01')
        Activity.objects.create(user=users[1], type='Swim', duration=45, calories=400, date='2023-01-02')
        Activity.objects.create(user=users[2], type='Bike', duration=60, calories=500, date='2023-01-03')
        Activity.objects.create(user=users[3], type='Yoga', duration=50, calories=200, date='2023-01-04')

        self.stdout.write(self.style.SUCCESS('Creating workouts...'))
        Workout.objects.create(user=users[0], name='Iron Endurance', description='Stark-level HIIT', date='2023-01-05')
        Workout.objects.create(user=users[2], name='Bat Strength', description='Dark Knight training', date='2023-01-06')

        self.stdout.write(self.style.SUCCESS('Creating leaderboard...'))
        Leaderboard.objects.create(team=marvel, score=700)
        Leaderboard.objects.create(team=dc, score=600)

        self.stdout.write(self.style.SUCCESS('Ensuring unique index on email...'))
        with connection.cursor() as cursor:
            cursor.execute('''db.get_collection('octofit_tracker_user').createIndex({"email": 1}, {"unique": true})''')

        self.stdout.write(self.style.SUCCESS('Database populated with test data!'))
