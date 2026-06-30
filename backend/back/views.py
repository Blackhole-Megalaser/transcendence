import logging
import random
from decimal import ROUND_CEILING, Decimal

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db import transaction
from django.db.models import Count, Max
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED,
    HTTP_402_PAYMENT_REQUIRED,
    HTTP_403_FORBIDDEN,
    HTTP_409_CONFLICT,
)
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from .forms import UserModifyForm, UserProfileUpdateForm, UserRegisterForm
from .models import (
    Color,
    Pixel,
    SkribblePlayer,
    SkribbleRoom,
    UserProfile,
    Word,
    WordList,
)
from .serializers import (
    AvatarSerializer,
    EmailUpdateSerializer,
    FriendlistSerializer,
    FriendsSerializer,
    LoginRequestSerializer,
    MaxPixelsSerializer,
    NyancoinsGrantSerializer,
    NyancoinsSerializer,
    PixelPlaceSerializer,
    PixelSerializer,
    PixelsSerializer,
    SignupRequestSerializer,
    SkribbleRoomSerializer,
    StartTurnSerializer,
    TplaceSerializer,
    TplaceUpgradePurchaseSerializer,
    UnlockedColorsSerializer,
    UserProfileSerializer,
    UserSerializer,
    WordListSerializer,
)

logger = logging.getLogger(__name__)

MAX_PIXEL_UPGRADE_PRICE = 150
COOLDOWN_UPGRADE_BASE_PRICE = 300
COOLDOWN_UPGRADE_PRICE_MULTIPLIER = Decimal("1.10")
BASE_REGENERATION_DELAY_SECONDS = 60
MIN_REGENERATION_DELAY_SECONDS = 15


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
    lookup_field = "username"
    lookup_value_regex = "[a-zA-Z0-9-_@.+]+"

    def get_permissions(self):
        """
        Admins can do anything, users can only access their own info
        """
        permission_classes = [permissions.IsAdminUser]
        if self.action in ["retrieve", "change_email"]:
            requester_username = self.request.user.username
            wanted_username = self.get_object().username
            request_for_own_info = requester_username == wanted_username
            if request_for_own_info:
                permission_classes = [permissions.IsAuthenticated]
        if self.action in ["logout"]:
            permission_classes = [permissions.IsAuthenticated]
        elif self.action in ["login", "signup"]:
            permission_classes = [permissions.AllowAny]
        got_permissions = [permission() for permission in permission_classes]
        return got_permissions

    def get_object(self):
        username = self.kwargs.get("username")
        if username == "me":
            return self.request.user
        if username is None:
            return self.get_queryset()
        else:
            return self.get_queryset().get(username=username)

    @action(
        detail=False,
        methods=["post"],
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
    )
    def logout(self, request):
        logout(request)
        return Response({"detail": "Logged out."})

    @action(
        detail=False,
        methods=["post"],
        serializer_class=SignupRequestSerializer,
    )
    def signup(self, request):
        logging.info("here we are %s", request)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        validated_data = serializer.validated_data
        logging.info("data valid %s", validated_data)
        username = validated_data["username"]
        password = validated_data["password1"]

        if not str.isascii(username):
            return Response({"detail": "Invalid characters (ASCII only)"}, status=400)

        if self.queryset.filter(username=username).exists():
            return Response({"detail": "This username is already taken"}, status=409)

        user = User.objects.create_user(
            username=validated_data["username"],
            password=password,
            email=validated_data["email"],
        )

        login(request, user)
        data = UserSerializer(user, context={"request": request}).data
        return Response(data)

    # currently not double check for password since email is not used for anything
    # you need to be logged still to change your mail
    @action(
        detail=True,
        methods=["post"],
        serializer_class=EmailUpdateSerializer,
    )
    def change_email(self, request, username):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = self.get_object()
        user.email = serializer.validated_data["email"]  # pyright: ignore[reportOptionalSubscript]
        user.save()

        return Response({"detail": "Email adress changed successfully."}, status=200)


class NestedUserProfileBase:
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer

    def get_parent_user(self):
        username = self.kwargs.get("user")
        if username is None or username == "me":
            return self.request.user
        if username != self.request.user.username and not self.request.user.is_staff:
            raise PermissionDenied("You cannot access another user's profile data.")
        return get_object_or_404(User, username=username)

    def get_profile(self):
        parent_user = self.get_parent_user()
        profile = parent_user.userprofile
        profile.regenerate_pixels()
        return profile

    def get_object(self):
        return self.get_profile()


