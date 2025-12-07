from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import User, Team, Activity, Leaderboard, Workout
from datetime import datetime


class UserModelTest(TestCase):
    """Test cases for User model"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            bio='Test bio',
            fitness_level='intermediate'
        )
    
    def test_user_creation(self):
        """Test user is created successfully"""
        self.assertEqual(self.user.username, 'testuser')
        self.assertEqual(self.user.email, 'test@example.com')
        self.assertEqual(self.user.fitness_level, 'intermediate')


class TeamModelTest(TestCase):
    """Test cases for Team model"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.team = Team.objects.create(
            name='Test Team',
            description='A test team',
            created_by=self.user
        )
    
    def test_team_creation(self):
        """Test team is created successfully"""
        self.assertEqual(self.team.name, 'Test Team')
        self.assertEqual(self.team.created_by, self.user)
        self.assertEqual(str(self.team), 'Test Team')


class ActivityModelTest(TestCase):
    """Test cases for Activity model"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.activity = Activity.objects.create(
            user=self.user,
            activity_type='Running',
            duration=30,
            calories_burned=300,
            distance=5.0,
            date=datetime.now()
        )
    
    def test_activity_creation(self):
        """Test activity is created successfully"""
        self.assertEqual(self.activity.activity_type, 'Running')
        self.assertEqual(self.activity.duration, 30)
        self.assertEqual(self.activity.calories_burned, 300)


class LeaderboardModelTest(TestCase):
    """Test cases for Leaderboard model"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.leaderboard = Leaderboard.objects.create(
            user=self.user,
            total_calories=1000,
            total_activities=10,
            total_distance=50.0,
            rank=1,
            period='weekly'
        )
    
    def test_leaderboard_creation(self):
        """Test leaderboard entry is created successfully"""
        self.assertEqual(self.leaderboard.user, self.user)
        self.assertEqual(self.leaderboard.rank, 1)
        self.assertEqual(self.leaderboard.period, 'weekly')


class WorkoutModelTest(TestCase):
    """Test cases for Workout model"""
    
    def setUp(self):
        self.workout = Workout.objects.create(
            name='Morning Cardio',
            description='A morning cardio workout',
            difficulty_level='beginner',
            duration=30,
            calories_estimate=250,
            exercises=['Jumping Jacks', 'Running'],
            target_muscles=['Legs', 'Core'],
            equipment_needed=['None']
        )
    
    def test_workout_creation(self):
        """Test workout is created successfully"""
        self.assertEqual(self.workout.name, 'Morning Cardio')
        self.assertEqual(self.workout.difficulty_level, 'beginner')
        self.assertEqual(self.workout.duration, 30)


class UserAPITest(APITestCase):
    """API test cases for User endpoints"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
    
    def test_get_users_list(self):
        """Test getting list of users"""
        url = reverse('user-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TeamAPITest(APITestCase):
    """API test cases for Team endpoints"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.team = Team.objects.create(
            name='Test Team',
            created_by=self.user
        )
    
    def test_get_teams_list(self):
        """Test getting list of teams"""
        url = reverse('team-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class ActivityAPITest(APITestCase):
    """API test cases for Activity endpoints"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.activity = Activity.objects.create(
            user=self.user,
            activity_type='Running',
            duration=30,
            calories_burned=300,
            date=datetime.now()
        )
    
    def test_get_activities_list(self):
        """Test getting list of activities"""
        url = reverse('activity-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class LeaderboardAPITest(APITestCase):
    """API test cases for Leaderboard endpoints"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.leaderboard = Leaderboard.objects.create(
            user=self.user,
            rank=1,
            period='weekly'
        )
    
    def test_get_leaderboard_list(self):
        """Test getting leaderboard list"""
        url = reverse('leaderboard-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class WorkoutAPITest(APITestCase):
    """API test cases for Workout endpoints"""
    
    def setUp(self):
        self.workout = Workout.objects.create(
            name='Morning Cardio',
            description='A morning cardio workout',
            difficulty_level='beginner',
            duration=30,
            calories_estimate=250
        )
    
    def test_get_workouts_list(self):
        """Test getting list of workouts"""
        url = reverse('workout-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
