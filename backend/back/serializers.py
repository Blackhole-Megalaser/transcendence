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


class NyancoinsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ["nyancoins"]


class ColorsSerializer(serializers.ModelSerializer):
    unlocked_colors = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = UserProfile
        fields = ["unlocked_colors"]


class PixelsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = [
            "placable_pixels",
            "max_placable_pixels",
            "regeneration_delay",
            "next_regeneration",
        ]


class MaxPixelsSerializer(serializers.ModelSerializer):
    unlocked_colors = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = UserProfile
        fields = ["max_placable_pixels"]
