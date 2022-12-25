from django.contrib.auth.models import User
from rest_framework import serializers, exceptions
from main.models import Profile, Followers, Followings, Post, LikePost, Chat
import django.contrib.auth.password_validation as validators
from django.core.validators import validate_email
from rest_framework.authtoken.views import Token


class ProfileSerializer(serializers.ModelSerializer):
    user_email = serializers.CharField(source='user.username')
    user_password = serializers.CharField(source='user.password', write_only=True)
    user_first_name = serializers.CharField(source='user.first_name')
    user_last_name = serializers.CharField(source='user.last_name')

    class Meta:
        model = Profile
        fields = ['id', 'user_email', 'user_password', 'user_first_name', 'user_last_name', 'bio', 'location']

    def validate_user_email(self, value):
        validate_email(value)
        profiles = Profile.objects.filter(user__username=value)
        if profiles.exists():
            raise exceptions.ValidationError({"user_user_email": ['Already exist']})
        else:
            return value

    def validate_user_password(self, value):
        validators.validate_password(password=value)
        return value

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        token = Token.objects.create(user=instance.user)
        ret['token'] = str(token)

        return ret

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data['user'])
        bio = validated_data['bio']
        location = validated_data['location']

        profile = Profile.objects.create(
            user=user,
            bio=bio,
            location=location,
        )
        post = Post.objects.create(
            profile=profile,
            text="Hello I am new here"
        )
        LikePost.objects.create(post=post)

        Chat.objects.create(profile_1=profile, profile_2=profile)
        Followings.objects.create(profile=profile)
        Followers.objects.create(profile=profile)
        return profile


class ProfileEditSerializer(serializers.ModelSerializer):
    user_first_name = serializers.CharField(source='user.first_name', required=False)
    user_last_name = serializers.CharField(source='user.last_name', required=False)

    class Meta:
        model = Profile
        fields = ['id', 'user_first_name', 'user_last_name', 'bio', 'location']

    def validate_user_username(self, value):
        profiles = Profile.objects.filter(user__username=value)
        if profiles.exists() and profiles.first().pk != self.instance.pk:
            raise exceptions.ValidationError({"user_username": ['Already exist']})
        else:
            return value

    def update(self, instance, validated_data):
        user = validated_data.get('user', {})
        first_name = user.get('first_name', instance.user.first_name)
        last_name = user.get('last_name', instance.user.last_name)

        instance.user.first_name = first_name
        instance.user.last_name = last_name

        instance.bio = validated_data.get('bio', instance.bio)
        instance.location = validated_data.get('location', instance.location)

        instance.user.save()
        instance.save()
        return instance


class ProfileChangePasswordSerializer(serializers.ModelSerializer):
    old_password = serializers.CharField(source='user.password', write_only=True)
    new_password = serializers.CharField(write_only=True)

    class Meta:
        model = Profile
        fields = ['id', 'old_password', 'new_password']

    def validate(self, attrs):
        old_password = attrs.get('user')['password']
        new_password = attrs.get('new_password')
        user = self.instance.user

        if not user.check_password(old_password):
            raise exceptions.ValidationError({'password': ['Wrong old password']})

        if old_password == new_password:
            raise exceptions.ValidationError({'password': ['New password cannot match the old one']})
        validators.validate_password(password=new_password)
        return attrs

    def update(self, instance, validated_data):
        new_password = validated_data.get('new_password')

        instance.user.set_password(new_password)
        instance.user.save()
        return instance


class ProfileChangeImageSerializer(serializers.HyperlinkedModelSerializer):
    image = serializers.ImageField(required=True)

    class Meta:
        model = Profile
        fields = ['id', 'image']

    def update(self, instance, validated_data):
        image = validated_data.get('image', None)
        instance.image = image
        instance.save()
        return instance
