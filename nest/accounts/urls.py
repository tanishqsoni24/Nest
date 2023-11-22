from django.urls import path, include
from .import views


urlpatterns = [
    path("signup/", views.signup, name="signup"),
    path("activate/<email>/<otp>/", views.activate, name="activate"),
    path("login/", views.acc_login, name="login"),
]
