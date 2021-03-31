from django.db import models
from django.contrib.auth.models import User
from django.conf import settings


   


class Message(models.Model):
	author = models.ForeignKey('auth.User', related_name='snippets', on_delete=models.CASCADE)
	content=models.CharField(max_length=100)
	timestamp=models.DateTimeField(auto_now_add=True)


	def __str__(self):
		return self.author.username
  

	# def last_10_messages(self):
	# 	return Message.objects.order_by('-timestamp').all()[:10]