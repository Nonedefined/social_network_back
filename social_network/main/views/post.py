from main.serializers import PostSerializer, PostLikeUnlikeSerializer, \
    PostCommentSerializer, CommentLikeUnlikeSerializer
from rest_framework import generics, exceptions, views
from rest_framework.permissions import IsAuthenticated
from main.models import Post, Profile, Comment, LikePost, LikeComment
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from social_network.settings import TIME_ZONE_DIFFERENCE
from datetime import timedelta


class PostList(views.APIView):
    queryset = Profile.objects.all()
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(pk=self.kwargs['pk'])

    def get_object(self):
        return Profile.objects.filter(user=self.request.user).first()

    @staticmethod
    def format_time(time):
        created_at = time + timedelta(hours=TIME_ZONE_DIFFERENCE)
        return '%02d' % created_at.month + '.%02d' % created_at.day + ' %02d' % created_at.hour + ':%02d' % created_at.minute

    def get(self, request, *args, **kwargs):
        profile = self.get_queryset()
        my_profile = self.get_object()
        if not profile.exists():
            raise exceptions.ValidationError({'id': ['No such profile']})

        posts = Post.objects.filter(profile=profile.first()).order_by('-id')
        posts_response = []
        for post in posts:
            comments = Comment.objects.filter(post=post)
            comments_response = []
            for comment in comments:
                profile_image = None
                if comment.profile.image:
                    profile_image = comment.profile.image.url

                comment_profile_id = comment.profile.pk
                comment_profile_image = profile_image
                comment_profile_first_name = comment.profile.user.first_name
                comment_profile_last_name = comment.profile.user.last_name

                comment_likes = LikeComment.objects.filter(comment=comment).first()
                comment_likes_amount = comment_likes.comment_like_amount
                comment_is_liked = bool(comment_likes.comment_like.filter(user=my_profile.user))

                image = None
                if comment.image:
                    image = comment.image.url

                created_at = self.format_time(comment.created_at)
                comments_response.append({
                    'id': comment.id,
                    'comment_profile_id': comment_profile_id,
                    'comment_profile_image': comment_profile_image,
                    'comment_profile_first_name': comment_profile_first_name,
                    'comment_profile_last_name': comment_profile_last_name,
                    'comment_likes_amount': comment_likes_amount,
                    'comment_is_liked': comment_is_liked,
                    'text': comment.text,
                    'image': image,
                    'created_at': created_at,
                })

            image = None
            if post.image:
                image = post.image.url

            created_at = self.format_time(post.created_at)
            likes = LikePost.objects.filter(post=post).first()
            likes_amount = likes.post_like_amount

            is_liked = bool(likes.post_like.filter(user=my_profile.user))

            posts_response.append({
                'id': post.pk,
                'text': post.text,
                'image': image,
                'comments': comments_response,
                'likes_amount': likes_amount,
                'created_at': created_at,
                'is_liked': is_liked,
            })

        return Response([{'Posts': posts_response}])


class PostCreate(generics.CreateAPIView):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)

    def get_object(self):
        return Profile.objects.filter(user=self.request.user).first()


class PostLikeUnlike(generics.UpdateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostLikeUnlikeSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return Profile.objects.filter(user=self.request.user).first()

    def get_queryset(self):
        return self.queryset.filter(pk=self.kwargs['pk']).first()


class PostComment(generics.CreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostCommentSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)

    def get_object(self):
        return self.queryset.filter(pk=self.kwargs['pk']).first()


class CommentLikeUnlike(generics.UpdateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentLikeUnlikeSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return Profile.objects.filter(user=self.request.user).first()

    def get_queryset(self):
        return self.queryset.filter(pk=self.kwargs['pk']).first()

