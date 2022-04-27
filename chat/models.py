from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Chat(models.Model): 

    chat_id = models.IntegerField(primary_key=True)
    author_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chat')
    title = models.TextField(blank=False, null=False, default='Title')
    feed = models.TextField(blank=False, null=False, default='Feed')
    time = models.TimeField(blank=True, auto_now_add=True)
    date = models.DateField(blank=True)
    feed_type = models.CharField(max_length=1, 
                choices=(('p', 'positive'), ('n', 'negative')),
                blank=False, default=None)
    tags =  models.JSONField(default={})
    upvotes = models.ManyToManyField(User, related_name='chat1', default=None)
    downvotes = models.ManyToManyField(User, related_name='chat2', default=None)

    # @property
    # def downvotesCount(self):
    #     return self.downvotesCount.all().count()

    # @property
    # def upvotesCount(self):
    #     return self.upvotesCount.all().count()
    