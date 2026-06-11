from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.contrib.auth.models import User
from rest_framework import serializers

from .models import UserProfile


# /users/
class UserSerializer(serializers.HyperlinkedModelSerializer):
    profile_image = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ["url", "username", "email", "is_staff", "profile_image"]
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


# /users/{username}/
class TplaceSerializer(serializers.ModelSerializer):
    unlocked_colors = serializers.StringRelatedField(many=True, read_only=True)
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


class ColorsSerializer(serializers.ModelSerializer):
    unlocked_colors = serializers.StringRelatedField(many=True, read_only=True)

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
