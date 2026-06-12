from django.contrib import admin
from .models import Movie, UserAction

@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'genre', 'year', 'rating')
    list_filter = ('genre', 'year')
    search_fields = ('title', 'plot')

@admin.register(UserAction)
class UserActionAdmin(admin.ModelAdmin):
    list_display = ('user', 'action_type', 'movie', 'timestamp')
    list_filter = ('action_type', 'timestamp')