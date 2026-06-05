from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from rest_framework import permissions, viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action

from .forms import UserRegisterForm, UserModifyForm, UserProfileUpdateForm
from .models import UserProfile
from .serializers import (
    UserSerializer,
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
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]
    lookup_field = "username"
    lookup_value_regex = "[a-zA-Z0-9-_@.+]+"

    @action(
        detail=False,
        url_path="me",
        methods=["get"],
        permission_classes=[permissions.IsAuthenticated],
    )
    def me(self, request):
        serializer = self.get_serializer(request.user, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.get_serializer(user)
        data = serializer.data

        # Add available nested routes
        data["available_routes"] = {
            "tplace": request.build_absolute_uri(f"/api/users/{user.username}/tplace/"),
            "nyancoins": request.build_absolute_uri(
                f"/api/users/{user.username}/nyancoins/"
                ),
            "colors": request.build_absolute_uri(f"/api/users/{user.username}/colors/"),
            "pixels": request.build_absolute_uri(f"/api/users/{user.username}/pixels/"),
            "max-pixels": request.build_absolute_uri(
                f"/api/users/{user.username}/max-pixels/"
                ),
        }

        return Response(data)


# /users/{username}/
class TplaceViewSet(viewsets.ModelViewSet):
    serializer_class = TplaceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        username = self.kwargs.get("user_username")
        if username is not None:
            get_object_or_404(UserProfile, user__username=username)
            return UserProfile.objects.filter(user__username=username)
        return UserProfile.objects.all()


class NyancoinsViewSet(viewsets.ModelViewSet):
    serializer_class = NyancoinsSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        username = self.kwargs.get("user_username")
        if username is not None:
            get_object_or_404(UserProfile, user__username=username)
            return UserProfile.objects.filter(user__username=username)
        return UserProfile.objects.all()


class ColorsViewSet(viewsets.ModelViewSet):
    serializer_class = ColorsSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        username = self.kwargs.get("user_username")
        if username is not None:
            get_object_or_404(UserProfile, user__username=username)
            return UserProfile.objects.filter(user__username=username)
        return UserProfile.objects.all()


class PixelsViewSet(viewsets.ModelViewSet):
    serializer_class = PixelsSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        username = self.kwargs.get("user_username")
        if username is not None:
            get_object_or_404(UserProfile, user__username=username)
            return UserProfile.objects.filter(user__username=username)
        return UserProfile.objects.all()


class MaxPixelsViewSet(viewsets.ModelViewSet):
    serializer_class = MaxPixelsSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        username = self.kwargs.get("user_username")
        if username is not None:
            get_object_or_404(UserProfile, user__username=username)
            return UserProfile.objects.filter(user__username=username)
        return UserProfile.objects.all()
