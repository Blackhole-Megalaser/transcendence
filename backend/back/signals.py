from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import UserProfile, Color


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    profile, profile_created = UserProfile.objects.get_or_create(user=instance)
    if created or profile_created:
        free_colors = Color.objects.filter(cost=0)
        profile.unlocked_colors.set(free_colors)
    profile.save()
