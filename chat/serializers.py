from rest_framework import serializers

from chat.models import Chat

class PostFeedSerializer(serializers.ModelSerializer):

    class Meta:
        model = Chat
        fields = ('author_id', 'title', 'feed', 'feed_type', 'tags')

class GetChatSerializer(serializers.ModelSerializer): 
    downvotesCount = serializers.SerializerMethodField("get_downvotes_count")#source="downvotesCount")
    upvotesCount = serializers.SerializerMethodField("get_upvotes_count")#source="upvotesCount")

    class Meta:
        model = Chat
        fields = ('author_id', 'chat_id', 'title', 'feed', 'feed_type', 'tags', 'date', 'time', "downvotesCount", "upvotesCount")

    def get_downvotes_count(self, chat_object):
        return chat_object.downvotes.all().count()

    def get_upvotes_count(self, chat_object):
        return chat_object.upvotes.all().count()