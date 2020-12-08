from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from classes.models import ClassRoom


@login_required
def home(request):
	
	classes = ClassRoom.objects.all()
	context = {'classes':classes}
	return render(request, 'home.html',context)