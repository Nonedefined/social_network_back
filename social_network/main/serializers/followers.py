from rest_framework import serializers, exceptions
from main.models import Profile, Followers, Followings


class ProfileFollowUnfollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['id']

    def update(self, instance, validated_data):
        user_to_follow = self.context['view'].get_queryset().first()
        if not user_to_follow:
            raise exceptions.ValidationError({'id': ['No such profile']})

        if instance == user_to_follow:
            raise exceptions.ValidationError({'id': ['You can not follow yourself']})

        followings, _ = Followings.objects.get_or_create(profile=instance)
        followers, _ = Followers.objects.get_or_create(profile=user_to_follow)

        if followings.profile_following.filter(pk=user_to_follow.pk).exists():
            followings.profile_following.remove(user_to_follow)
            followers.profile_followers.remove(instance)
        else:
            followings.profile_following.add(user_to_follow)
            followers.profile_followers.add(instance)

        return {'status': 200}

