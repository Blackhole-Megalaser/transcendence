# Register your models here.
from django.contrib import admin
from .models import UserProfile, Word, WordList, Color, Pixel

admin.site.register(UserProfile)
admin.site.register(Word)
admin.site.register(WordList)
admin.site.register(Color)
admin.site.register(Pixel)
