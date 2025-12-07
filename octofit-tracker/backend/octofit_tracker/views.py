from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Sum, Count
from .models import User, Team, Activity, Leaderboard, Workout
from .serializers import (
    UserSerializer, TeamSerializer, ActivitySerializer,
    LeaderboardSerializer, WorkoutSerializer
)


class UserViewSet(viewsets.ModelViewSet):
    """
    ViewSet for User operations
    Provides CRUD operations for users
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    @action(detail=True, methods=['get'])
    def activities(self, request, pk=None):
        """Get all activities for a specific user"""
        user = self.get_object()
        activities = Activity.objects.filter(user=user)
        serializer = ActivitySerializer(activities, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def stats(self, request, pk=None):
        """Get user statistics"""
        user = self.get_object()
        stats = Activity.objects.filter(user=user).aggregate(
            total_activities=Count('_id'),
            total_calories=Sum('calories_burned'),
            total_distance=Sum('distance')
        )
        return Response(stats)


class TeamViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Team operations
    Provides CRUD operations for teams
    """
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    
    @action(detail=True, methods=['get'])
    def members(self, request, pk=None):
        """Get all members of a specific team"""
        team = self.get_object()
        members = team.members.all()
        serializer = UserSerializer(members, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def join(self, request, pk=None):
        """Allow a user to join a team"""
        team = self.get_object()
        user_id = request.data.get('user_id')
        try:
            user = User.objects.get(id=user_id)
            user.team = team
            user.save()
            return Response({'status': 'user joined team'})
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)


class ActivityViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Activity operations
    Provides CRUD operations for activities
    """
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer
    
    def get_queryset(self):
        """Filter activities by user if provided"""
        queryset = Activity.objects.all()
        user_id = self.request.query_params.get('user', None)
        if user_id:
            queryset = queryset.filter(user_id=user_id)
        return queryset


class LeaderboardViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Leaderboard operations
    Provides CRUD operations for leaderboard entries
    """
    queryset = Leaderboard.objects.all()
    serializer_class = LeaderboardSerializer
    
    def get_queryset(self):
        """Filter leaderboard by period if provided"""
        queryset = Leaderboard.objects.all()
        period = self.request.query_params.get('period', None)
        if period:
            queryset = queryset.filter(period=period)
        return queryset
    
    @action(detail=False, methods=['get'])
    def weekly(self, request):
        """Get weekly leaderboard"""
        leaderboard = Leaderboard.objects.filter(period='weekly').order_by('rank')
        serializer = self.get_serializer(leaderboard, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def monthly(self, request):
        """Get monthly leaderboard"""
        leaderboard = Leaderboard.objects.filter(period='monthly').order_by('rank')
        serializer = self.get_serializer(leaderboard, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def all_time(self, request):
        """Get all-time leaderboard"""
        leaderboard = Leaderboard.objects.filter(period='all-time').order_by('rank')
        serializer = self.get_serializer(leaderboard, many=True)
        return Response(serializer.data)


class WorkoutViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Workout operations
    Provides CRUD operations for workout suggestions
    """
    queryset = Workout.objects.all()
    serializer_class = WorkoutSerializer
    
    def get_queryset(self):
        """Filter workouts by difficulty level if provided"""
        queryset = Workout.objects.all()
        difficulty = self.request.query_params.get('difficulty', None)
        if difficulty:
            queryset = queryset.filter(difficulty_level=difficulty)
        return queryset
    
    @action(detail=False, methods=['get'])
    def suggestions(self, request):
        """Get personalized workout suggestions based on user's fitness level"""
        fitness_level = request.query_params.get('fitness_level', 'beginner')
        workouts = Workout.objects.filter(difficulty_level=fitness_level)
        serializer = self.get_serializer(workouts, many=True)
        return Response(serializer.data)
