from main.serializers import ProfileFollowUnfollowSerializer
from rest_framework import views
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from main.models import Profile, Followers, Followings
from rest_framework import exceptions
from rest_framework.response import Response


class ProfileFollowUnfollow(generics.UpdateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileFollowUnfollowSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.queryset.get(user=self.request.user)

    def get_queryset(self):
        return self.queryset.filter(pk=self.kwargs['pk'])


class ProfileIsFollowed(views.APIView):
    queryset = Profile.objects.all()
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.queryset.get(user=self.request.user)

    def get_queryset(self):
        return self.queryset.filter(pk=self.kwargs['pk']).first()

    def get(self, request, *args, **kwargs):
        my_profile = self.get_object()
        profile_follow = self.get_queryset()
        if not profile_follow:
            raise exceptions.ValidationError({'id': ['No such profile']})

        followers = Followers.objects.get(profile=profile_follow)
        is_followed = bool(followers.profile_followers.filter(user=my_profile.user))
        return Response([{'is_followed': is_followed}])


def get_profile_response(profiles):
    response = []
    for profile in profiles:
        followers = Followers.objects.filter(profile=profile)
        followers_amount = followers.first().followers_amount
        image = None
        if profile.image:
            image = profile.image.url
        response.append({
            'id': profile.id,
            'user_first_name': profile.user.first_name,
            'user_last_name': profile.user.last_name,
            'followers_amount': followers_amount,
            'image': image
        })
    return response


class ProfileFollowers(views.APIView):
    queryset = Profile.objects.all()
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(pk=self.kwargs['pk']).first()

    def get(self, request, *args, **kwargs):
        profile = self.get_queryset()
        if not profile:
            raise exceptions.ValidationError({'id': ['No such profile']})

        profile_followers = Followers.objects.filter(profile=profile).first()
        response = get_profile_response(profile_followers.profile_followers.all())
        return Response([response])


class ProfileFollowings(views.APIView):
    queryset = Profile.objects.all()
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(pk=self.kwargs['pk']).first()

    def get(self, request, *args, **kwargs):
        profile = self.get_queryset()
        if not profile:
            raise exceptions.ValidationError({'id': ['No such profile']})

        profile_followings = Followings.objects.filter(profile=profile).first()
        response = get_profile_response(profile_followings.profile_following.all())
        return Response([response])

