from django.db import models
from django.contrib.auth.models import User



class UserProfile(models.Model):
	role_choice = (('Lecturer', 'Lecturer'),('Student', 'Student'))
	role = models.CharField(max_length=100,choices=role_choice,default='Student')
	user = models.OneToOneField(User,null=True,on_delete=models.CASCADE)
	bio = models.TextField(null=True,blank=True)
	profile_pic = models.ImageField(null=True,blank=True,default='profile pic.jpg',upload_to='profiles/')
	website_url = models.URLField(max_length=150,blank=True,null=True)
	facebook_url = models.URLField(max_length=150,blank=True,null=True)
	twitter_url = models.URLField(max_length=150,blank=True,null=True)
	github_url = models.URLField(max_length=150,blank=True,null=True)
	instagram_url = models.URLField(max_length=150,blank=True,null=True)
	youtube_url = models.URLField(max_length=150,blank=True,null=True)

# default='studydoorway_logo.png'
	def __str__(self):
		return str(self.user)


