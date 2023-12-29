from django.shortcuts import render, redirect
from django.http import HttpResponse
from base.helpers import *
from django.contrib.auth.models import User
from .models import Profile
from django.views.decorators.csrf import csrf_exempt
# import login
from django.contrib.auth import authenticate, login, logout

# Create your views here.

@csrf_exempt
def signup(request):
    if request.method == "POST":
        print('enter')
        email = request.POST.get("email")
        password = request.POST.get("password")
        if not email or not password:
            return HttpResponse("Invalid Data")
        is_valid_email = email_verifier(email)
        if(not is_valid_email):
            return HttpResponse("Invalid Email")

        user = User.objects.filter(username = email).first()

        if user:
            return HttpResponse("User Already Exists")
        make_user = User.objects.create(username = email)
        make_user.set_password(password)
        make_user.save()

        otp = generate_otp()
        profile_obj = Profile.objects.create(user = make_user, email = email, otp = otp)
        profile_obj.save()

        send_email(email, otp)
        return HttpResponse(f"An Email Has been sent to your Registered Mail Id as <b>{email}</b>")
    return render(request, "accounts/register.html")

@csrf_exempt
def activate(request, email, otp):
    user = User.objects.filter(username = email).first()
    profile_obj = Profile.objects.filter(user = user).first()
    if profile_obj.otp == int(otp):
        profile_obj.is_account_verified = True
        profile_obj.otp = None
        profile_obj.save()
        return HttpResponse("Account Verified")
    return HttpResponse("Invalid OTP")

@csrf_exempt
def acc_login(request):
    if request.method == "POST":
        print('enter')
        email = request.POST.get("email")
        password = request.POST.get("password")
        if not email or not password:
            return HttpResponse("Invalid Data")
        is_valid_email = email_verifier(email)
        if(not is_valid_email):
            return HttpResponse("Invalid Email")
        user = User.objects.filter(username = email).first()
        if not user:
            return HttpResponse("User Doesn't Exists")
        if not user.check_password(password):
            return HttpResponse("Invalid Password")
        profile_obj = Profile.objects.filter(user = user).first()
        if not profile_obj.is_account_verified:
            return HttpResponse("Account Not Verified")
        login(request, user)
        return HttpResponse("Logged In")
    return render(request, "accounts/login.html")
        
def acc_logout(request):
    logout(request)
    return redirect("/")

