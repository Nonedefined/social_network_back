from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(null=True, blank=True, upload_to='%Y/%m/%d/')
    bio = models.TextField(max_length=300, blank=True)
    location = models.CharField(max_length=30, blank=True)

    def __str__(self):
        return self.user.username


class Followers(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
    profile_followers = models.ManyToManyField(Profile, related_name='profile_followers', blank=True)

    @property
    def followers_amount(self):
        return self.profile_followers.all().count()

    def __str__(self):
        return self.profile.user.username


class Followings(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
    profile_following = models.ManyToManyField(Profile, related_name='profile_following', blank=True)

    @property
    def followings_amount(self):
        return self.profile_following.all().count()

    def __str__(self):
        return self.profile.user.username


class Chat(models.Model):
    profile_1 = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='profile_1')
    profile_2 = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='profile_2')

    def __str__(self):
        return f'{self.profile_1.user.username} {self.profile_2.user.username}'


class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='chat')
    profile_from = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='profile_from')
    text = models.TextField(blank=True)
    image = models.ImageField(null=True, blank=True, upload_to='%Y/%m/%d/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.chat} {self.profile_from.user.username}'


class Post(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='profile')
    text = models.TextField(blank=True)
    image = models.ImageField(null=True, blank=True, upload_to='%Y/%m/%d/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.profile.user.username


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post')
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    text = models.TextField(blank=True)
    image = models.ImageField(null=True, blank=True, upload_to='%Y/%m/%d/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.post} {self.profile.user.username}'


class LikePost(models.Model):
    post = models.OneToOneField(Post, on_delete=models.CASCADE)
    post_like = models.ManyToManyField(Profile, related_name='post_like', blank=True)

    @property
    def post_like_amount(self):
        return self.post_like.all().count()

    def __str__(self):
        return self.post.profile.user.username


class LikeComment(models.Model):
    comment = models.OneToOneField(Comment, on_delete=models.CASCADE)
    comment_like = models.ManyToManyField(Profile, related_name='comment_like', blank=True)

    @property
    def comment_like_amount(self):
        return self.comment_like.all().count()

    def __str__(self):
        return self.comment.profile.user.username
