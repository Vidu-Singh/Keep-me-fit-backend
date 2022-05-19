from rest_framework import serializers
from .models import Person, Profile, Coach

class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model= Person
        fields='__all__'

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model= Profile
        fields= "__all__"

class CoachSerializer(serializers.ModelSerializer):
    class Meta:
        model= Coach
        fields= "__all__"