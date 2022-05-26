from django.urls import path, include
from .views import *

urlpatterns = [
    path("signup", RegisterUser.as_view()),
    path("login", LoginUser.as_view()),
    path("create-profile",ProfileView.as_view()),
    path("add-food",AddFood.as_view()),
    path("get-food",GetFood.as_view()),
    path("user-diet",AddDietView.as_view()),
    path("all-coaches",ExpertsView.as_view()),
]