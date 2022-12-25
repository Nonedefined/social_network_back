from django.contrib import admin

from main.models import Profile, Followers, Followings, Chat, Message, Post, Comment, LikePost, LikeComment


@admin.register(Profile)
class ProfileModel(admin.ModelAdmin):
    list_filter = ('user', )
    list_display = ('user', )


@admin.register(Followers)
class FollowerModel(admin.ModelAdmin):
    list_filter = ('profile', )
    list_display = ('profile', )


@admin.register(Followings)
class FollowingModel(admin.ModelAdmin):
    list_filter = ('profile', )
    list_display = ('profile', )


@admin.register(Message)
class MessageModel(admin.ModelAdmin):
    list_filter = ('chat', )
    list_display = ('chat', )


@admin.register(Chat)
class ChatModel(admin.ModelAdmin):
    list_filter = ('profile_1', 'profile_2')
    list_display = ('profile_1', 'profile_2')


@admin.register(Post)
class PostModel(admin.ModelAdmin):
    list_filter = ('profile', )
    list_display = ('profile', )


@admin.register(Comment)
class CommentModel(admin.ModelAdmin):
    list_filter = ('profile', )
    list_display = ('profile', )


@admin.register(LikePost)
class LikePostModel(admin.ModelAdmin):
    list_filter = ('post', )
    list_display = ('post', )


@admin.register(LikeComment)
class LikeCommentModel(admin.ModelAdmin):
    list_filter = ('comment', )
    list_display = ('comment', )



