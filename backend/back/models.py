import datetime
import logging
import os

from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.db import models
from django.db.models.deletion import CASCADE, RESTRICT
from django.utils import timezone

##########################################################
# WARNING: do not run `make dev` while editing this file #
##########################################################

logger = logging.getLogger(__name__)


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
    list = models.ForeignKey(WordList, on_delete=models.RESTRICT, related_name="words")

    def __str__(self):
        return self.word


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
    next_regeneration = models.DateTimeField(default=timezone.now)
    unlocked_colors = models.ManyToManyField(Color)
    unlocked_wordlists = models.ManyToManyField(WordList)
    # List of actual friends, who accepted the request
    friends = models.ManyToManyField("UserProfile", symmetrical=True)
    # Sent friend requests, not accepted nor rejected
    # self is the sender, foreign is the reciever who can accept or reject
    # on reject, simply remove from this list
    # on accept, move to friends
    pending_friend_requests = models.ManyToManyField("UserProfile")

    def save(self, *args, **kwargs):
        if self.pk:
            try:
                old = UserProfile.objects.get(pk=self.pk)
                if old.profile_image != self.profile_image:
                    old.profile_image.delete(save=False)
            except UserProfile.DoesNotExist:
                pass
        super().save(*args, **kwargs)

    def regenerate_pixels(self):
        """
        Regenerate the pixels for that user.
        Also saves that profile.
        """
        now = timezone.now()
        pixels_to_regenerate = 0
        while now > self.next_regeneration:
            pixels_to_regenerate += 1
            self.next_regeneration = self.next_regeneration + self.regeneration_delay
        self.placable_pixels = min(
            self.placable_pixels + pixels_to_regenerate, self.max_placable_pixels
        )
        self.save()


class Pixel(models.Model):
    x_pos = models.IntegerField(validators=[MinValueValidator(0)])
    y_pos = models.IntegerField(validators=[MinValueValidator(0)])
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    color = models.ForeignKey(Color, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["x_pos", "y_pos"], name="pixel_uniq_pos")
        ]


class SkribbleRoom(models.Model):
    # random 5 letter room code
    code = models.TextField(max_length=5)
    # pretty name to show in room selector
    name = models.TextField(max_length=255, unique=True)
    current_word = models.ForeignKey(
        Word, on_delete=RESTRICT, related_name="rooms_with_current_word"
    )
    wordlist = models.ForeignKey(WordList, on_delete=RESTRICT)
    current_player_index = models.IntegerField(default=0)
    round_counter = models.IntegerField(default=0)
    round_started = models.BooleanField(default=False)

    word_history = models.ManyToManyField(
        Word,
        through="SkribbleRoomWord",
        related_name="rooms_with_word_in_history",
    )

    timer = models.DurationField(default=timezone.timedelta(minutes=1))
    timer_end = models.DurationField(default=timezone.now)

    created_at = models.DurationField(default=timezone.now)


class SkribbleRoomWord(models.Model):
    room = models.ForeignKey(SkribbleRoom, on_delete=CASCADE)
    word = models.ForeignKey(Word, on_delete=CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["room", "word"], name="unique_room_word_history"
            ),
        ]


class SkribblePlayer(models.Model):
    """
    A player in a round of Skribble
    """

    room = models.ForeignKey(SkribbleRoom, on_delete=CASCADE)
    player = models.OneToOneField(UserProfile, on_delete=models.RESTRICT)
    # order in which the player will play
    order = models.IntegerField(validators=[MinValueValidator(0)])
    score = models.IntegerField(validators=[MinValueValidator(0)])

    # true if the player has found the word
    found = models.BooleanField(default=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["room", "order"], name="skribble_player_unique_order_per_room"
            )
        ]
