from django.contrib.auth.models import User
from django.db import models
from django.core.validators import MinValueValidator

import datetime
import os


class Color(models.Model):
    name = models.TextField()
    hex_code = models.TextField()
    cost = models.IntegerField(validators=[MinValueValidator(0)], default=0)

    def __str__(self):
        return self.hex_code


class WordList(models.Model):
    name = models.TextField(max_length=255)


class Word(models.Model):
    word = models.TextField(max_length=255)
    list = models.ForeignKey(WordList, on_delete=models.RESTRICT)


def get_image_path(instance, filename):
    path = os.path.join("profile_images/", str(instance.user.username))
    return path


class UserProfile(models.Model):
    class Meta:
        constraints = [
            models.CheckConstraint(
                condition=models.Q(
                    placable_pixels__lte=models.F("max_placable_pixels")
                ),
                name="placable_lte_max_placable_pixels",
            )
        ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_image = models.ImageField(
        max_length=255,
        upload_to=get_image_path,
        # upload_to="profile_images/",
        blank=True,
        null=True,
    )
    nyancoins = models.IntegerField(validators=[MinValueValidator(0)], default=20)
    placable_pixels = models.IntegerField(validators=[MinValueValidator(0)], default=10)
    max_placable_pixels = models.IntegerField(
        validators=[MinValueValidator(0)], default=10
    )
    regeneration_delay = models.DurationField(default=datetime.timedelta(minutes=1))
    next_regeneration = models.DateTimeField(default=datetime.datetime.now)
    unlocked_colors = models.ManyToManyField(Color)
    unlocked_wordlists = models.ManyToManyField(WordList)

    def save(self, *args, **kwargs):
        if self.pk:
            try:
                old = UserProfile.objects.get(pk=self.pk)
                if old.profile_image != self.profile_image:
                    old.profile_image.delete(save=False)
            except UserProfile.DoesNotExist:
                pass
        super().save(*args, **kwargs)


class Pixel(models.Model):
    x_pos = models.IntegerField(validators=[MinValueValidator(0)])
    y_pos = models.IntegerField(validators=[MinValueValidator(0)])
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    color = models.ForeignKey(Color, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
