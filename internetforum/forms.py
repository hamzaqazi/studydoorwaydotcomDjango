from django.forms import ModelForm
from django import forms
from .models import Answer,Question


class AnswerForm(ModelForm):
	class Meta:
		model = Answer
		fields = ('detail',)

class QuestionForm(ModelForm):
	class Meta:
		model = Question
		fields = ('title','detail','tags')