class NestedUserProfileView(NestedUserProfileBase, RetrieveAPIView):
    """
    Read-only NestedUserProfileView
    """


class TplaceView(NestedUserProfileView, RetrieveAPIView):
    serializer_class = TplaceSerializer


class NyancoinsView(NestedUserProfileView, RetrieveAPIView):
    serializer_class = NyancoinsSerializer


class ColorsView(NestedUserProfileView, RetrieveAPIView):
    serializer_class = UnlockedColorsSerializer


# /api/users/me/pixels
class UserPixelsView(NestedUserProfileView, RetrieveAPIView):
    serializer_class = PixelsSerializer


class MaxPixelsView(NestedUserProfileView, RetrieveAPIView):
    serializer_class = MaxPixelsSerializer


# /api/users/me/friends
class FriendsView(NestedUserProfileView, RetrieveAPIView):
    serializer_class = FriendsSerializer


# /api/users/me/friendlist
class FriendlistView(NestedUserProfileView, RetrieveAPIView):
    serializer_class = FriendlistSerializer


# /api/users/me/friend_request
class FriendsRequestView(NestedUserProfileBase, APIView):
    def get_permissions(self):
        """
        Users can only access their own info. Admins can access everyones.
        """
        if (
            self.request.user.is_anonymous
            or self.request.user.username != self.get_object().user.username
        ):
            permission_classes = [permissions.IsAdminUser]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]

    def get(self, request, user):
        profile = self.get_object()
        serializer = UserProfileSerializer(
            profile.pending_friend_requests.all(), many=True
        )
        return Response({"pending_friend_requests": serializer.data})

    def post(self, request, user):
        action = request.data.get("action")
        username = request.data.get("username")

        # action = [send / accept / reject] only
        if action not in {"send", "accept", "reject", "remove_friend"}:
            return Response(
                {"detail": "Invalid action."},
                status=HTTP_400_BAD_REQUEST,
            )

        profile = self.get_object()
        try:
            target_user = get_object_or_404(UserProfile, user__username=username)
        except Http404:
            return Response(
                {"detail": "User doesn't exist."},
                status=HTTP_403_FORBIDDEN,
            )

        if action == "send":
            if profile.friends.filter(id=target_user.id).exists():
                return Response(
                    {"detail": "User already in friendlist."},
                    status=HTTP_403_FORBIDDEN,
                )

            target_user.pending_friend_requests.add(profile)
            return Response(
                {"detail": "Friend request sent."},
                status=HTTP_200_OK,
            )

        if action in {"accept", "reject"}:
            if not profile.pending_friend_requests.filter(id=target_user.id).exists():
                return Response(
                    {"detail": "No such request."},
                    status=HTTP_400_BAD_REQUEST,
                )

            if action == "accept":
                profile.friends.add(target_user)
                target_user.friends.add(profile)

            profile.pending_friend_requests.remove(target_user)
            return Response(
                {"detail": f"Friend request {action}ed."},
                status=HTTP_200_OK,
            )

        if action == "remove_friend":
            if not profile.friends.filter(id=target_user.id).exists():
                return Response(
                    {"detail": "Not in friend list."}, status=HTTP_400_BAD_REQUEST
                )

            profile.friends.remove(target_user)
            target_user.friends.remove(profile)
            return Response({"detail": "Friend removed."}, status=HTTP_200_OK)


def get_cooldown_upgrade_count(profile):
    current_seconds = int(profile.regeneration_delay.total_seconds())
    return max(0, BASE_REGENERATION_DELAY_SECONDS - current_seconds)


def get_cooldown_upgrade_price(upgrade_index):
    price = Decimal(COOLDOWN_UPGRADE_BASE_PRICE) * (
        COOLDOWN_UPGRADE_PRICE_MULTIPLIER**upgrade_index
    )
    return int(price.to_integral_value(rounding=ROUND_CEILING))


def get_cooldown_upgrade_total_price(first_upgrade_index, quantity):
    return sum(
        get_cooldown_upgrade_price(first_upgrade_index + offset)
        for offset in range(quantity)
    )


def get_tplace_upgrade_response(profile, nyancoins_spent):
    data = TplaceSerializer(profile).data
    data["nyancoins_spent"] = nyancoins_spent
    return Response(data, status=HTTP_200_OK)


