from django.urls import path
from main.views import ProfileList, ProfileDetails, ProfileEdit, ProfileChangePassword,\
    ProfileFollowUnfollow, ProfileIsFollowed, MessageList, ProfileChangeImage, ChatList,\
    ProfileFollowers, ProfileFollowings, PostList, PostCreate, PostLikeUnlike, PostComment, CommentLikeUnlike


urlpatterns = [
    path('profiles/', ProfileList.as_view()),
    path('profile/<int:pk>/', ProfileDetails.as_view()),
    path('profile_edit/', ProfileEdit.as_view()),
    path('profile_change_password/', ProfileChangePassword.as_view()),
    path('profile_change_image/', ProfileChangeImage.as_view()),

    path('profile_follow_unfollow/<int:pk>/', ProfileFollowUnfollow.as_view()),
    path('profile_is_followed/<int:pk>/', ProfileIsFollowed.as_view()),
    path('profile_followers/<int:pk>/', ProfileFollowers.as_view()),
    path('profile_followings/<int:pk>/', ProfileFollowings.as_view()),

    path('messages/<int:pk>/', MessageList.as_view()),
    path('chats/', ChatList.as_view()),

    path('post/<int:pk>/', PostList.as_view()),
    path('post/', PostCreate.as_view()),
    path('post_like_unlike/<int:pk>/', PostLikeUnlike.as_view()),

    path('post_comment/<int:pk>/', PostComment.as_view()),
    path('comment_like_unlike/<int:pk>/', CommentLikeUnlike.as_view()),
]
