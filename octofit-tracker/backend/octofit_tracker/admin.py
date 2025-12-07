from django.contrib import admin
from .models import User, Team, Activity, Leaderboard, Workout


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Admin interface for User model"""
    list_display = ['username', 'email', 'first_name', 'last_name', 'fitness_level', 'team', 'date_joined']
    list_filter = ['fitness_level', 'team', 'date_joined']
    search_fields = ['username', 'email', 'first_name', 'last_name']
    ordering = ['-date_joined']
    
    fieldsets = (
        ('User Info', {
            'fields': ('username', 'email', 'first_name', 'last_name', 'password')
        }),
        ('Fitness Profile', {
            'fields': ('bio', 'fitness_level', 'goals', 'team')
        }),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')
        }),
        ('Important Dates', {
            'fields': ('last_login', 'date_joined')
        }),
    )
    readonly_fields = ['last_login', 'date_joined']


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    """Admin interface for Team model"""
    list_display = ['name', 'created_by', 'created_at', 'get_member_count']
    list_filter = ['created_at']
    search_fields = ['name', 'description']
    ordering = ['-created_at']
    
    fieldsets = (
        ('Team Info', {
            'fields': ('name', 'description', 'created_by')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )
    readonly_fields = ['created_at', 'updated_at']
    
    def get_member_count(self, obj):
        """Get the number of members in the team"""
        return obj.members.count()
    get_member_count.short_description = 'Members'


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    """Admin interface for Activity model"""
    list_display = ['user', 'activity_type', 'duration', 'calories_burned', 'distance', 'date']
    list_filter = ['activity_type', 'date', 'user']
    search_fields = ['user__username', 'activity_type', 'notes']
    ordering = ['-date']
    
    fieldsets = (
        ('Activity Info', {
            'fields': ('user', 'activity_type', 'date')
        }),
        ('Metrics', {
            'fields': ('duration', 'calories_burned', 'distance')
        }),
        ('Additional Info', {
            'fields': ('notes',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Leaderboard)
class LeaderboardAdmin(admin.ModelAdmin):
    """Admin interface for Leaderboard model"""
    list_display = ['user', 'rank', 'period', 'total_calories', 'total_activities', 'total_distance', 'updated_at']
    list_filter = ['period', 'updated_at']
    search_fields = ['user__username']
    ordering = ['period', 'rank']
    
    fieldsets = (
        ('User & Team', {
            'fields': ('user', 'team')
        }),
        ('Statistics', {
            'fields': ('total_calories', 'total_activities', 'total_distance', 'rank')
        }),
        ('Period', {
            'fields': ('period',)
        }),
        ('Timestamps', {
            'fields': ('updated_at',)
        }),
    )
    readonly_fields = ['updated_at']


@admin.register(Workout)
class WorkoutAdmin(admin.ModelAdmin):
    """Admin interface for Workout model"""
    list_display = ['name', 'difficulty_level', 'duration', 'calories_estimate', 'created_at']
    list_filter = ['difficulty_level', 'created_at']
    search_fields = ['name', 'description']
    ordering = ['-created_at']
    
    fieldsets = (
        ('Workout Info', {
            'fields': ('name', 'description', 'difficulty_level')
        }),
        ('Metrics', {
            'fields': ('duration', 'calories_estimate')
        }),
        ('Details', {
            'fields': ('exercises', 'target_muscles', 'equipment_needed')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )
    readonly_fields = ['created_at', 'updated_at']
