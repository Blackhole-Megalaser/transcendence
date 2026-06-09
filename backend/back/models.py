from django.contrib.auth.models import User
from django.db import models
from django.core.validators import MinValueValidator

import datetime


class Color(models.Model):
    name = models.TextField()
    hex_code = models.TextField()
    cost = models.IntegerField(validators=[MinValueValidator(0)], default=0)


class WordList(models.Model):
    name = models.TextField(max_length=255)


class Word(models.Model):
    word = models.TextField(max_length=255)
    list = models.ForeignKey(WordList, on_delete=models.RESTRICT)


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
        upload_to="profile_images/",
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


class Pixel(models.Model):
    x_pos = models.IntegerField(validators=[MinValueValidator(0)])
    y_pos = models.IntegerField(validators=[MinValueValidator(0)])
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    color = models.ForeignKey(Color, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
