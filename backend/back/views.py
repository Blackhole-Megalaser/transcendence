import logging

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect, render
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_402_PAYMENT_REQUIRED,
    HTTP_409_CONFLICT,
)
from rest_framework.views import APIView
from rest_framework.viewsets import ReadOnlyModelViewSet

from .forms import UserModifyForm, UserProfileUpdateForm, UserRegisterForm
from .models import Color, Pixel, UserProfile, WordList
from .serializers import (
    LoginRequestSerializer,
    MaxPixelsSerializer,
    NyancoinsSerializer,
    PixelPlaceSerializer,
    PixelSerializer,
    PixelsSerializer,
    SignupRequestSerializer,
    TplaceSerializer,
    UnlockedColorsSerializer,
    UserSerializer,
    WordListSerializer,
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


class NestedUserProfileView(RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer

    def get_parent_user(self):
        username = self.kwargs.get("user_username")
        if username is None or username == "me":
            return self.request.user
        if username != self.request.user.username and not self.request.user.is_staff:
            raise PermissionDenied("You cannot access another user's profile data.")
        return get_object_or_404(User, username=username)

    def get_object(self):
        parent_user = self.get_parent_user()
        profile = parent_user.userprofile
        profile.regenerate_pixels()
        return profile


class TplaceView(NestedUserProfileView):
    serializer_class = TplaceSerializer


class NyancoinsView(NestedUserProfileView):
    serializer_class = NyancoinsSerializer


class ColorsView(NestedUserProfileView):
    serializer_class = UnlockedColorsSerializer


# /api/users/me/pixels
class UserPixelsView(NestedUserProfileView):
    serializer_class = PixelsSerializer


class MaxPixelsView(NestedUserProfileView):
    serializer_class = MaxPixelsSerializer


# /api/tplace/pixels/
class PixelPlaceView(APIView):
    """
    Place a pixel at the specified x and y coordinates.

    Color matches on the name of the color.

    In case of non unlocked color, return HTTP 402 payment required

    In case of not enough pixels for that user, return HTTP 409 conflict

    If the pixel at that position already has the same color as the one in the request,
    no nyancoins are awarded and no placable pixels are deducted. HTTP 200 OK is returned.

    Otherwise, 1 nyancoin is awarded and HTTP 201 CREATED returned.

    Pixels not present in the database are assumed to have the color with name 'White'.
    If that color does not exist in the db, then the user's placed color
    is alwyas assumed to be different.
    """

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = PixelPlaceSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        logger.debug("pixel place: ", serializer.data)

        user = request.user
        profile = user.userprofile
        profile.regenerate_pixels()

        color = Color.objects.filter(name=serializer.data["color"]).first()
        color_unlocked = profile.unlocked_colors.contains(color)
        if not color_unlocked:
            return Response(
                {"detail": "Color not unlocked"}, status=HTTP_402_PAYMENT_REQUIRED
            )

        x_pos, y_pos = serializer.data["x_pos"], serializer.data["y_pos"]

        user_placable_pixels = profile.placable_pixels
        if user_placable_pixels <= 0:
            return Response(
                {"detail": "No more pixels to place"}, status=HTTP_409_CONFLICT
            )

        nyancoins_gained = 0
        status = HTTP_200_OK
        try:
            pixel = Pixel.objects.get(x_pos=x_pos, y_pos=y_pos)
            pixel_color = pixel.color
        except Pixel.DoesNotExist:
            pixel = Pixel(x_pos=x_pos, y_pos=y_pos)
            try:
                pixel_color = Color.objects.get(name="White")
            except Color.DoesNotExist:
                pixel_color = None

        if pixel_color != color:
            pixel.color = color
            pixel.user = user
            pixel.save()
            profile.placable_pixels -= 1
            profile.nyancoins += 1
            nyancoins_gained = 1
            status = HTTP_201_CREATED
            profile.save()

        return Response(
            {
                "pixel": PixelSerializer(pixel).data,
                "placable_pixels": profile.placable_pixels,
                "max_placable_pixels": profile.max_placable_pixels,
                "next_pixel_at": profile.next_regeneration,
                "nyancoins": profile.nyancoins,
                "nyancoins_gained": nyancoins_gained,
            },
            status=status,
        )


class CanvasView(APIView):
    """
    Get the full canvas
    """

    def get(self, request):
        width = settings.TPLACE_MAX_X
        height = settings.TPLACE_MAX_Y
        index = {}
        for hex_code, pk in Color.objects.values_list("hex_code", "pk"):
            index[pk] = hex_code
            if hex_code == "#FFFFFF":
                default_color_index = pk

        pixels = [default_color_index] * width * height
        for x_pos, y_pos, color_id in Pixel.objects.select_related("color").values_list(
            "x_pos", "y_pos", "color_id"
        ):
            pixels[x_pos + y_pos * height] = color_id

        return Response(
            {
                "width": width,
                "height": height,
                "palette": index,
                "pixels": pixels,
            }
        )


class WordListViewSet(ReadOnlyModelViewSet):
    """
    Get a wordlist
    """

    queryset = WordList.objects.all()
    serializer_class = WordListSerializer
    lookup_field = "name"
