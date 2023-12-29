import re
import random
from django.core.mail import send_mail
from django.conf import settings
from django.utils.html import format_html

def email_verifier(email):
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
    if(re.fullmatch(regex, email)):
        return True
    return False

def generate_otp():
    return random.randint(100000, 999999)

def send_email(email, otp):
    subject = "OTP for Account Verification"
    activation_link = f"http://192.168.1.10:8000/accounts/activate/{email}/{otp}/"
    message = f"Activate Your Account by Clicking on this Link : "
    email_from = settings.EMAIL_HOST_USER
    message = format_html(
        f"Hi {email},<br>"
        f"Activate Your Account by Clicking on this Link : <br>"
        f'<a href="{activation_link}" style="background-color: #4CAF50; border: none; color: white; padding: 15px 32px; text-align: center; text-decoration: none; display: inline-block; font-size: 16px; margin: 4px 2px; cursor: pointer;">Click Here</a>'
    )
    send_mail(subject,'', email_from, [email], html_message=message)
