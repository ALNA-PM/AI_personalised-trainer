from django.shortcuts import render
from .models import TrainingSession

def home(request):
    """Renders the home page."""
    return render(request, 'AI_trainer/home.html')