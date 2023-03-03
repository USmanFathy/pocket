from django.contrib.auth import authenticate, login
from django.shortcuts import render,redirect
from django.core.mail import send_mail
from authenticator.models import User
from django.conf import settings
from django.utils import timezone
from datetime import datetime, timedelta
import random

def validate_otp(otp, user):
    if user.otp_token is not None and user.otp_token == otp:
        valid_time = user.otp_created + timedelta(minutes=5)
        if datetime.now() < valid_time:
            return True
    return False

def login_view(request):
    error_message = None
    show_otp = False

    if request.method == 'POST' and 'otp' not in request.POST:
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)

        if user is not None:
            show_otp = True
            email_from = settings.EMAIL_HOST_USER
            email_to = [email]
            random_otp = random.randint(000000,999999)
            user.otp_token = random_otp
            user.otp_created = timezone.now()
            user.save()

            try:
                send_mail( "Your OTP.", str(random_otp), email_from, email_to)
            except:
                print("Exception with the mail")

        else:
            error_message = 'Invalid email or password'
    else:
        error_message = None

    if show_otp:
        if 'otp' in request.POST:
            print(user)
            print("outside validation")
            otp = request.POST['otp']
            if validate_otp(otp,user): # replace with your OTP validation logic
                print(user)
                login(request, user)
                # Redirect to the home page or a dashboard page
                return redirect('admin') # replace 'home' with your URL pattern name
            else:
                error_message = 'Invalid OTP'
        else:
            show_otp = True # If the request method is not POST, we show the OTP field

    context = {
        'title': "Login",
        'error_message': error_message,
        'show_otp': show_otp,
    }

    return render(request, 'login.html', context)

