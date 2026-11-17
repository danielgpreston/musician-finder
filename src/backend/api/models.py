from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Genre(models.Model):
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Instrument(models.Model):
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Profile(models.Model):
    EXPERIENCE_LEVELS = [
        ("beginner", "Beginner"),
        ("intermediate", "Intermediate"),
        ("advanced", "Advanced"),
        ("professional", "Professional"),
    ]

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile"
    )
    display_name = models.CharField(max_length=100, blank=True)
    bio = models.TextField(max_length=500, blank=True)
    age = models.PositiveSmallIntegerField(
        null=True, blank=True, validators=[MinValueValidator(13), MaxValueValidator(120)]
    )
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=50, blank=True)
    experience_level = models.CharField(
        max_length=20, choices=EXPERIENCE_LEVELS, default="beginner"
    )
    instruments = models.ManyToManyField(Instrument, blank=True, related_name="players")
    genres = models.ManyToManyField(Genre, blank=True, related_name="musicians")
    looking_for = models.ManyToManyField(Instrument, blank=True, related_name="wanted_by")
    instagram = models.URLField(blank=True)
    youtube = models.URLField(blank=True)
    website = models.URLField(blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Profile of {self.user.get_username()}"
