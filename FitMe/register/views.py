from datetime import timedelta

from django.http import JsonResponse
from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import *
import requests
from .serializers import *
import random
import pickle
import datefinder
from googleapiclient.discovery import build

# used in steps,colories api
access_token = "ya29.a0ARrdaM_vzkkn6kLUbrM2xXL5gVrGJ37IgPQmkFDevSHA5c6dz0ciNjbKVjjJjOfQpQRcjBT2xhu2IvGp3aXax5nmDg2TNeMfKl9bzBowL4FqP8SpzcGh1eG0U71LjlXxYYluYQ2cR9zAumkEZnwlkaGjVngP"
header = {'Authorization': 'Bearer {}'.format(access_token)}
start_time = 1653503405000
end_time = 1653589795000

# credentials for calender integration
scopes = ['https://www.googleapis.com/auth/calendar']
credentials = pickle.load(open("/home/priyesjain/Keep-me-fit-backend/FitMe/register/token.pkl","rb"))



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

    def steps(self,request):
        url = "https://www.googleapis.com/fitness/v1/users/me/dataset:aggregate"
        data = {
               "aggregateBy": [
              {
                    "dataSourceId": "derived:com.google.step_count.delta:com.google.android.gms:estimated_steps"
              }
              ],
            "startTimeMillis":start_time,
            "endTimeMillis": end_time,
            "bucketByTime": {
            "durationMillis": 86400000
             }
        }
        response = requests.post(url, headers=header,json=data).json()
        print(response["bucket"][0]["dataset"][0]['point'][0]['value'][0]['intVal'])
        return Response(response["bucket"][0]["dataset"][0]['point'][0]['value'][0]['intVal'],status=status.HTTP_200_OK)

    def calories(self,request):
        url = "https://www.googleapis.com/fitness/v1/users/me/dataset:aggregate"
        data = {
               "aggregateBy": [
              {
                    "dataSourceId": "derived:com.google.calories.expended:com.google.android.gms:merge_calories_expended"
              }
              ],
            "startTimeMillis":start_time,
            "endTimeMillis": end_time,
            "bucketByTime": {
            "durationMillis": 86400000
             }
        }
        response = requests.post(url, headers=header,json=data).json()
        # print(response)
        print(response["bucket"][0]["dataset"][0]['point'][0]['value'][0]['fpVal'])
        return Response(response["bucket"][0]["dataset"][0]['point'][0]['value'][0]['fpVal'],status=status.HTTP_200_OK)


    def distancetravelled(self,request):
        url = "https://www.googleapis.com/fitness/v1/users/me/dataset:aggregate"
        data = {
               "aggregateBy": [
              {
                    "dataSourceId": "derived:com.google.distance.delta:com.google.android.gms:merge_distance_delta"
              }
              ],
            "startTimeMillis":start_time,
            "endTimeMillis": end_time,
            "bucketByTime": {
            "durationMillis": 86400000
             }
        }
        response = requests.post(url, headers=header,json=data).json()
        print(response["bucket"][0]["dataset"][0]['point'][0]['value'][0]['fpVal'])
        # print(response["bucket"][0]["dataset"][0]['point'][0]['value'][0]['fpVal'])
        return Response(response["bucket"][0]["dataset"][0]['point'][0]['value'][0]['fpVal'],status=status.HTTP_200_OK)

    def heartrate(self,request):
        url = "https://www.googleapis.com/fitness/v1/users/me/dataset:aggregate"
        data = {
               "aggregateBy": [
              {
                    "dataSourceId": "derived:com.google.heart_rate.bpm:com.google.android.gms:merge_heart_rate_bpm"
              }
              ],
            "startTimeMillis":start_time,
            "endTimeMillis": end_time,
            "bucketByTime": {
            "durationMillis": 86400000
             }
        }
        response = requests.post(url, headers=header,json=data).json()
        print(response)
        # print(response["bucket"][0]["dataset"][0]['point'][0]['value'][0]['fpVal'])
        return Response(response,status=status.HTTP_200_OK)

    def get_all_events_of_user(self,request):
        service = build("calendar", "v3", credentials=credentials)
        result = service.calendarList().list().execute()
        calendar_id = result['items'][0]['id']
        all_events = service.events().list(calendarId=calendar_id).execute()
        response = all_events
        return Response(response, status=status.HTTP_200_OK)

    def create_event(start_time_str, summary, duration=1, description=None, location=None, attendees=[]):
        service = build("calendar", "v3", credentials=credentials)
        result = service.calendarList().list().execute()
        calendar_id = result['items'][0]['id']
        timezone = 'Asia/Kolkata'
        matches = list(datefinder.find_dates(start_time_str))
        if len(matches):
            start_time = matches[0]
            end_time = start_time + timedelta(hours=duration)

        event = {
            'summary': summary,
            'location': location,
            'description': description,
            'start': {
                'dateTime': start_time.strftime("%Y-%m-%dT%H:%M:%S"),
                'timeZone': timezone,
            },
            'end': {
                'dateTime': end_time.strftime("%Y-%m-%dT%H:%M:%S"),
                'timeZone': timezone,
            },
            'attendees': attendees,
            'reminders': {
                'useDefault': False,
                'overrides': [
                    {'method': 'email', 'minutes': 24 * 60},
                    {'method': 'popup', 'minutes': 10},
                ],
            },
        }
        return service.events().insert(calendarId=calendar_id, body=event).execute()

    def delete_event(self,request):
        service = build("calendar", "v3", credentials=credentials)
        result = service.calendarList().list().execute()
        calendar_id = result['items'][0]['id']
        timezone = 'Asia/Kolkata'
        count = service.events().delete(calendarId=calendar_id, eventId='960g87mr2r6pb2otd0n9a2j85c').execute();
        return JsonResponse({'message': '{} Event was deleted successfully!'.format(count[0])},
                            status=status.HTTP_204_NO_CONTENT)

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
