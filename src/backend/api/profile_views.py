from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Genre, Instrument, Profile
from .serializers import ProfileSerializer


@api_view(["GET", "PATCH"])
@permission_classes([IsAuthenticated])
def my_profile_view(request):
    profile, _ = Profile.objects.get_or_create(user=request.user)
    if request.method == "PATCH":
        serializer = ProfileSerializer(profile, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    return Response(ProfileSerializer(profile).data)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def profile_detail_view(request, user_id):
    profile = Profile.objects.filter(user_id=user_id, is_active=True).first()
    if profile is None:
        return Response({"error": "Profile not found."}, status=status.HTTP_404_NOT_FOUND)
    return Response(ProfileSerializer(profile).data)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def options_view(request):
    return Response(
        {
            "instruments": list(Instrument.objects.values_list("name", flat=True)),
            "genres": list(Genre.objects.values_list("name", flat=True)),
            "experience_levels": [value for value, _ in Profile.EXPERIENCE_LEVELS],
        }
    )
