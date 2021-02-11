from django import forms
from django.forms import ModelForm
from .models import *

class DateInput(forms.DateInput):
	input_type = 'date'


class CreateClassRoom(ModelForm):
	student_key = forms.CharField(max_length=50,help_text='Enter the class joining key so students can use this key to enroll in this classroom')
	class Meta:
		model = ClassRoom
		fields = '__all__'
		exclude = ['user',]

	def clean_student_key(self):
		student_key = self.cleaned_data['student_key']
		if ClassRoom.objects.filter(student_key=student_key).exists():
			raise forms.ValidationError('Class room with this Student key already exists')
		return student_key

class EditClassRoom(ModelForm):
	class Meta:
		model = ClassRoom
		fields = '__all__'
		exclude = ['user',]
		

class CreateAssignment(ModelForm):
	class Meta:
		model = Assignment
		widgets = {'due_date' : DateInput()}
		fields = '__all__'
		exclude = ['user','class_room']


class JoinClassRoom(forms.Form):
	student_key = forms.CharField(max_length=50,help_text='Enter the class joining key provided by class creator')


	def clean_student_key(self):
		student_key = self.cleaned_data['student_key']
		if not ClassRoom.objects.filter(student_key=student_key).exists():
			raise forms.ValidationError('No classroom exists with provided key')
		return student_key