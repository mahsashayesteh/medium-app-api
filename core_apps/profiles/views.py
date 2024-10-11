#TODO:change this in production
from author_api.settings.local import DEFAULT_FROM_EMAIL
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from rest_framework.exceptions import NotFound
from .models import Profile
from .pagination import ProfilePagination
from .renderers import ProfileJSONRenderer, ProfilesJSONRenderer
from .serializers import ProfileSerializers, UpdateProfileSerializer, FollowingSerializer
from .exception import CantFollowYourself

user = get_user_model()

class ProfileListAPIView(generics.ListAPIView):
    serializer_class = ProfileSerializers
    permission_classes = [IsAuthenticated]
    queryset = Profile.objects.all()
    renderer_classes = (ProfilesJSONRenderer,)
    pagination_class = ProfilePagination

class ProfileDetailAPIView(generics.RetrieveAPIView):
    Permission_classes = [IsAuthenticated]
    serializer_class = ProfileSerializers
    renderer_classes = [ProfileJSONRenderer]
    
    queryset = Profile.objects.select_related("user")
        
    def get_object(self):
        user = self.request.user
        profile = self.queryset.get(user=user)
        return profile

class UpdateProfileAPIView(APIView):
    permission_classes = [IsAuthenticated]
    queryset = Profile.objects.select_related("user")
    renderer_classes = [ProfileJSONRenderer]
    serializer_class = UpdateProfileSerializer
    
    def get_object(self):
        profile = self.request.user.profile
        return profile
    
    def patch(self, request, *args, **kwargs):
        
        data = request.data
        serializer = UpdateProfileSerializer(
            instance=request.user.profile, data=data, partial=True
        )
        print(data)
        print(request.user.profile)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

class FollowerListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        try:
            profile = Profile.objects.get(user__id=request.user.id)
            followers_profile = profile.followers.all()
            print(type(followers_profile))
            print(followers_profile)
            print(followers_profile.count())
            print(followers_profile.count)
            serializer = FollowingSerializer(followers_profile, many=True)
            print(serializer)
            formatted_response = {
                "status_code":status.HTTP_200_OK,
                "follower_count": followers_profile.count(),
                "followers": serializer.data,
            }
            return Response(formatted_response, status=status.HTTP_200_OK)
        except Profile.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

class FollowingListView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, user_id, format=None):
        try:
            profile = Profile.object.get(user__id = user_id)
            following_Profile = profile.followers_list()
            user = [p.user for p in following_Profile]
            serializer = FollowingSerializer(user, many=True)
            formatted_response = {
                "status":status.HTTP_200_OK,
                "following_profile":following_Profile,
                "user_i_follow":serializer.data,
            }
            return Response(formatted_response, status=status.HTTP_200_OK)
        
        except Profile.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
class FollowAPIView(APIView):
    def post(self, request, user_id, fomat=None):
        try:
            profile = Profile.objects.get(user__id=user_id)
            follower = Profile.objects.get(user = request.user)
            user_profile = request.user.profile
            
            if profile == follower:
                raise CantFollowYourself
            
            if user_profile.check_following(profile):
                formatted_response = {
                    "status":status.HTTP_400_BAD_REQUEST,
                    "message": f"شما از قبل {profile.user.first_name} فالو دارید"
                }
                return Response(formatted_response, status=status.HTTP_400_BAD_REQUEST)
            user_profile.follow(profile)
            subject = "A new user follows you"
            message = f"Hi there {profile.user.first_name}!!, the user {user_profile.user.email} now follows you"
            from_email = DEFAULT_FROM_EMAIL
            recipient_list = [profile.user.email]
            send_mail(subject, message, from_email, recipient_list, fail_silently=True)
            formatted_response = {
                    "status":status.HTTP_200_OK,
                    "message": f"you follow {profile.user.first_name} "
                }
            return Response(formatted_response, status=status.HTTP_200_OK)

        except Profile.DoesNotExist:
            raise NotFound(f"شما نمی توانید پروفایلی که وجود ندارد را دنبال کنید")  
        
class UnfollowAPIView(APIView):
    
    def post(self, request, user_id, format=None):
        try:
            profile = Profile.objects.get(user__id=user_id)
            user_profile = request.user.profile
            
            if not Profile.objects.filter(user=request.user, followers = profile):
                formatted_response = {
                    "status":status.HTTP_400_BAD_REQUEST,
                    "message":f"شما تا زمانی که {profile.user.first_name} {profile.user.last_name} فالو نکرده باشید نمی توانید آنفالو کنید"

                }
                return Response(formatted_response, status=status.HTTP_400_BAD_REQUEST)
            user_profile.unfollow(profile)
            formatted_response = {
                "status":status.HTTP_200_OK,
                "message": f"شما {profile.user.first_name} {profile.user.last_name} را دیگر آنفالو کردید"
            }
            return Response(formatted_response, status=status.HTTP_200_OK)
        except Profile.DoesNotExist:
            raise NotFound(f"پروفایلی که وجود ندارد را نمی توانید آنفالو کنید")

