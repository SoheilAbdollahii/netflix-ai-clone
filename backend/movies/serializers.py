from rest_framework import serializers
from .models import Movie, UserAction

class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = '__all__'

class UserActionSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAction
        fields = ['movie', 'search_query', 'action_type']