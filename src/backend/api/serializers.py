from rest_framework import serializers

from .models import Genre, Instrument, Profile


class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username", read_only=True)
    instruments = serializers.SlugRelatedField(
        many=True, slug_field="name", queryset=Instrument.objects.all(), required=False
    )
    genres = serializers.SlugRelatedField(
        many=True, slug_field="name", queryset=Genre.objects.all(), required=False
    )
    looking_for = serializers.SlugRelatedField(
        many=True, slug_field="name", queryset=Instrument.objects.all(), required=False
    )

    class Meta:
        model = Profile
        fields = [
            "id", "username", "display_name", "bio", "age", "city", "state",
            "experience_level", "instruments", "genres", "looking_for",
            "instagram", "youtube", "website", "is_active",
        ]
        read_only_fields = ["id", "username"]
