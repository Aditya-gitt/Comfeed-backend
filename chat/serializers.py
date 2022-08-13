from rest_framework import serializers

from chat.models import Chat

class PostFeedSerializer(serializers.ModelSerializer):

    class Meta:
        model = Chat
        fields = ('author_id', 'title', 'feed', 'feed_type', 'tags')

class GetChatSerializer(serializers.ModelSerializer): 
    downvotesCount = serializers.SerializerMethodField("get_downvotes_count")#source="downvotesCount")
    upvotesCount = serializers.SerializerMethodField("get_upvotes_count")#source="upvotesCount")
    username = serializers.SerializerMethodField("get_username")#source="username"
    vote = serializers.SerializerMethodField("get_vote")
    class Meta:
        model = Chat
        fields = ('vote', 'username', 'author_id', 'chat_id', 'title', 'feed', 'feed_type', 'tags', 'date', 'time', "downvotesCount", "upvotesCount")

    def get_downvotes_count(self, chat_object):
        return chat_object.downvotes.all().count()

    def get_upvotes_count(self, chat_object):
        return chat_object.upvotes.all().count()

    def get_username(self, chat_object): 
        return chat_object.author_id.username

    def get_vote(self, chat_object): 
        loggedin_user_id = self.context.get('id')

        if chat_object.downvotes.filter(id=loggedin_user_id).exists():
            return -1
        else :
            if chat_object.upvotes.filter(id=loggedin_user_id).exists():
                return 1
            else :
                return 0