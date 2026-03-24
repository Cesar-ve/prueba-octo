from django.urls import reverse
from rest_framework.test import APITestCase
from .models import User, Team, Activity, Workout, Leaderboard

class UserTests(APITestCase):
    def test_create_user(self):
        response = self.client.post('/admin/auth/user/add/', {'username': 'testuser', 'password': 'testpass'})
        self.assertIn(response.status_code, [200, 302])

class TeamTests(APITestCase):
    def test_create_team(self):
        user = User.objects.create(username='testuser')
        team = Team.objects.create(name='Test Team')
        team.members.add(user)
        self.assertEqual(team.name, 'Test Team')

class ActivityTests(APITestCase):
    def test_create_activity(self):
        user = User.objects.create(username='testuser')
        activity = Activity.objects.create(user=user, type='run', duration=30, calories=200, date='2023-01-01')
        self.assertEqual(activity.type, 'run')

class WorkoutTests(APITestCase):
    def test_create_workout(self):
        user = User.objects.create(username='testuser')
        workout = Workout.objects.create(user=user, name='Pushups', description='Do 20 pushups', date='2023-01-01')
        self.assertEqual(workout.name, 'Pushups')

class LeaderboardTests(APITestCase):
    def test_create_leaderboard(self):
        team = Team.objects.create(name='Test Team')
        leaderboard = Leaderboard.objects.create(team=team, score=100)
        self.assertEqual(leaderboard.score, 100)
