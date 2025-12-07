from djongo import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """Custom user model for OctoFit Tracker"""
    bio = models.TextField(blank=True, null=True)
    fitness_level = models.CharField(max_length=50, blank=True, null=True)
    goals = models.JSONField(default=list, blank=True)
    team = models.ForeignKey('Team', on_delete=models.SET_NULL, null=True, blank=True, related_name='members')
    
    class Meta:
        db_table = 'users'


class Team(models.Model):
    """Team model for group competitions"""
    _id = models.ObjectIdField(primary_key=True)
    name = models.CharField(max_length=200, unique=True)
    description = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_teams')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'teams'
    
    def __str__(self):
        return self.name


class Activity(models.Model):
    """Activity model for tracking user exercises"""
    _id = models.ObjectIdField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='activities')
    activity_type = models.CharField(max_length=100)
    duration = models.IntegerField(help_text='Duration in minutes')
    calories_burned = models.IntegerField()
    distance = models.FloatField(null=True, blank=True, help_text='Distance in kilometers')
    notes = models.TextField(blank=True, null=True)
    date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'activities'
        ordering = ['-date']
    
    def __str__(self):
        return f"{self.user.username} - {self.activity_type} on {self.date}"


class Leaderboard(models.Model):
    """Leaderboard model for tracking competitive rankings"""
    _id = models.ObjectIdField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='leaderboard_entries')
    team = models.ForeignKey(Team, on_delete=models.CASCADE, null=True, blank=True, related_name='leaderboard_entries')
    total_calories = models.IntegerField(default=0)
    total_activities = models.IntegerField(default=0)
    total_distance = models.FloatField(default=0.0)
    rank = models.IntegerField(default=0)
    period = models.CharField(max_length=50, default='weekly', help_text='weekly, monthly, all-time')
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'leaderboard'
        ordering = ['rank']
        unique_together = ['user', 'period']
    
    def __str__(self):
        return f"{self.user.username} - Rank {self.rank} ({self.period})"


class Workout(models.Model):
    """Workout model for personalized workout suggestions"""
    _id = models.ObjectIdField(primary_key=True)
    name = models.CharField(max_length=200)
    description = models.TextField()
    difficulty_level = models.CharField(max_length=50, help_text='beginner, intermediate, advanced')
    duration = models.IntegerField(help_text='Duration in minutes')
    calories_estimate = models.IntegerField()
    exercises = models.JSONField(default=list)
    target_muscles = models.JSONField(default=list)
    equipment_needed = models.JSONField(default=list)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'workouts'
    
    def __str__(self):
        return f"{self.name} ({self.difficulty_level})"
