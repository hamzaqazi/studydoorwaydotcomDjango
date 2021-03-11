from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .forms import *
from django.contrib import messages
from .models import *
from accounts.models import *
from django.views.generic.detail import DetailView


@login_required
def create_class_view(request):
	
	form = CreateClassRoom()
	join_class_form = JoinClassRoom()
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
		if 'create_classroom' in request.POST:
			form = CreateClassRoom(request.POST,request.FILES)
			if form.is_valid():
				instance = form.save(commit=False)
				instance.user = request.user
				instance.save()
				classroom = ClassRoom.objects.get(id=instance.id)
				messages.success(request,'Classrooom created successfully')
				return redirect('/classes/create_class/')
			else:
				messages.warning(request,'Error! Classroom not created Please correct the error in the form')
		if 'join_classroom' in request.POST:
			join_class_form = JoinClassRoom(request.POST)
			if join_class_form.is_valid():
				student_key = request.POST.get('student_key')
				class_room = ClassRoom.objects.get(student_key=student_key)
				student = request.user
				if Student.objects.filter(student=student,class_room=class_room).exists():
					messages.warning(request,'you are already a student in this classroom  '+ class_room.class_name)
				elif Instructor.objects.filter(instructor=student,class_room=class_room).exists():
					messages.warning(request,'you are the creator of this class [' + class_room.class_name + '] you can not join this class as student')
				else:					
					new_student = Student(student=student,class_room=class_room)
					new_student.save()
					print(new_student)
					messages.success(request,'Classrooom joined successfully')
					return redirect('/classes/create_class/')

	context = {
		'form': form,
		'join_class_form': join_class_form,
		'classes_created': classes_created,
		'classes_joined': classes_joined,
	}
	
	return render(request,'classes/create_class.html',context)


@login_required
def announcement_likes_view(request,pk,class_id):
	announcement = get_object_or_404(Announcement, id=request.POST.get('announcement_id'))
	
	if announcement.likes.filter(id=request.user.id).exists():
		announcement.likes.remove(request.user)
	else:	
		announcement.likes.add(request.user)

	return HttpResponseRedirect(reverse('class_info', args=[str(class_id)]))

# class AnnouncementLikesDetailView(DetailView):
# 	model = Announcement
# 	template_name = 'classes/class_info.html'
# 	context_object_name = 'object'

# 	def get_context_data(self, **kwargs):
# 		data = super().get_context_data(**kwargs)

# 		likes_connected = get_object_or_404(Announcement, id=self.kwargs['pk'])
# 		liked = False

# 		if likes_connected.likes.filter(id=self.request.user.id).exists():
# 			liked = True
# 		data['total_likes'] = likes_connected.total_likes()
# 		data['ann_is_liked'] = liked
# 		return data

def announcement_comments_view(request,announcement_id,class_id):
	announcement = Announcement.objects.get(id=announcement_id)
	if request.method == 'POST':
		comment_text = request.POST.get('comment_text')
		Comment.objects.create(user=request.user,announcement=announcement,comment_text=comment_text)
	return HttpResponseRedirect(reverse('class_info', args=[str(class_id)]))

@login_required
def class_info_view(request,id):
	student = request.user
	classes_created = ClassRoom.objects.filter(user=request.user)
	student_classes = Student.objects.filter(student=request.user)
	classes_joined = []
	for student_info in student_classes:
		classes_joined.append(student_info.class_room)

	classroom = ClassRoom.objects.get(id=id)
	assignments = Assignment.objects.filter(class_room = id)
	students = Student.objects.filter(class_room=classroom)
	instructors = Instructor.objects.filter(class_room=classroom)


	create_class_form = CreateClassRoom(instance=classroom)
	create_assignment_form = CreateAssignment()
	create_announcement_form = CreateAnnouncement()
	announcements = Announcement.objects.filter(class_room=classroom).order_by('-announcement_date')
	if request.method == 'POST':
		if 'announce' in request.POST:
			
			announcement_text = request.POST.get('announcement_text')
			announcement_file = request.FILES.get('announcement_file',None)
			if not announcement_file:
				Announcement.objects.create(announcement_text=announcement_text,user=request.user,class_room=classroom)
			else:
				# announcement_file = request.FILES['announcement_file']
				Announcement.objects.create(announcement_text=announcement_text,announcement_file=announcement_file,user=request.user,class_room=classroom)
			
			return redirect('class_info',id=id)
			
		if 'edit_class' in request.POST:
			create_class_form = EditClassRoom(request.POST, request.FILES, instance=classroom)
			if create_class_form.is_valid():
				create_class_form.save()
				messages.success(request,'classroom updated successfully')
				return redirect('class_info',id=id)
			else:
				messages.warning(request, create_class_form.errors)

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
		'announcements':announcements,
	}
	return render(request,'classes/class_info.html',context)


def student_work_view(request,class_id):
	# classroom = Classroom.objects.get(class_id=id)
	context = {
		'class':get_object_or_404(ClassRoom, pk=class_id),
	}
	return render(request,'classes/student_work.html',context)
@login_required
def s_class_info_view(request,id):
	assignments = Assignment.objects.filter(class_room = id)
	students = Student.objects.filter(class_room= id)
	instructors = Instructor.objects.filter(class_room= id)

	context = {
		'class':get_object_or_404(ClassRoom, pk=id),
		'assignments':assignments,
		'instructors':instructors,
		'students':students,
	}
	return render(request, 'classes/s_class_info.html',context)

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