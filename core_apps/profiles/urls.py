from django.urls import path
from .views import (
    ProfileDetailAPIView,
    ProfileListAPIView,
    UpdateProfileAPIView,
    FollowAPIView,
    FollowingListView,
    FollowerListView,
    UnfollowAPIView,
)

urlpatterns = [
    path("all/", ProfileListAPIView.as_view(), name="all-profile"),
    path("me/", ProfileDetailAPIView.as_view(), name="my-profile"),
    path("me/update/", UpdateProfileAPIView.as_view(), name="update-profile"),
    path("me/followers/", FollowerListView.as_view(),name="followers"),
    path("<uuid:user_id>/follow/", FollowAPIView.as_view(), name="follow"),
    path("<uuid:user_id>/unfollow/", UnfollowAPIView.as_view(), name="unfollow"),
    
]