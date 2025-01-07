from django.contrib import admin
from .models import User, Job


# Registering the User model in the admin interface with custom configuration
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    # Fields to display in the list view
    list_display = ('username', 'email', 'role', 'date_joined')

    # Filters available in the right sidebar of the list view
    list_filter = ('role', 'is_active', 'date_joined')

    # Fields that can be searched using the search bar
    search_fields = ('username', 'email')

    # Default ordering of records in the list view
    ordering = ('-date_joined',)

    # Fields that are read-only in the form view
    readonly_fields = ('date_joined', 'last_login')

    # Field grouping for organizing the form view
    fieldsets = (
        ('User Information', {'fields': ('username', 'email', 'password')}),
        ('Permissions', {'fields': ('role', 'is_active', 'is_staff', 'is_superuser')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )


# Registering the Job model in the admin interface with custom configuration
@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    # Fields to display in the list view
    list_display = ('title', 'created_by', 'created_at')

    # Filters available in the right sidebar of the list view
    list_filter = ('created_at',)

    # Fields that can be searched using the search bar
    search_fields = ('title', 'description', 'created_by__username')

    # Default ordering of records in the list view
    ordering = ('-created_at',)

    # Fields that are read-only in the form view
    readonly_fields = ('created_at',)

    # Field grouping for organizing the form view
    fieldsets = (
        ('Job Information', {'fields': ('title', 'description')}),
        ('Ownership', {'fields': ('created_by',)}),
        ('Timestamps', {'fields': ('created_at',)}),
    )

