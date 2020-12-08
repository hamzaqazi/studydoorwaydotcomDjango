from django.db.models.signals import post_save
from django.contrib.auth.models import User
from .models import *



def create_instructor(sender, instance, created, **kwargs):
	if created:
		classroom = ClassRoom.objects.get(id=instance.id)
		instructor = Instructor(instructor=instance.user,class_room=classroom)
		instructor.save()
		print("Instructor created")


post_save.connect(create_instructor,sender=ClassRoom)