class TplaceMaxPixelsUpgradeView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = TplaceUpgradePurchaseSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        quantity = serializer.validated_data["quantity"]
        total_cost = quantity * MAX_PIXEL_UPGRADE_PRICE

        with transaction.atomic():
            profile = UserProfile.objects.select_for_update().get(user=request.user)
            profile.regenerate_pixels()

            if profile.nyancoins < total_cost:
                return Response(
                    {
                        "detail": "Not enough nyancoins",
                        "required_nyancoins": total_cost,
                        "nyancoins": profile.nyancoins,
                    },
                    status=HTTP_409_CONFLICT,
                )

            profile.nyancoins -= total_cost
            profile.max_placable_pixels += quantity
            profile.save(update_fields=["nyancoins", "max_placable_pixels"])

        return get_tplace_upgrade_response(profile, total_cost)


class TplaceRegenerationDelayUpgradeView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = TplaceUpgradePurchaseSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        quantity = serializer.validated_data["quantity"]
        delay_reduction = timezone.timedelta(seconds=quantity)

        with transaction.atomic():
            profile = UserProfile.objects.select_for_update().get(user=request.user)
            profile.regenerate_pixels()

            next_regeneration_delay = profile.regeneration_delay - delay_reduction
            if next_regeneration_delay.total_seconds() < MIN_REGENERATION_DELAY_SECONDS:
                return Response(
                    {"detail": "Regeneration delay cannot go below 15 seconds"},
                    status=HTTP_400_BAD_REQUEST,
                )

            cooldown_upgrades = get_cooldown_upgrade_count(profile)
            total_cost = get_cooldown_upgrade_total_price(cooldown_upgrades, quantity)
            if profile.nyancoins < total_cost:
                return Response(
                    {
                        "detail": "Not enough nyancoins",
                        "required_nyancoins": total_cost,
                        "nyancoins": profile.nyancoins,
                    },
                    status=HTTP_409_CONFLICT,
                )

            profile.nyancoins -= total_cost
            profile.regeneration_delay = next_regeneration_delay
            if profile.placable_pixels < profile.max_placable_pixels:
                profile.next_regeneration = max(
                    timezone.now(),
                    profile.next_regeneration - delay_reduction,
                )
            profile.save(
                update_fields=[
                    "nyancoins",
                    "regeneration_delay",
                    "next_regeneration",
                ]
            )

        return get_tplace_upgrade_response(profile, total_cost)


class AvatarView(NestedUserProfileBase, APIView):
    serializer_class = AvatarSerializer

    def get_permissions(self):
        """
        Users can update only their own avatar. Admin can update everyone's avatar.
        """
        if (
            self.request.user.is_anonymous
            or self.request.user.username != self.get_object().user.username
        ):
            permission_classes = [permissions.IsAdminUser]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]

    def response(self, request):
        image = self.get_object().profile_image
        if image:
            return Response({"url": request.build_absolute_uri(image.url)})
        else:
            return Response({"url": None})

    def post(self, request, user):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        profile = self.get_object()

        profile.profile_image = serializer.validated_data["profile_image"]  # pyright: ignore[reportOptionalSubscript]
        profile.save()
        return self.response(request)

    def get(self, request, user):
        return self.response(request)


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
            if profile.placable_pixels == profile.max_placable_pixels:
                profile.next_regeneration = timezone.now() + profile.regeneration_delay  # pyright: ignore[reportOperatorIssue]
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


# /api/tplace/giveme/
class TplaceGiveNyancoinsView(APIView):
    permission_classes = [permissions.IsAdminUser]
    serializer_class = NyancoinsGrantSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        amount = serializer.validated_data["amount"]

        with transaction.atomic():
            profile = UserProfile.objects.select_for_update().get(user=request.user)
            profile.regenerate_pixels()
            profile.nyancoins += amount
            profile.save(update_fields=["nyancoins"])

        data = TplaceSerializer(profile).data
        data["nyancoins_added"] = amount
        return Response(data, status=HTTP_200_OK)


