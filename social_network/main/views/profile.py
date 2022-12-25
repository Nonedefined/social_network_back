from main.serializers import ProfileSerializer, ProfileEditSerializer, ProfileChangePasswordSerializer, ProfileFollowUnfollowSerializer, ProfileChangeImageSerializer
from rest_framework import generics
from rest_framework import exceptions
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from main.models import Profile, Followers, Followings
import random


def get_profile_data(profile):
    user_date_joined = profile.user.date_joined

    followings = Followings.objects.filter(profile=profile)
    followers = Followers.objects.filter(profile=profile)

    followings_amount = followings.first().followings_amount
    followers_amount = followers.first().followers_amount

    image = None
    if profile.image:
        image = profile.image.url

    return {
        'id': profile.id,
        'bio': profile.bio,
        'location': profile.location,
        'user_first_name': profile.user.first_name,
        'user_last_name': profile.user.last_name,
        'user_date_joined': user_date_joined.date(),
        'followings_amount': followings_amount,
        'followers_amount': followers_amount,
        'image': image
    }


class ProfileList(generics.ListCreateAPIView, generics.ListAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        response_data = []
        for profile in self.queryset.all():
            profile_data = get_profile_data(profile)
            response_data.append(profile_data)
        random.shuffle(response_data)
        return Response([response_data])


class ProfileDetails(generics.ListAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

    permission_classes = [AllowAny]

    def get_queryset(self):
        return self.queryset.filter(pk=self.kwargs['pk'])

    def get(self, request, *args, **kwargs):
        profile = self.get_queryset()
        if not profile.exists():
            raise exceptions.ValidationError({'id': ['No such profile']})

        data = get_profile_data(profile.first())
        return Response([data])


class ProfileEdit(generics.ListAPIView, generics.RetrieveUpdateDestroyAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileEditSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.queryset.get(user=self.request.user)

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def get(self, request, *args, **kwargs):
        profile = self.get_queryset().first()
        data = get_profile_data(profile)
        return Response([data])


class ProfileChangePassword(generics.UpdateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileChangePasswordSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.queryset.get(user=self.request.user)


class ProfileChangeImage(generics.UpdateAPIView, generics.DestroyAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileChangeImageSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)

    def get_object(self):
        return self.queryset.get(user=self.request.user)

    def destroy(self, request, *args, **kwargs):
        profile = self.get_object()
        profile.image = None
        profile.save()
        data = get_profile_data(profile)
        return Response([data])

