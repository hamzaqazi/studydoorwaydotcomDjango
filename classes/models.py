from django.db import models
from django.contrib.auth.models import User


from .models import *


class ClassRoom(models.Model):
	SECTION = (
		('A','A'),
		('B','B'),
		('C','C'),
		('D','D'),
		)
	student_key = models.CharField(max_length=50)
	user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
	date_created = models.DateTimeField(auto_now_add=True, null=True)
	last_updated = models.DateTimeField(auto_now=True)
	class_name = models.CharField(max_length= 250)
	section = models.CharField(max_length= 200, null=True, choices=SECTION)
	subject = models.CharField(max_length= 250,null=True)
	title_image = models.ImageField(null=True,blank=True,default='profile pic.jpg',upload_to='classTitleImages/')

	def __str__(self):
		return self.class_name



class Student(models.Model):
	class_room = models.ForeignKey(ClassRoom,null=True,on_delete=models.SET_NULL)
	student = models.ForeignKey(User,null=False,on_delete=models.CASCADE)
	added_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.student.first_name


class Instructor(models.Model):
	class_room = models.ForeignKey(ClassRoom,null=True,on_delete=models.SET_NULL)
	instructor = models.ForeignKey(User,null=False,on_delete=models.CASCADE)
	added_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.instructor.first_name


class Assignment(models.Model):
	POINTS = (
		('10','10'),
		('20','20'),
		('30','30'),
		('40','40'),
		('50','50'),
		('60','60'),
		('70','70'),
		('80','80'),
		('90','90'),
		('100','100'),
		)
	class_room = models.ForeignKey(ClassRoom,null=True, on_delete=models.CASCADE)
	title = models.CharField(max_length=100)
	instruction = models.TextField(max_length=500,null=True,blank=True)
	file = models.FileField(null=True,blank=True,upload_to='files/t_assignments/')
	points = models.CharField(max_length=100, null=True, choices=POINTS, default=100)
	due_date = models.DateField()
	assigning_date = models.DateField(auto_now_add=True)
	last_updated = models.DateTimeField(auto_now=True)
	user = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name='assignments')

	def __str__(self):
		return self.title



class Submission(models.Model):
	file = models.FileField(upload_to='files/s_submissions/')
	submitted_at = models.DateField(auto_now=True)
	last_updated = models.DateField(auto_now=True)
	assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='submissions')
	grade = models.CharField(max_length=100, blank=True, null=True, default='No grade yet')
	feedback = models.CharField(max_length=100, blank=True, null=True, default='No feedback yet')


# class ClassInfo(models.Model):
# 	class_room = models.OneToOneField(ClassRoom,null=True,on_delete=models.CASCADE)
# 	assignments = models.ForeignKey(Assignment,null=True,on_delete=models.SET_NULL)
	
# 	def __str__(self):
# 		return str(self.class_room)

