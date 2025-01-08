from django.shortcuts import render, redirect
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
            return render(request, 'AI_trainer/login.html', {'lock_time': lock_time})

        # Validate email input
        if not email:
            messages.error(request, "Please do enter your email.")
            return render(request, 'AI_trainer/login.html')
        
        if '@' not in email:
            messages.error(request, "Please enter a valid email address.")
            return render(request, 'AI_trainer/login.html')

        # Validate password input
        if not password:
            messages.error(request, "Please do enter your password.")
            return render(request, 'AI_trainer/login.html')

        # Verify email and password in MongoDB
        user = collection.find_one({"email": email})

        if user is None:
            messages.error(request, "Email and password are mismatching, please enter valid details.")
            failed_attempts += 1
        elif user['password'] != password:
            messages.error(request, "Email and password are mismatching, please enter valid details.")
            failed_attempts += 1
        else:
            # Reset failed attempts on successful login
            failed_attempts = 0
            return redirect('AI_trainer:home')  # Redirect to home page after successful login

        # Lock the user out after 3 failed attempts
        if failed_attempts >= 3:
            lock_time = 30  # Lock for 30 seconds
            messages.error(request, "Multiple failed login attempts. Please wait 30 seconds.")
        
        return render(request, 'AI_trainer/login.html', {'lock_time': lock_time})

    return render(request, 'AI_trainer/login.html')

from django.shortcuts import render

def home_view(request):
    """Renders the home page."""
    return render(request, 'AI_trainer/home.html')  # Ensure you have a home.html template