# /api/tplace/canvas/
class CanvasView(APIView):
    """
    Get the canvas dimensions, palette and non-default pixels.
    """

    def get(self, request):
        width = settings.TPLACE_MAX_X
        height = settings.TPLACE_MAX_Y
        palette = {}
        default_color_id = None

        for hex_code, pk in Color.objects.values_list("hex_code", "pk"):
            palette[pk] = hex_code
            if hex_code == "#FFFFFF":
                default_color_id = pk

        pixels = [
            {"x_pos": x_pos, "y_pos": y_pos, "color_id": color_id}
            for x_pos, y_pos, color_id in Pixel.objects.filter(
                x_pos__gte=0,
                x_pos__lt=width,
                y_pos__gte=0,
                y_pos__lt=height,
            )
            .values_list("x_pos", "y_pos", "color_id")
            .iterator()
        ]

        return Response(
            {
                "width": width,
                "height": height,
                "encoding": "sparse",
                "default_color_id": default_color_id,
                "palette": palette,
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

    @action(methods=["GET"], detail=True)
    def random(self, request, name):
        """
        Get a random word from a wordlist
        """
        wordlist = self.get_object()
        word = wordlist.words.order_by("?").first()
        return Response({"word": word.word})


class SkribbleRoomViewSet(ModelViewSet):
    """
    Skribble room view
    """

    queryset = SkribbleRoom.objects.annotate(num_players=Count("players")).filter(
        num_players__gt=0
    )
    serializer_class = SkribbleRoomSerializer
    lookup_field = "code"
    lookup_url_kwarg = "code"

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action in ["destroy", "update", "partial_update"]:
            permission_classes = [permissions.IsAdminUser]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]

    def create(self, request, *args, **kwargs):
        user_profile = request.user.userprofile
        old_room_code = None

        try:
            if (
                hasattr(user_profile, "skribbleplayer")
                and user_profile.skribbleplayer.room
            ):
                old_room_code = user_profile.skribbleplayer.room.code
        except Exception:
            pass

        SkribbleRoom.cleanup_empty_rooms()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        with transaction.atomic():
            request.user.userprofile.leave_skribble()
            SkribbleRoom.cleanup_empty_rooms()
            self.perform_create(serializer)
            room = serializer.instance
            request.user.userprofile.join_skribble(room)

        if old_room_code:
            from channels.layers import get_channel_layer
            from asgiref.sync import async_to_sync

            def send_websocket_update():
                channel_layer = get_channel_layer()
                async_to_sync(channel_layer.group_send)(
                    f"chat_{old_room_code}",
                    {
                        "type": "update_players",
                    },
                )

            transaction.on_commit(send_websocket_update)
        return Response(self.get_serializer(room).data, status=HTTP_201_CREATED)

    @action(methods=["post"], detail=True)
    def join(self, request, code):
        """
        Join an existing room.

        1. Player will leave any room they joined (will trigger empty room cleanup)
        2. Player will join the specified room

        Preconditions:

        1. A game can only be joined if it has not started -> 409 Conflict

        Returns the current room status
        """
        room = self.get_object()
        if room.game_started:
            return Response(
                {"detail": "The game already started"}, status=HTTP_409_CONFLICT
            )
        request.user.userprofile.join_skribble(room)

        from channels.layers import get_channel_layer
        from asgiref.sync import async_to_sync

        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f"chat_{room.code}",
            {
                "type": "update_players",
            },
        )
        return Response(self.get_serializer(room).data)

    @action(methods=["post"], detail=False)
    def leave(self, request):
        """
        Leave the room.

        1. Player will leave any room they are in (will trigger empty room cleanup)

        As a reminder, a player can only be in one room at once.

        Always succeeds, no data is returned.
        """
        user_profile = request.user.userprofile
        room_code = None

        try:
            if (
                hasattr(user_profile, "skribbleplayer")
                and user_profile.skribbleplayer.room
            ):
                room_code = user_profile.skribbleplayer.room.code
        except Exception:
            pass

        with transaction.atomic():
            request.user.userprofile.leave_skribble()
            SkribbleRoom.cleanup_empty_rooms()

        if room_code:
            from channels.layers import get_channel_layer
            from asgiref.sync import async_to_sync

            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                f"chat_{room_code}",
                {
                    "type": "update_players",
                },
            )
        return Response()

    @action(methods=["post"], detail=True)
    def start_game(self, request, code):
        """
        Start the game in a room.

        1. Shuffles the player order
        2. Set game_started to true

        Next: The first player in the order should call select_word to get a choice of words

        Preconditions:

        1. Only a player in the room can start the game -> 401 Unauthorized
        2. A game can only be started if it wasn't already -> 409 Conflict

        Returns the current room status.
        """
        room = self.get_object()
        player = request.user.userprofile.skribbleplayer
        room_players = room.players.all()
        if player not in room_players:
            return Response(
                {"detail": "You must join the room before you can start the game"},
                status=HTTP_401_UNAUTHORIZED,
            )
        if room.game_started:
            return Response(
                {"detail": "The game already started"}, status=HTTP_409_CONFLICT
            )
        with transaction.atomic():
            num_players = len(room_players)

            # first set it to a dummy value that is too high to cause conflicts
            max_order = (
                SkribblePlayer.objects.select_for_update()
                .filter(room=room)
                .aggregate(m=Max("order"))
                .get("m")
            )
            for i, p in enumerate(room_players):
                p.order = max_order + 1 + i
            SkribblePlayer.objects.bulk_update(room_players, ["order"])

            # then actually shuffle the order
            order = list(range(num_players))
            random.shuffle(order)
            for i, p in enumerate(room_players):
                p.order = order[i]
            SkribblePlayer.objects.bulk_update(room_players, ["order"])

            # do the bookkeeping
            room.game_started = True
            room.round_counter = 1
            room.save()

        from channels.layers import get_channel_layer
        from asgiref.sync import async_to_sync

        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f"chat_{room.code}",
            {
                "type": "game_started",
            },
        )

        return Response(self.get_serializer(room).data)

    @action(methods=["get"], detail=True)
    def select_word(self, request, code):
        """
        Get 3 possible words, that the player may draw during their turn.

        Next: The player should call start_turn with their selected word.

        Preconditions:

        1. The player is in the room -> 401 Unauthorized
        2. The game has started -> 400 Bad Request
        3. The player is the current player -> 401 Unauthorized
        4. The turn has not started yet -> 400 Bad Request

        Returns three words chosen at random from the room's wordlist, that have not appeared in the room as of yet.
        """
        room = self.get_object()
        try:
            player = request.user.userprofile.skribbleplayer
        except UserProfile.skribbleplayer.RelatedObjectDoesNotExist:
            player = None
        room_players = room.players.all()
        if not player or player not in room_players:
            return Response(
                {"detail": "You must join the room before you can start a turn"},
                status=HTTP_401_UNAUTHORIZED,
            )
        if not room.game_started:
            return Response(
                {"detail": "The game has not started yet"}, status=HTTP_400_BAD_REQUEST
            )
        if player.order != room.current_player_index:
            return Response(
                {"detail": "It is not your turn"}, status=HTTP_401_UNAUTHORIZED
            )
        if room.turn_started:
            return Response(
                {"detail": "The turn already started"}, status=HTTP_400_BAD_REQUEST
            )
        wordlist = room.wordlist
        # Yes, this does the limit on the DB side
        # https://docs.djangoproject.com/en/6.0/topics/db/queries/#limiting-querysets
        words = (
            wordlist.words.exclude(id__in=room.word_history.all())
            .order_by("?")
            .values_list("word", flat=True)[:3]
        )
        return Response({"words": words})

    @action(methods=["post"], detail=True, serializer_class=StartTurnSerializer)
    def start_turn(self, request, code):
        """
        The player has chosen a word to draw, and starts drawing now.

        1. The chosen word is added to the word_history of that room.
        2. The timer is reset and starts counting down
        3. The turn starts

        Preconditions:
        1. The player is in the room -> 401 Unauthorized
        2. The game has started -> 400 Bad Request
        3. The player is the current player -> 401 Unauthorized
        4. The turn not has started yet -> 400 Bad Request
        5. The word is not in word_history, but in the current wordlist -> 400 Bad Request

        Returns the current room status.
        """
        room = self.get_object()
        try:
            player = request.user.userprofile.skribbleplayer
        except UserProfile.skribbleplayer.RelatedObjectDoesNotExist:
            player = None
        room_players = room.players.all()
        if not player or player not in room_players:
            return Response(
                {"detail": "You must join the room before you play"},
                status=HTTP_401_UNAUTHORIZED,
            )
        if not room.game_started:
            return Response(
                {"detail": "The game has not started yet"}, status=HTTP_400_BAD_REQUEST
            )
        if player.order != room.current_player_index:
            return Response(
                {"detail": "It is not your turn"}, status=HTTP_401_UNAUTHORIZED
            )
        if room.turn_started:
            return Response(
                {"detail": "The turn already started"}, status=HTTP_400_BAD_REQUEST
            )
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        word = serializer.validated_data["word"]

        wordlist = room.wordlist
        try:
            word = (
                wordlist.words.exclude(id__in=room.word_history.all())
                .filter(word=word)
                .get()
            )
        except Word.DoesNotExist:
            return Response(
                {"detail": "The word you have chosen is invalid"},
                status=HTTP_400_BAD_REQUEST,
            )

        with transaction.atomic():
            room.word_history.add(word)
            room.timer_end = timezone.now() + room.timer
            room.turn_started = True
            room.save()

        return Response(SkribbleRoomSerializer(room).data)
