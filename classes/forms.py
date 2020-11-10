from django import forms
from django.forms import ModelForm
from .models import ClassRoom,Assignment

class DateInput(forms.DateInput):
	input_type = 'date'


class CreateClassRoom(ModelForm):
	class Meta:
		model = ClassRoom
		fields = '__all__'
		exclude = ['user']

class CreateAssignment(ModelForm):
	class Meta:
		model = Assignment
		widgets = {'due_date' : DateInput()}
		fields = '__all__'
		exclude = ['user','class_room']