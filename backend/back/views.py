from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from rest_framework import serializers, permissions, viewsets

from .forms import UserRegisterForm, UserModifyForm, UserProfileUpdateForm
from .models import UserProfile


def index(request):
    user = request.user
    return render(request, "back/index.html", {"user": user})


@login_required
def profile(request):
    user = request.user
    return render(
        request,
        "back/profile.html",
        {"user": user},
    )


def signup(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request, "Your account has been created ! You are now able to log in"
            )
            return redirect("login")
    else:
        form = UserRegisterForm()
    return render(
        request,
        "registration/signup.html",
        {"form": form, "title": "Sign Up for Blackhole Megalaser"},
    )


@login_required
def account_modify(request):
    user = User.objects.get(pk=request.user.pk)
    user_profile, _created = UserProfile.objects.get_or_create(user=user)
    if request.method == "POST":
        user_form = UserModifyForm(request.POST, instance=user)
        profile_form = UserProfileUpdateForm(
            request.POST,
            request.FILES,
            instance=user_profile,
        )
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect("profile")
    else:
        user_form = UserModifyForm(instance=request.user)
        profile_form = UserProfileUpdateForm(instance=user_profile)
    return render(
        request,
        "back/account_modify.html",
        {"user_form": user_form, "profile_form": profile_form},
    )


class UserSerializer(serializers.ModelSerializer):
    profile_image = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ["url", "username", "email", "is_staff", "profile_image"]

    def get_profile_image(self, obj):
        try:
            profile = obj.userprofile
        except UserProfile.DoesNotExist:
            return None
        if profile.profile_image:
            request = self.context.get("request")
            url = profile.profile_image.url
            if request:
                return request.build_absolute_uri(url)
            return url
        return None


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]
