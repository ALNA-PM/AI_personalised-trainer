from django.urls import path
from . import views

app_name = 'AI_trainer'

urlpatterns = [
    path("home/", views.home, name="home"), 
]