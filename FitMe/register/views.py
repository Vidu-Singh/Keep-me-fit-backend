from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import *
from .serializers import *
import random
from .utils import Util

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
            Util.send_mail(data['email'], number)
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
        number = random.randint(1000, 9999)
        user =  Person.objects.get(email=data["email"])
        user_code={
            "code":number
        }
        serializer=PersonSerializer(user,data=user_code,partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        print(serializer.data)
        Util.send_mail(data['email'], number)
        return Response({"message": "Login successful"}, status=status.HTTP_202_ACCEPTED)

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

# API to add food items
class AddFood(APIView):
    def post(self,request):
        data=request.data
        serializer= FoodSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

# API to get all food items
class GetFood(APIView):
    def get(self,request):
        all_food_items= Food.objects.all()
        response= FoodSerializer(all_food_items,many=True).data
        return Response(response, status=status.HTTP_200_OK)

# API to add diet plan for the user
class AddDietView(APIView):
    def post(self,request):
        data = request.data
        user_id = self.request.query_params.get('uid')
        all_food= Food.objects.all()
        breakfast= all_food.get(food_item=data["breakfast_food"])
        breakfast_data = FoodSerializer(breakfast).data
        break_id=breakfast_data.get('id')
        print(break_id)
        breakfast_protein= breakfast_data.get("protein")
        breakfast_fat = breakfast_data.get("fat")
        breakfast_carb= breakfast_data.get("carb")
        breakfast_cal = breakfast_data.get("calories")

        lunch= all_food.get(food_item= data["lunch_food"])
        lunch_data = FoodSerializer(lunch).data
        lunch_id=lunch_data.get('id')

        lunch_protein= lunch_data.get("protein")
        lunch_fat= lunch_data.get("fat")
        lunch_carb= lunch_data.get("carb")
        lunch_cal= lunch_data.get("calories")

        dinner= all_food.get(food_item =data["dinner_food"])
        dinner_data = FoodSerializer(dinner).data
        dinner_id=dinner_data.get('id')

        dinner_cal=dinner_data.get("calories")
        total_cal= breakfast_cal+lunch_cal+dinner_cal
        diet={
            "user_diet":user_id,
            "breakfast_food": break_id,
            "breakfast_quantity": data["breakfast_quantity"],
            "lunch_food" : lunch_id,
            "lunch_quantity": data["lunch_quantity"],
            "dinner_food": dinner_id,
            "dinner_quantity": data["dinner_quantity"],
            "water" : data["water"],
            "total_calories": total_cal
        }
        serializer= DietSerializer(data=diet)
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