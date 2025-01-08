from django.urls import path
from . import views
from .views import login_view, home_view

app_name = 'AI_trainer'

urlpatterns = [
    path('', login_view, name='login'),
    path('home/', home_view, name='home'), 
]