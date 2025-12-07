from rest_framework import serializers
from .models import User, Team, Activity, Leaderboard, Workout


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model"""
    team_name = serializers.CharField(source='team.name', read_only=True)
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 
                  'bio', 'fitness_level', 'goals', 'team', 'team_name', 
                  'date_joined', 'last_login']
        read_only_fields = ['id', 'date_joined', 'last_login']
        extra_kwargs = {'password': {'write_only': True}}


class TeamSerializer(serializers.ModelSerializer):
    """Serializer for Team model"""
    created_by_username = serializers.CharField(source='created_by.username', read_only=True)
    member_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Team
        fields = ['_id', 'name', 'description', 'created_by', 'created_by_username', 
                  'member_count', 'created_at', 'updated_at']
        read_only_fields = ['_id', 'created_at', 'updated_at']
    
    def get_member_count(self, obj):
        return obj.members.count()


class ActivitySerializer(serializers.ModelSerializer):
    """Serializer for Activity model"""
    user_username = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = Activity
        fields = ['_id', 'user', 'user_username', 'activity_type', 'duration', 
                  'calories_burned', 'distance', 'notes', 'date', 
                  'created_at', 'updated_at']
        read_only_fields = ['_id', 'created_at', 'updated_at']


class LeaderboardSerializer(serializers.ModelSerializer):
    """Serializer for Leaderboard model"""
    user_username = serializers.CharField(source='user.username', read_only=True)
    team_name = serializers.CharField(source='team.name', read_only=True)
    
    class Meta:
        model = Leaderboard
        fields = ['_id', 'user', 'user_username', 'team', 'team_name', 
                  'total_calories', 'total_activities', 'total_distance', 
                  'rank', 'period', 'updated_at']
        read_only_fields = ['_id', 'updated_at']


class WorkoutSerializer(serializers.ModelSerializer):
    """Serializer for Workout model"""
    
    class Meta:
        model = Workout
        fields = ['_id', 'name', 'description', 'difficulty_level', 'duration', 
                  'calories_estimate', 'exercises', 'target_muscles', 
                  'equipment_needed', 'created_at', 'updated_at']
        read_only_fields = ['_id', 'created_at', 'updated_at']
