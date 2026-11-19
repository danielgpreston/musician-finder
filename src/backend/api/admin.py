from django.contrib import admin

# Register your models here.

from .models import Genre, Instrument, Profile

admin.site.register(Genre)
admin.site.register(Instrument)
admin.site.register(Profile)
