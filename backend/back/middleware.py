from datetime import timedelta

from django.utils import timezone

from .models import UserProfile


class UpdateLastSeenMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        user = getattr(request, "user", None)
        if user and user.is_authenticated:
            now = timezone.now()
            profile = UserProfile.objects.filter(user=user).only("last_seen").first()

            if profile and (
                profile.last_seen is None
                or (now - profile.last_seen) > timedelta(minutes=3)
            ):
                UserProfile.objects.filter(pk=profile.pk).update(last_seen=now)

        return response
