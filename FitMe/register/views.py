from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import *
from .serializers import *
import random

# Register User API
class RegisterUser(APIView):
    def post(self,request):
        data = request.data
        try:
            person = Person.objects.get(email=data["email"])
            if person is not None:
                return Response({"error": "Email already exists"}, status=status.HTTP_406_NOT_ACCEPTABLE)
        except Person.DoesNotExist:
            number = random.randint(1000, 9999)
            print(number)
            user_data={
                "email":data["email"],
                "password":data["password"],
                "code":number
            }
            serializer = PersonSerializer(data=user_data)

            serializer.is_valid(raise_exception=True)
            serializer.save()
            user = {
                "user_email": serializer.data.get("email")
            }
            return Response(user, status=status.HTTP_201_CREATED)

# Login API
class LoginUser(APIView):
    def post(self, request):
        data = request.data
        try:
            result = Person.objects.get(email=data["email"])
        except Person.DoesNotExist:
            return Response({"error": "Invalid email Id"}, status=status.HTTP_406_NOT_ACCEPTABLE)
        user = PersonSerializer(result).data
        if user.get("password") != data["password"]:
            return Response({"error": "Invalid Password"}, status=status.HTTP_406_NOT_ACCEPTABLE)
        user = {
            "User Email": user.get("email")
        }
        return Response(user, status=status.HTTP_202_ACCEPTED)

# Code Authentication(user/id)

# User profile view
class ProfileView(APIView):
    def post(self, request):
        data=request.data
        user_id = self.request.query_params.get('uid')
        profile_data={
            "user_id":user_id,
            "name":data["name"],
            "dob": data["dob"],
            "gender":data["gender"],
            "height": data["height"],
            "weight": data["weight"],
            "allergies": data["allergies"],
            "health_issues": data["health_issues"]
        }
        serializer= ProfileSerializer(data=profile_data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

# Coach for Well-being connect
class ExpertsView(APIView):
    def get(self, request):
        all_coaches= Coach.objects.all()
        response= CoachSerializer(all_coaches,many=True).data
        return Response(response,status=status.HTTP_200_OK)

    def post(self,request):
        coach_data=request.data
        serializer= CoachSerializer(data=coach_data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)