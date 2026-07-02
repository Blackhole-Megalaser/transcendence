import logging
import random
from decimal import ROUND_CEILING, Decimal

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db import transaction
from django.db.models import Count
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
    EndTurnSerializer,
    FriendlistSerializer,
    FriendsSerializer,
    GuessSerializer,
    LoginRequestSerializer,
    MaxPixelsSerializer,
    NyancoinsGrantSerializer,
    NyancoinsSerializer,
    PixelPlaceSerializer,
    PixelSerializer,
    PixelsSerializer,
    SignupRequestSerializer,
    SkribbleRoomSerializer,
    SkribbleRoomSettingsSerializer,
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
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        validated_data = serializer.validated_data
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

            if profile.user.username == target_user.user.username:
                return Response(
                    {"detail": "You can't friend yourself!"},
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
            profile.next_regeneration = timezone.now() + profile.regeneration_delay
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
    queryset = SkribbleRoom.objects.annotate(num_players=Count("players")).filter(
        num_players__gt=0
    )
    serializer_class = SkribbleRoomSerializer
    lookup_field = "code"
    lookup_url_kwarg = "code"

    min_players = 2
    guesser_first_score = 200
    guesser_last_score = 50
    drawer_score_per_guesser = 70

    def get_permissions(self):
        if self.action in ["destroy", "update", "partial_update"]:
            permission_classes = [permissions.IsAdminUser]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        return (
            SkribbleRoom.objects.annotate(num_players=Count("players"))
            .filter(num_players__gt=0)
            .select_related("host__user", "current_word", "wordlist")
            .prefetch_related("players__player__user")
        )

    def _broadcast(self, room_code, event_type, **payload):
        from asgiref.sync import async_to_sync
        from channels.layers import get_channel_layer

        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f"chat_{room_code}",
            {
                "type": event_type,
                **payload,
            },
        )

    def _get_user_player(self, request):
        try:
            return request.user.userprofile.skribbleplayer
        except UserProfile.skribbleplayer.RelatedObjectDoesNotExist:
            return None

    def _get_room_player(self, request, room):
        player = self._get_user_player(request)
        if player is None or player.room_id != room.id:
            return None
        return player

    def _ordered_players(self, room):
        return list(room.players.select_related("player__user").order_by("order", "id"))

    def _current_drawer(self, room):
        return (
            room.players.select_related("player__user")
            .filter(order=room.current_player_index)
            .first()
        )

    def _is_host(self, request, room):
        return room.host_id == request.user.userprofile.id

    def _normalize_guess(self, value):
        return " ".join(value.casefold().strip().split())

    def _mask_word(self, word):
        return "".join(" " if char.isspace() else "_" for char in word)

    def _guess_score(self, room, now):
        timer_seconds = max(room.timer.total_seconds(), 1)
        remaining_seconds = max((room.timer_end - now).total_seconds(), 0)
        remaining_ratio = min(remaining_seconds / timer_seconds, 1)
        score_range = self.guesser_first_score - self.guesser_last_score
        return round(self.guesser_last_score + (score_range * remaining_ratio))

    def _drawer_score(self, room, found_count, now):
        if found_count <= 0:
            return 0
        timer_seconds = max(room.timer.total_seconds(), 1)
        remaining_seconds = max((room.timer_end - now).total_seconds(), 0)
        remaining_ratio = min(remaining_seconds / timer_seconds, 1)
        speed_multiplier = 0.5 + (0.5 * remaining_ratio)
        return round(self.drawer_score_per_guesser * found_count * speed_multiplier)

    def _all_guessers_found(self, room):
        drawer = self._current_drawer(room)
        guessers = room.players.all()
        if drawer is not None:
            guessers = guessers.exclude(pk=drawer.pk)
        return guessers.exists() and not guessers.filter(found=False).exists()

    def _winner_usernames(self, players):
        if not players:
            return []
        best_score = max(player.score for player in players)
        return [
            player.player.user.username
            for player in players
            if player.score == best_score
        ]

    def _room_state(self, room, request=None):
        players = self._ordered_players(room)
        drawer = self._current_drawer(room)
        request_player = None
        if request is not None and request.user.is_authenticated:
            request_player = self._get_room_player(request, room)

        is_request_drawer = (
            request_player is not None
            and drawer is not None
            and request_player.pk == drawer.pk
        )
        current_word = None
        word_mask = None
        if room.turn_started and room.current_word_id:
            word_value = room.current_word.word
            word_mask = self._mask_word(word_value)
            if is_request_drawer:
                current_word = word_value

        remaining_seconds = None
        if room.turn_started:
            remaining_seconds = max(
                round((room.timer_end - timezone.now()).total_seconds()), 0
            )

        return {
            "code": room.code,
            "name": room.name,
            "host": room.host.user.username if room.host_id else None,
            "is_host": self._is_host(request, room) if request is not None else False,
            "current_drawer": drawer.player.user.username
            if drawer is not None
            else None,
            "is_drawer": is_request_drawer,
            "players": [
                {
                    "username": player.player.user.username,
                    "order": player.order,
                    "score": player.score,
                    "found": player.found,
                    "is_host": player.player_id == room.host_id,
                    "is_drawer": drawer is not None and player.pk == drawer.pk,
                }
                for player in players
            ],
            "round_counter": room.round_counter,
            "max_rounds": room.max_rounds,
            "game_started": room.game_started,
            "game_finished": room.game_finished,
            "turn_started": room.turn_started,
            "current_player_index": room.current_player_index,
            "timer_seconds": round(room.timer.total_seconds()),
            "timer_end": room.timer_end,
            "remaining_seconds": remaining_seconds,
            "word": current_word,
            "word_mask": word_mask,
            "winners": self._winner_usernames(players) if room.game_finished else [],
        }

    def _require_player_in_room(self, request, room, message):
        player = self._get_room_player(request, room)
        if player is None:
            return None, Response({"detail": message}, status=HTTP_401_UNAUTHORIZED)
        return player, None

    def _shuffle_players(self, room):
        players = self._ordered_players(room)
        for index, player in enumerate(players):
            player.order = len(players) + index
            player.found = False
        if players:
            SkribblePlayer.objects.bulk_update(players, ["order", "found"])

        order = list(range(len(players)))
        random.shuffle(order)
        for index, player in enumerate(players):
            player.order = order[index]
        if players:
            SkribblePlayer.objects.bulk_update(players, ["order"])
        return players

    def _start_room_game(self, room, max_rounds=None):
        with transaction.atomic():
            room = SkribbleRoom.objects.select_for_update().get(pk=room.pk)
            if max_rounds is not None:
                room.max_rounds = max_rounds
            players = self._shuffle_players(room)
            for player in players:
                player.score = 0
            SkribblePlayer.objects.bulk_update(players, ["score"])
            room.word_history.clear()
            room.current_word = None
            room.current_player_index = 0
            room.round_counter = 1
            room.game_started = True
            room.game_finished = False
            room.turn_started = False
            room.timer_end = timezone.now() + room.timer
            room.save()
        self._broadcast(room.code, "game_started")
        self._broadcast(room.code, "state_changed")
        return room

    def _finish_turn(self, room, award_points=True, reason="manual"):
        now = timezone.now()
        drawer_points = 0
        with transaction.atomic():
            room = SkribbleRoom.objects.select_for_update().get(pk=room.pk)
            if not room.turn_started:
                return room, {"turn_ended": False, "drawer_points": 0}

            players = self._ordered_players(room)
            drawer = self._current_drawer(room)
            found_count = 0
            if drawer is not None:
                found_count = sum(
                    1 for player in players if player.pk != drawer.pk and player.found
                )

            if award_points and drawer is not None and found_count > 0:
                drawer_points = self._drawer_score(room, found_count, now)
                drawer.score += drawer_points
                drawer.save(update_fields=["score"])

            for player in players:
                player.found = False
            if players:
                SkribblePlayer.objects.bulk_update(players, ["found"])

            room.current_word = None
            room.turn_started = False
            room.timer_end = now

            active_players = self._ordered_players(room)
            if len(active_players) < self.min_players:
                room.game_started = False
                room.game_finished = True
            else:
                next_orders = [
                    player.order
                    for player in active_players
                    if player.order > room.current_player_index
                ]
                if next_orders:
                    room.current_player_index = min(next_orders)
                else:
                    room.current_player_index = min(
                        player.order for player in active_players
                    )
                    room.round_counter += 1

                if room.round_counter > room.max_rounds:
                    room.round_counter = room.max_rounds
                    room.game_started = False
                    room.game_finished = True

            room.save()

        self._broadcast(
            room.code,
            "turn_ended",
            reason=reason,
            drawer_points=drawer_points,
        )
        if room.game_finished:
            self._broadcast(room.code, "game_finished")
        self._broadcast(room.code, "state_changed")
        return room, {"turn_ended": True, "drawer_points": drawer_points}

    def create(self, request, *args, **kwargs):
        user_profile = request.user.userprofile
        old_room_code = None

        try:
            if user_profile.skribbleplayer.room:
                old_room_code = user_profile.skribbleplayer.room.code
        except UserProfile.skribbleplayer.RelatedObjectDoesNotExist:
            pass

        SkribbleRoom.cleanup_empty_rooms()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        with transaction.atomic():
            user_profile.leave_skribble()
            SkribbleRoom.cleanup_empty_rooms()
            serializer.save(host=user_profile)
            room = serializer.instance
            user_profile.join_skribble(room)

        if old_room_code:
            self._broadcast(old_room_code, "update_players")
        self._broadcast(room.code, "update_players")
        return Response(self.get_serializer(room).data, status=HTTP_201_CREATED)

    @action(methods=["get"], detail=True)
    def state(self, request, code):
        room = self.get_object()
        player, error = self._require_player_in_room(
            request, room, "You must join the room before you can inspect it"
        )
        if error:
            return error
        return Response(self._room_state(room, request))

    @action(methods=["post"], detail=True)
    def join(self, request, code):
        room = self.get_object()
        if room.game_started or room.game_finished:
            return Response(
                {"detail": "The game is not joinable"}, status=HTTP_409_CONFLICT
            )

        old_room_code = None
        try:
            current_room = request.user.userprofile.skribbleplayer.room
            if current_room.pk != room.pk:
                old_room_code = current_room.code
        except UserProfile.skribbleplayer.RelatedObjectDoesNotExist:
            pass

        request.user.userprofile.join_skribble(room)
        if room.host_id is None:
            room.host = request.user.userprofile
            room.save(update_fields=["host"])
        if old_room_code:
            self._broadcast(old_room_code, "update_players")
            self._broadcast(old_room_code, "state_changed")
        self._broadcast(room.code, "update_players")
        self._broadcast(room.code, "state_changed")
        return Response(self.get_serializer(room).data)

    @action(methods=["post"], detail=False)
    def leave(self, request):
        user_profile = request.user.userprofile
        room = None
        player = None

        try:
            player = user_profile.skribbleplayer
            room = player.room
        except UserProfile.skribbleplayer.RelatedObjectDoesNotExist:
            pass

        if room is None:
            return Response()

        room_code = room.code
        drawer_left = room.turn_started and player.order == room.current_player_index

        with transaction.atomic():
            user_profile.leave_skribble()
            if SkribbleRoom.objects.filter(pk=room.pk).exists():
                room = SkribbleRoom.objects.select_for_update().get(pk=room.pk)
                if room.host_id == user_profile.id:
                    next_player = (
                        room.players.select_related("player").order_by("order").first()
                    )
                    room.host = next_player.player if next_player is not None else None
                    room.save(update_fields=["host"])
            SkribbleRoom.cleanup_empty_rooms()
            room_exists = SkribbleRoom.objects.filter(pk=room.pk).exists()

        if room_exists:
            room = SkribbleRoom.objects.get(pk=room.pk)
            if room.game_started and room.players.count() < self.min_players:
                room.game_started = False
                room.game_finished = True
                room.turn_started = False
                room.current_word = None
                room.save()
                self._broadcast(room_code, "game_finished")
            elif drawer_left:
                self._finish_turn(room, award_points=False, reason="drawer_left")
            elif room.turn_started and self._all_guessers_found(room):
                self._finish_turn(room, reason="all_found")

        self._broadcast(room_code, "update_players")
        self._broadcast(room_code, "state_changed")
        return Response()

    @action(methods=["post"], detail=True)
    def start_game(self, request, code):
        room = self.get_object()
        player, error = self._require_player_in_room(
            request, room, "You must join the room before you can start the game"
        )
        if error:
            return error
        if not self._is_host(request, room):
            return Response(
                {"detail": "Only the room host can start the game"},
                status=HTTP_403_FORBIDDEN,
            )
        if room.game_started:
            return Response(
                {"detail": "The game already started"}, status=HTTP_409_CONFLICT
            )
        if room.game_finished:
            return Response(
                {"detail": "Replay the room to start a new game"},
                status=HTTP_409_CONFLICT,
            )
        if room.players.count() < self.min_players:
            return Response(
                {"detail": "At least two players are required to start the game"},
                status=HTTP_400_BAD_REQUEST,
            )
        room = self._start_room_game(room)
        return Response(self.get_serializer(room).data)

    @action(
        methods=["post"],
        detail=True,
        serializer_class=SkribbleRoomSettingsSerializer,
    )
    def configure(self, request, code):
        room = self.get_object()
        player, error = self._require_player_in_room(
            request, room, "You must join the room before you can configure it"
        )
        if error:
            return error
        if not self._is_host(request, room):
            return Response(
                {"detail": "Only the room host can configure the game"},
                status=HTTP_403_FORBIDDEN,
            )
        if room.game_started:
            return Response(
                {"detail": "The game already started"}, status=HTTP_409_CONFLICT
            )

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        max_rounds = serializer.validated_data.get("max_rounds")
        if max_rounds is not None:
            room.max_rounds = max_rounds
            room.save(update_fields=["max_rounds"])

        self._broadcast(room.code, "state_changed")
        return Response(SkribbleRoomSerializer(room).data)

    @action(
        methods=["post"],
        detail=True,
        serializer_class=SkribbleRoomSettingsSerializer,
    )
    def replay(self, request, code):
        room = self.get_object()
        player, error = self._require_player_in_room(
            request, room, "You must join the room before you can replay it"
        )
        if error:
            return error
        if not self._is_host(request, room):
            return Response(
                {"detail": "Only the room host can replay the game"},
                status=HTTP_403_FORBIDDEN,
            )
        if room.players.count() < self.min_players:
            return Response(
                {"detail": "At least two players are required to replay the game"},
                status=HTTP_400_BAD_REQUEST,
            )

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        room = self._start_room_game(
            room, max_rounds=serializer.validated_data.get("max_rounds")
        )
        self._broadcast(room.code, "game_restarted")
        return Response(SkribbleRoomSerializer(room).data)

    @action(methods=["get"], detail=True)
    def select_word(self, request, code):
        room = self.get_object()
        player, error = self._require_player_in_room(
            request, room, "You must join the room before you can start a turn"
        )
        if error:
            return error
        if room.game_finished:
            return Response(
                {"detail": "The game is finished"}, status=HTTP_400_BAD_REQUEST
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
        words = (
            room.wordlist.words.exclude(id__in=room.word_history.all())
            .order_by("?")
            .values_list("word", flat=True)[:3]
        )
        return Response({"words": list(words)})

    @action(methods=["post"], detail=True, serializer_class=StartTurnSerializer)
    def start_turn(self, request, code):
        room = self.get_object()
        player, error = self._require_player_in_room(
            request, room, "You must join the room before you play"
        )
        if error:
            return error
        if room.game_finished:
            return Response(
                {"detail": "The game is finished"}, status=HTTP_400_BAD_REQUEST
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
        chosen_word = serializer.validated_data["word"]

        try:
            word = (
                room.wordlist.words.exclude(id__in=room.word_history.all())
                .filter(word=chosen_word)
                .get()
            )
        except Word.DoesNotExist:
            return Response(
                {"detail": "The word you have chosen is invalid"},
                status=HTTP_400_BAD_REQUEST,
            )

        with transaction.atomic():
            room = SkribbleRoom.objects.select_for_update().get(pk=room.pk)
            room.word_history.add(word)
            room.current_word = word
            room.timer_end = timezone.now() + room.timer
            room.turn_started = True
            room.save()
            room.players.update(found=False)

        self._broadcast(room.code, "canvas_reset")
        self._broadcast(room.code, "turn_started")
        self._broadcast(room.code, "state_changed")
        return Response(self._room_state(room, request))

    @action(methods=["post"], detail=True, serializer_class=GuessSerializer)
    def guess(self, request, code):
        room = self.get_object()
        player, error = self._require_player_in_room(
            request, room, "You must join the room before you can guess"
        )
        if error:
            return error
        if not room.game_started or room.game_finished:
            return Response(
                {"detail": "There is no active game"}, status=HTTP_400_BAD_REQUEST
            )
        if not room.turn_started or not room.current_word_id:
            return Response(
                {"detail": "There is no active turn"}, status=HTTP_400_BAD_REQUEST
            )
        if player.order == room.current_player_index:
            return Response(
                {"detail": "The drawer cannot guess"}, status=HTTP_400_BAD_REQUEST
            )
        if timezone.now() >= room.timer_end:
            room, turn_info = self._finish_turn(room, reason="timer")
            return Response(
                {
                    "correct": False,
                    "turn_ended": turn_info["turn_ended"],
                    "state": self._room_state(room, request),
                }
            )

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        guess = self._normalize_guess(serializer.validated_data["guess"])
        expected = self._normalize_guess(room.current_word.word)
        if guess != expected:
            return Response({"correct": False, "turn_ended": False})
        if player.found:
            return Response(
                {"correct": True, "already_found": True, "turn_ended": False}
            )

        timer_expired = False
        with transaction.atomic():
            room = SkribbleRoom.objects.select_for_update().get(pk=room.pk)
            if not room.turn_started or not room.current_word_id:
                return Response({"correct": False, "turn_ended": True})
            if guess != self._normalize_guess(room.current_word.word):
                return Response({"correct": False, "turn_ended": False})

            now = timezone.now()
            if now >= room.timer_end:
                timer_expired = True
            else:
                player = SkribblePlayer.objects.select_for_update().get(pk=player.pk)
                if player.found:
                    return Response(
                        {"correct": True, "already_found": True, "turn_ended": False}
                    )
                points = self._guess_score(room, now)
                player.found = True
                player.score += points
                player.save(update_fields=["found", "score"])

        if timer_expired:
            room, turn_info = self._finish_turn(room, reason="timer")
            return Response(
                {
                    "correct": False,
                    "turn_ended": turn_info["turn_ended"],
                    "state": self._room_state(room, request),
                }
            )

        self._broadcast(
            room.code,
            "player_found",
            username=player.player.user.username,
            points=points,
        )

        turn_ended = False
        drawer_points = 0
        if self._all_guessers_found(room):
            room, turn_info = self._finish_turn(room, reason="all_found")
            turn_ended = turn_info["turn_ended"]
            drawer_points = turn_info["drawer_points"]
        else:
            room.refresh_from_db()
            self._broadcast(room.code, "state_changed")

        return Response(
            {
                "correct": True,
                "points": points,
                "turn_ended": turn_ended,
                "drawer_points": drawer_points,
                "state": self._room_state(room, request),
            }
        )

    @action(methods=["post"], detail=True, serializer_class=EndTurnSerializer)
    def end_turn(self, request, code):
        room = self.get_object()
        player, error = self._require_player_in_room(
            request, room, "You must join the room before you can end a turn"
        )
        if error:
            return error
        if not room.turn_started:
            return Response(
                {"detail": "There is no active turn"}, status=HTTP_400_BAD_REQUEST
            )

        timer_expired = timezone.now() >= room.timer_end
        is_drawer = player.order == room.current_player_index
        if not (timer_expired or is_drawer or self._is_host(request, room)):
            return Response(
                {"detail": "Only the host, drawer, or timer can end the turn"},
                status=HTTP_403_FORBIDDEN,
            )

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        reason = "timer" if timer_expired else serializer.validated_data["reason"]
        room, turn_info = self._finish_turn(room, reason=reason)
        return Response(
            {
                "turn_ended": turn_info["turn_ended"],
                "drawer_points": turn_info["drawer_points"],
                "state": self._room_state(room, request),
            }
        )
