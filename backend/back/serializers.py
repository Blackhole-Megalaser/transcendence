from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.exceptions import ValidationError
from django.core.validators import (
    MaxValueValidator,
    MinValueValidator,
)
from rest_framework import serializers
from rest_framework.relations import StringRelatedField

from .models import Color, Pixel, SkribblePlayer, SkribbleRoom, UserProfile, WordList


class PlayerSerializer(serializers.ModelSerializer):
    room = serializers.SlugRelatedField(read_only=True, slug_field="code")
    username = serializers.CharField(source="player.user.username", read_only=True)

    class Meta:
        model = SkribblePlayer
        fields = [
            "room",
            "username",
            "order",
            "score",
            "found",
        ]
        read_only_fields = fields


class SkribbleRoomSerializer(serializers.ModelSerializer):
    players = PlayerSerializer(many=True, read_only=True)

    class Meta:
        model = SkribbleRoom
        fields = [
            "code",
            "name",
            "players",
            "current_player_index",
            "round_counter",
            "round_started",
            "timer",
            "timer_end",
            "created_at",
        ]
        read_only_fields = [
            "code",
            "players",
            "current_player_index",
            "round_counter",
            "round_started",
            "timer",
            "timer_end",
            "created_at",
        ]


# /users/
class UserSerializer(serializers.HyperlinkedModelSerializer):
    profile_image = serializers.SerializerMethodField()
    available_routes = serializers.SerializerMethodField()
    skribble = SkribbleRoomSerializer(
        read_only=True, source="userprofile.skribbleplayer.room"
    )

    class Meta:
        model = User
        fields = [
            "url",
            "username",
            "email",
            "is_staff",
            "profile_image",
            "available_routes",
            "skribble",
        ]
        extra_kwargs = {"url": {"view_name": "user-detail", "lookup_field": "username"}}

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

    def get_available_routes(self, obj):
        request = self.context.get("request")
        username = obj.username
        if not request:
            return None
        return {
            "tplace": request.build_absolute_uri(f"/api/users/{username}/tplace/"),
            "nyancoins": request.build_absolute_uri(
                f"/api/users/{username}/nyancoins/"
            ),
            "colors": request.build_absolute_uri(f"/api/users/{username}/colors/"),
            "pixels": request.build_absolute_uri(f"/api/users/{username}/pixels/"),
            "max-pixels": request.build_absolute_uri(
                f"/api/users/{username}/max-pixels/"
            ),
            "avatar": request.build_absolute_uri(f"/api/users/{username}/avatar/"),
        }


class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Color
        fields = ["name", "hex_code"]
        read_only_fields = fields


# /users/{username}/
class TplaceSerializer(serializers.ModelSerializer):
    unlocked_colors = ColorSerializer(many=True, read_only=True)
    unlocked_wordlists = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = UserProfile
        fields = [
            "nyancoins",
            "placable_pixels",
            "max_placable_pixels",
            "regeneration_delay",
            "next_regeneration",
            "unlocked_colors",
            "unlocked_wordlists",
        ]
        read_only_fields = fields


class NyancoinsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ["nyancoins"]
        read_only_fields = fields


class UnlockedColorsSerializer(serializers.ModelSerializer):
    unlocked_colors = ColorSerializer(many=True, read_only=True)

    class Meta:
        model = UserProfile
        fields = ["unlocked_colors"]
        read_only_fields = fields


class PixelsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = [
            "placable_pixels",
            "max_placable_pixels",
            "regeneration_delay",
            "next_regeneration",
        ]
        read_only_fields = fields


class MaxPixelsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ["max_placable_pixels"]
        read_only_fields = fields


class AvatarSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ["profile_image"]


class LoginRequestSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


class SignupRequestSerializer(serializers.Serializer):
    username = serializers.CharField(validators=[UnicodeUsernameValidator()])
    email = serializers.EmailField()
    password1 = serializers.CharField()
    password2 = serializers.CharField()

    def validate(self, attrs):
        if attrs["password1"] != attrs["password2"]:
            raise ValidationError("Passwords do not match")
        validate_password(attrs["password1"])
        return attrs


class PixelPlaceSerializer(serializers.Serializer):
    x_pos = serializers.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(settings.TPLACE_MAX_X - 1)]
    )
    y_pos = serializers.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(settings.TPLACE_MAX_Y - 1)]
    )
    color = serializers.SlugRelatedField(
        slug_field="name", queryset=Color.objects.all()
    )


class PixelSerializer(serializers.ModelSerializer):
    color = ColorSerializer()

    class Meta:
        model = Pixel
        fields = ["x_pos", "y_pos", "color", "user", "updated_at"]


class WordListSerializer(serializers.HyperlinkedModelSerializer):
    words = StringRelatedField(many=True)

    class Meta:
        model = WordList
        fields = ["words", "name"]
