from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import CreateClassRoom,CreateAssignment
from django.contrib import messages
from .models import *


@login_required
def create_class_view(request):
	form = CreateClassRoom()
	classes = ClassRoom.objects.filter(user=request.user) 

	if request.method =='POST':
		form = CreateClassRoom(request.POST,request.FILES)
		if form.is_valid():
			instance = form.save(commit=False)
			instance.user = request.user
			instance.save()
			messages.success(request,'Classrooom created successfully')
			return redirect('/classes/create_class/')
	context = {'form': form, 'classes': classes}
	return render(request,'classes/create_class.html',context)


@login_required
def class_info_view(request,id):
	assignments = Assignment.objects.filter(class_room = id)
	classroom = ClassRoom.objects.get(id=id)
	create_class_form = CreateClassRoom(instance=classroom)
	create_assignment_form = CreateAssignment()
	if request.method == 'POST':
		if 'edit_class' in request.POST:
			create_class_form = CreateClassRoom(request.POST, request.FILES, instance=classroom)
			if create_class_form.is_valid():
				create_class_form.save()
				messages.success(request,'classroom updated successfully')
				return redirect('class_info',id=id)
			else:
				messages.success(request,'error! classroom not updated')

		if 'create_assignment' in request.POST:
			create_assignment_form = CreateAssignment(request.POST, request.FILES)
			if create_assignment_form.is_valid():
				instance = create_assignment_form.save(commit=False)
				instance.user = request.user
				instance.class_room = classroom
				instance.save()
				messages.success(request,'Assignment created successfully')
				create_assignment_form = CreateAssignment()
				return redirect('class_info',id=id)
	context = {
		'class':get_object_or_404(ClassRoom, pk=id),
		'assignments':assignments,
		'create_class_form':create_class_form,
		'create_assignment_form':create_assignment_form,
	}
	return render(request,'classes/class_info.html',context)


def update_assignment_view(request,class_id,assignment_id):
	assignment = Assignment.objects.get(id=assignment_id)
	update_assignment_form = CreateAssignment(instance=assignment)
	if request.method == 'POST':
		update_assignment_form = CreateAssignment(request.POST,request.FILES,instance=assignment)
		if update_assignment_form.is_valid():
			update_assignment_form.save()
			messages.success(request, 'Assignment updated successfully')
			return redirect('class_info',id=class_id)

	context = {
		'update_assignment_form': update_assignment_form,
		'assignment':assignment,
	}		
	return render(request,'classes/update_assignment.html',context)



def delete_assignment_view(request,class_id,assignment_id):
	assignment = Assignment.objects.get(id=assignment_id)
	if request.method == 'POST':
		assignment.delete()
		messages.warning(request, 'Assignment deleted successfully')
		return redirect('class_info',id=class_id)

	context = {
		'assignment':assignment,
	}
	return render(request,'classes/delete_assignment.html',context)