from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from rest_framework import permissions, viewsets, status
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework.decorators import action
import logging

from .forms import UserRegisterForm, UserModifyForm, UserProfileUpdateForm
from .models import UserProfile
from .serializers import (
    UserSerializer,
    TplaceSerializer,
    NyancoinsSerializer,
    ColorsSerializer,
    PixelsSerializer,
    MaxPixelsSerializer,
    LoginRequestSerializer,
    SignupRequestSerializer,
)

logger = logging.getLogger(__name__)


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

    @action(
        detail=False,
        methods=["post"],
        permission_classes=[],
        serializer_class=LoginRequestSerializer,
    )
    def login(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = authenticate(
            request,
            username=serializer.validated_data["username"],
            password=serializer.validated_data["password"],
        )
        if user is None:
            return Response({"detail": "Invalid credentials"}, status=401)
        login(request, user)
        data = UserSerializer(user, context={"request": request}).data
        return Response(data)

    @action(
        detail=False,
        methods=["post"],
        permission_classes=[permissions.IsAuthenticated],
    )
    def logout(self, request):
        logout(request)
        return Response({"detail": "Logged out."})

    @action(
        detail=False,
        methods=["post"],
        permission_classes=[permissions.AllowAny],
        serializer_class=SignupRequestSerializer,
    )
    def signup(self, request):
        logging.info("here we are %s", request)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        validated_data = serializer.validated_data
        logging.info("data valid %s", validated_data)
        password = validated_data["password1"]
        print(validated_data)

        user = User.objects.create_user(
            username=validated_data["username"],
            password=password,
            email=validated_data["email"],
        )

        login(request, user)
        data = UserSerializer(user, context={"request": request}).data
        return Response(data)

    def retrieve(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.get_serializer(user)
        data = serializer.data

        # fmt: off
        # Add available nested routes
        data["available_routes"] = {
            "tplace": request.build_absolute_uri(f"/api/users/{user.username}/tplace/"),
            "nyancoins": request.build_absolute_uri(f"/api/users/{user.username}/nyancoins/"),
            "colors": request.build_absolute_uri(f"/api/users/{user.username}/colors/"),
            "pixels": request.build_absolute_uri(f"/api/users/{user.username}/pixels/"),
            "max-pixels": request.build_absolute_uri(f"/api/users/{user.username}/max-pixels/"),
        }
        # fmt: on

        return Response(data)


class NestedUserProfileReadOnlyViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer

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
