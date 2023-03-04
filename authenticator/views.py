from django.contrib.auth import authenticate, login
from django.shortcuts import render,redirect
from django.core.mail import send_mail
from authenticator.models import User
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
import random
from django.contrib import messages
import hashlib as hashVal

def login_view(request):
    request.session['otp-active'] = ""
    
    #  ________________________________________________________________________________NOTICE THIS FUNCTION
    if request.user.is_authenticated:
        print("redirected")
        # If the user is authenticated, redirect them to a specific URL
        # return redirect('my_authenticated_view')
    #  ________________________________________________________________________________NOTICE THIS FUNCTION

    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        
        # validate email and password
        user = authenticate(request, email=email, password=password)
        if user is not None:
            # generate OTP
            otp = random.randint(100000, 999999)
            
            # send OTP via email
            subject = 'Your login OTP'
            message = f'Your OTP is {otp}. Please enter it on the login page to log in.'
            email_from = settings.EMAIL_HOST_USER
            email_to = [email]
            user.otp_token = hashVal.sha256(str(otp).encode('UTF-8')).hexdigest()   #hashing this otp to store in the user model
            user.otp_created = timezone.now()
            user.save()
            
            try:
                send_mail( subject, message, email_from, email_to)
            except:
                print("Exception with the mail")

            request.session['otp-active'] = "active"
            return redirect('two_step_verification')
        else:
            messages.error(request, 'Invalid email or password')
    
    return render(request, 'login.html')

def two_step_verification(request):

    #  ________________________________________________________________________________NOTICE THIS FUNCTION
    if request.user.is_authenticated:
        print("redirected")
        # If the user is authenticated, redirect them to a specific URL
        # return redirect('my_authenticated_view')
    #  ________________________________________________________________________________NOTICE THIS FUNCTION

    if request.method == 'POST':
        email = request.POST['email']
        otp_entered = request.POST['otp']
        otp_hash = hashVal.sha256(str(otp_entered).encode('UTF-8')).hexdigest()
       
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request, 'Invalid email or otp')
            return redirect (two_step_verification)
        
        now = timezone.now()
        expiry_time = user.otp_created + timedelta(minutes=4)   # Setting expiry time
        
        if user.otp_token == otp_hash:
            if now < expiry_time:
                request.session['otp-active'] = ""
                login(request, user)
                # _________________________________________________________SET REDIRECT HERE
                return redirect("/admin/")
            else:
                request.session['otp-active'] = ""
                messages.error(request, 'Otp Expired.')
                return redirect (login)
        else:
            messages.error(request, 'Invalid email or otp')
            return redirect (two_step_verification)

    
    otp_active = request.session.get('otp-active')
    if not otp_active:
        return redirect('login')
    else:
        return render(request, 'verify_otp.html')