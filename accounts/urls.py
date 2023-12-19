from django.urls import path
from accounts import views

urlpatterns = [
    path("signup/", views.registration, name = "signup")
]
