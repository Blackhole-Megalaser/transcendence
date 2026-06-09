from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from rest_framework import permissions, viewsets
from rest_framework.exceptions import PermissionDenied

from .forms import UserRegisterForm, UserModifyForm, UserProfileUpdateForm
from .models import UserProfile
from .serializers import (
    TplaceSerializer,
    NyancoinsSerializer,
    ColorsSerializer,
    PixelsSerializer,
    MaxPixelsSerializer,
)


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


# /users/
class NestedUserProfileReadOnlyViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def get_parent_user(self):
        username = self.kwargs.get("user_username")
        if username is None:
            return self.request.user
        if username != self.request.user.username and not self.request.user.is_staff:
            raise PermissionDenied("You cannot access another user's profile data.")
        return get_object_or_404(User, username=username)

    def get_queryset(self):
        parent_user = self.get_parent_user()
        return (
            UserProfile.objects.select_related("user")
            .prefetch_related("unlocked_colors", "unlocked_wordlists")
            .filter(user=parent_user)
        )

class TplaceViewSet(NestedUserProfileReadOnlyViewSet):
    serializer_class = TplaceSerializer

class NyancoinsViewSet(NestedUserProfileReadOnlyViewSet):
    serializer_class = NyancoinsSerializer

class ColorsViewSet(NestedUserProfileReadOnlyViewSet):
    serializer_class = ColorsSerializer

class PixelsViewSet(NestedUserProfileReadOnlyViewSet):
    serializer_class = PixelsSerializer

class MaxPixelsViewSet(NestedUserProfileReadOnlyViewSet):
    serializer_class = MaxPixelsSerializer
