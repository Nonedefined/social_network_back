from main.serializers import MessageSerializer, ChatSerializer
from rest_framework import generics, exceptions
from rest_framework.permissions import IsAuthenticated
from main.models import Message, Profile, Chat
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from social_network.settings import TIME_ZONE_DIFFERENCE
from datetime import timedelta
from django.db.models import Q


class MessageList(generics.ListCreateAPIView, generics.ListAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)

    @staticmethod
    def get_chat(prof_from, prof_to):
        chats_1 = Chat.objects.filter(profile_1=prof_from, profile_2=prof_to)
        chats_2 = Chat.objects.filter(profile_1=prof_to, profile_2=prof_from)
        if chats_1.exists():
            return chats_1.first()
        elif chats_2.exists():
            return chats_2.first()

    def get_object(self):
        return Profile.objects.filter(pk=self.kwargs['pk']).first()

    def get(self, request, *args, **kwargs):
        profile_from = Profile.objects.get(user=self.request.user)
        profile_to = self.get_object()
        if not profile_to:
            raise exceptions.ValidationError({"id": ['No such profile']})

        chat = self.get_chat(profile_from, profile_to)
        if not chat:
            raise exceptions.ValidationError({"chat": ['No such chat']})

        messages = Message.objects.filter(chat=chat)
        messages_response = []
        for message in messages:
            image = None
            if message.image:
                image = message.image.url

            created_at = message.created_at + timedelta(hours=TIME_ZONE_DIFFERENCE)
            created_at = '%02d' % created_at.hour + ':%02d' % created_at.minute
            messages_response.append({
                'id': message.pk,
                'profile_from': message.profile_from.pk,
                'text': message.text,
                'image': image,
                'created_at': created_at
            })

        return Response([{'Messages': messages_response}])


class ChatList(generics.ListAPIView):
    queryset = Message.objects.all()
    serializer_class = ChatSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        profile = Profile.objects.get(user=self.request.user)
        chats = Chat.objects.filter(Q(profile_1=profile) | Q(profile_2=profile))
        users_id = {}
        for chat in chats:
            message_id = Message.objects.filter(chat=chat).last().pk

            if chat.profile_1 == profile:
                profile_id = chat.profile_2.id
            else:
                profile_id = chat.profile_1.id

            profile_chat = Profile.objects.get(pk=profile_id)
            image = None
            if profile_chat.image:
                image = profile_chat.image.url

            users_id[message_id] = {
                'id': profile_id,
                'image': image,
                'user_first_name': profile_chat.user.first_name,
                'user_last_name': profile_chat.user.last_name,
            }

        users_id = {k: v for k, v in sorted(users_id.items(), key=lambda item: item[0], reverse=True)}
        return Response([{'Chats': users_id.values()}])
