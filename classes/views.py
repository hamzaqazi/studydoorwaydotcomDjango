from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import CreateClassRoom,CreateAssignment
from django.contrib import messages
from .models import *
from accounts.models import *


@login_required
def create_class_view(request):
	
	form = CreateClassRoom()
	classes_created = ClassRoom.objects.filter(user=request.user)
	student = Student.objects.filter(student=request.user)
	# student = get_object_or_404(Student, pk=request.user.id)
	# s_class_id = student.class_room.id
	# classes_joined = ClassRoom.objects.filter(id=s_class_id)
	classes_joined = []
	for student_info in student:
		classes_joined.append(student_info.class_room)
		# if settings.DEBUG:
		# 	print(student_info.class_room)

	if request.method =='POST':
		form = CreateClassRoom(request.POST,request.FILES)
		if form.is_valid():
			instance = form.save(commit=False)
			instance.user = request.user
			instance.save()
			classroom = ClassRoom.objects.get(id=instance.id)
			messages.success(request,'Classrooom created successfully')
			return redirect('/classes/create_class/')
	context = {'form': form, 'classes_created': classes_created,'classes_joined': classes_joined,}
	return render(request,'classes/create_class.html',context)


@login_required
def class_info_view(request,id):
	student = request.user
	classes_created = ClassRoom.objects.filter(user=request.user)
	student_classes = Student.objects.filter(student=request.user)
	classes_joined = []
	for student_info in student_classes:
		classes_joined.append(student_info.class_room)


	classroom = ClassRoom.objects.get(id=id)
	if Student.objects.filter(student=student, class_room=classroom).exists():

		return render(request, 'classes/s_class_info.html')
	assignments = Assignment.objects.filter(class_room = id)
	students = Student.objects.filter(class_room=classroom)
	instructors = Instructor.objects.filter(class_room=classroom)
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
		'students':students,
		'instructors':instructors,
		'classes_created':classes_created,
		'classes_joined':classes_joined,
	}
	return render(request,'classes/class_info.html',context)

@login_required
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


@login_required
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