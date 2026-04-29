from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("accounts/profile/", views.profile, name="profile"),
    path("accounts/signup", views.signup, name="signup"),
    path("accounts/modify", views.account_modify, name="account_modify"),
]
