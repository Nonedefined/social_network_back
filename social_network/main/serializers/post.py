from main.models import Post, Profile, LikePost, Comment, LikeComment
from rest_framework import serializers, exceptions


class PostSerializer(serializers.HyperlinkedModelSerializer):
    image = serializers.ImageField(required=False)

    class Meta:
        model = Post
        fields = ['id', 'text', 'image']

    def validate(self, attrs):
        image = attrs.get('image')
        text = attrs.get('text')
        if not image and not text:
            raise exceptions.ValidationError({'field': ['Empty field']})

        return attrs

    def create(self, validated_data):
        text = validated_data.get('text', '')
        image = validated_data.get('image', None)
        profile = self.context['view'].get_object()
        post = Post.objects.create(
            profile=profile,
            text=text,
            image=image
        )
        LikePost.objects.create(post=post)
        return post


class PostLikeUnlikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id']

    def update(self, instance, validated_data):
        post = self.context['view'].get_queryset()
        if not post:
            raise exceptions.ValidationError({'id': ['No such post']})

        post_like, _ = LikePost.objects.get_or_create(post=post)
        if post_like.post_like.filter(pk=instance.pk).exists():
            post_like.post_like.remove(instance)
        else:
            post_like.post_like.add(instance)

        return {'status': 200}


class PostCommentSerializer(serializers.HyperlinkedModelSerializer):
    image = serializers.ImageField(required=False)

    class Meta:
        model = Post
        fields = ['id', 'text', 'image']

    def validate(self, attrs):
        image = attrs.get('image')
        text = attrs.get('text')
        if not image and not text:
            raise exceptions.ValidationError({'field': ['Empty field']})
        return attrs

    def create(self, validated_data):
        profile = Profile.objects.get(user=self.context['request'].user)
        post = self.context['view'].get_object()
        if not post:
            raise exceptions.ValidationError({"id": ['No such post']})

        text = validated_data.get('text', '')
        image = validated_data.get('image', None)

        comment = Comment.objects.create(
            post=post,
            profile=profile,
            text=text,
            image=image
        )
        LikeComment.objects.create(comment=comment)
        return comment


class CommentLikeUnlikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id']

    def update(self, instance, validated_data):
        comment = self.context['view'].get_queryset()
        if not comment:
            raise exceptions.ValidationError({'id': ['No such comment']})

        comment_like, _ = LikeComment.objects.get_or_create(comment=comment)
        if comment_like.comment_like.filter(pk=instance.pk).exists():
            comment_like.comment_like.remove(instance)
        else:
            comment_like.comment_like.add(instance)

        return {'status': 200}
