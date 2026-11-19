from django.urls import path

from .profile_views import my_profile_view, options_view, profile_detail_view

urlpatterns = [
    path("profiles/me/", my_profile_view),
    path("profiles/<int:user_id>/", profile_detail_view),
    path("options/", options_view),
]
