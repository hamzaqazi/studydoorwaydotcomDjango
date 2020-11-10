from django.db.models.signals import post_save
from django.contrib.auth.models import User
from .models import *


# def create_class_info(sender, instance, created, **kwargs):
# 	if created:
# 		ClassInfo.objects.create(class_room=instance)
# 		print("ClassInfo created")

# post_save.connect(create_class_info,sender=ClassRoom)		