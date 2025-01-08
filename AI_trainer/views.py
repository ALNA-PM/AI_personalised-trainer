from django.shortcuts import render, redirect
from .models import TrainingSession
from django.http import JsonResponse
from pymongo import MongoClient
from django.contrib import messages
import time

client = MongoClient('mongodb://localhost:27017/')
db = client['AI_trainer']
collection = db['login']

failed_attempts = 0
lock_time = 0

def login_view(request):
    global failed_attempts, lock_time

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        print(f"Email: {email}, Password: {password}")
        
        # Check if the user is locked out
        if lock_time > 0:
            messages.error(request, f"Multiple failed login attempts. Please wait {lock_time} seconds.")
            return render(request, 'AI_trainer/login.html')

        if not email or not password:
            messages.error(request, "Email and password are required.")
            return render(request, 'AI_trainer/login.html')

        user = collection.find_one({"email": email})

        if user is None:
            messages.error(request, "Email is incorrect.")
            failed_attempts += 1
        elif user['password'] != password:
            messages.error(request, "Password is incorrect.")
            failed_attempts += 1
        else:
            # Reset failed attempts on successful login
            failed_attempts = 0
            return redirect('AI_trainer:home')  # Redirect to home page after successful login

        # Lock the user out after 3 failed attempts
        if failed_attempts >= 3:
            lock_time = 30  # Lock for 30 seconds
            messages.error(request, "Multiple failed login attempts. Please wait 30 seconds.")
        
        return render(request, 'AI_trainer/login.html')

    return render(request, 'AI_trainer/login.html')

def countdown():
    global lock_time
    while lock_time > 0:
        time.sleep(1)
        lock_time -= 1
        
def home_view(request):
    """Renders the home page."""
    return render(request, 'AI_trainer/home.html')

