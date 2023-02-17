from django.urls import include, path

from .views import ProfileDetailView

urlpatterns = [
    path("", include("allauth.urls")),
    path("<str:username>/", ProfileDetailView.as_view(), name="profile"),
]
