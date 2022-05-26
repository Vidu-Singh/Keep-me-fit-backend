from rest_framework import serializers
from .models import Person, Profile, Coach, Food, UserDiet

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

class DietSerializer(serializers.ModelSerializer):
    class Meta:
        model= UserDiet
        fields= "__all__"

class FoodSerializer(serializers.ModelSerializer):
    class Meta:
        model= Food
        fields= "__all__"