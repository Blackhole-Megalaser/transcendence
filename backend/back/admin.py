# Register your models here.
from django.contrib import admin

from .models import Color, Pixel, UserProfile, Word, WordList

admin.site.register(UserProfile)
admin.site.register(Word)
admin.site.register(WordList)
admin.site.register(Color)
admin.site.register(Pixel)
