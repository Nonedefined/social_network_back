from main.models import Message, Profile, Chat
from rest_framework import serializers, exceptions


class MessageSerializer(serializers.HyperlinkedModelSerializer):
    image = serializers.ImageField(required=False)

    class Meta:
        model = Message
        fields = ['id', 'text', 'image']

    def validate(self, attrs):
        image = attrs.get('image')
        text = attrs.get('text')
        if not image and not text:
            raise exceptions.ValidationError({'field': ['Empty field']})

        return attrs

    def create(self, validated_data):
        def is_chat_exist(prof_from, prof_to):
            chats_1 = Chat.objects.filter(profile_1=prof_from, profile_2=prof_to)
            chats_2 = Chat.objects.filter(profile_1=prof_to, profile_2=prof_from)
            if chats_1.exists() or chats_2.exists():
                return True
            return False

        profile_from = Profile.objects.get(user=self.context['request'].user)
        profile_to = self.context['view'].get_object()
        if not profile_to:
            raise exceptions.ValidationError({"id": ['No such profile']})

        if not is_chat_exist(profile_from, profile_to):
            Chat.objects.create(profile_1=profile_from, profile_2=profile_to)

        chat = self.context['view'].get_chat(profile_from, profile_to)

        text = validated_data.get('text', '')
        image = validated_data.get('image', None)

        return Message.objects.create(
            chat=chat,
            profile_from=profile_from,
            text=text,
            image=image
        )


class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = ['id']

