from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .forms import *
from django.contrib import messages
from .models import *
from accounts.models import *
from django.views.generic.detail import DetailView
from quizes.models import Quiz
import datetime
from django.http import JsonResponse

@login_required
def create_class_view(request):
	
	form = CreateClassRoom()
	join_class_form = JoinClassRoom()
	classes_created = ClassRoom.objects.filter(user=request.user)
	student = Student.objects.filter(student=request.user)
	notifications = Notification.objects.filter(viewed=False)
	
	classes_joined = [] 
	
	for student_info in student:
		classes_joined.append(student_info.class_room)



	if request.method == 'POST':
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
		'notifications': notifications,
	}
	
	return render(request,'classes/create_class.html',context)


@login_required
def announcement_likes_view(request,pk,class_id):
	student = request.user
	class_room = ClassRoom.objects.get(id=class_id)
	announcement = get_object_or_404(Announcement, id=request.POST.get('announcement_id'))
	
	if announcement.likes.filter(id=request.user.id).exists():
		announcement.likes.remove(request.user)
	else:	
		announcement.likes.add(request.user)

	if Student.objects.filter(student=student,class_room=class_room).exists():
		return HttpResponseRedirect(reverse('s_class_info', args=[str(class_id)]))


	return HttpResponseRedirect(reverse('class_info', args=[str(class_id)]))


def announcement_comments_view(request,announcement_id,class_id):
	student = request.user
	class_room = ClassRoom.objects.get(id=class_id) 
	announcement = Announcement.objects.get(id=announcement_id)
	if request.method == 'POST':
		comment_text = request.POST.get('comment_text')
		Comment.objects.create(user=request.user,announcement=announcement,comment_text=comment_text)

		if Student.objects.filter(student=student,class_room=class_room).exists():
			return HttpResponseRedirect(reverse('s_class_info', args=[str(class_id)]))		
	return HttpResponseRedirect(reverse('class_info', args=[str(class_id)]))

def announcement_update_view(request,class_id,announcement_id):
	announcement = Announcement.objects.get(id=announcement_id)
	update_announcement_form = CreateAnnouncement(instance=announcement)
	if request.method == 'POST':
		update_announcement_form = CreateAnnouncement(request.POST,request.FILES,instance=announcement)
		if update_announcement_form.is_valid():
			update_announcement_form.save()
			messages.success(request, 'Announcement updated successfully')
			return redirect('class_info',id=class_id)

	context = {
		'update_announcement_form': update_announcement_form,
		'announcement':announcement,
	}
	return render(request,'classes/update_announcement.html',context)

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
	quizes = Quiz.objects.filter(class_room=classroom)
	lectures = Lecture.objects.filter(class_room=classroom).order_by('-upload_date')

	
	create_class_form = CreateClassRoom(instance=classroom)
	create_assignment_form = CreateAssignment()
	create_announcement_form = CreateAnnouncement()
	create_quiz_form = CreateQuiz()


	announcements = Announcement.objects.filter(class_room=classroom).order_by('-announcement_date')
	if request.method == 'POST':

		if 'upload_lectures' in request.POST:
			lecture_title = request.POST.get('lecture_title')
			lecture_files = request.FILES.getlist('lecture_files')

			for f in lecture_files:
				Lecture.objects.create(title=lecture_title,files=f,class_room=classroom)

			messages.success(request,'Lectures uploaded successfully')
			return redirect('class_info',id=id)

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
		if 'create_quiz' in request.POST:
			create_quiz_form = CreateQuiz(request.POST)
			if create_quiz_form.is_valid():
				instanace = create_quiz_form.save(commit=False)
				instance.user = request.user
				instance.class_room = classroom
				instance.save()
				messages.success(request,'Assignment Quiz created successfully')
				return redirect('class_info',id=id)

	context = {
		'class':get_object_or_404(ClassRoom, pk=id),
		'assignments':assignments,
		'create_class_form':create_class_form,
		'create_assignment_form':create_assignment_form,
		'create_quiz_form':create_quiz_form,
		'students':students,
		'instructors':instructors,
		'classes_created':classes_created,
		'classes_joined':classes_joined,
		'announcements':announcements,
		'quizes':quizes,
		'lectures':lectures,
	}
	return render(request,'classes/class_info.html',context)


def student_work_view(request,class_id,assignment_id):
	class_room = ClassRoom.objects.get(id=class_id)
	assignment = Assignment.objects.get(id=assignment_id)
	submissions = assignment.submissions.all()
	ungraded_sub = assignment.submissions.filter(grade='No grade yet').count()
	grade_form = GradeForm(request.POST or None)
	feedback_form = FeedbackForm(request.POST or None)
	print(submissions)
	if request.method == 'POST':
		if 'submit-feedback' in request.POST:
			if feedback_form.is_valid():
				feedback = request.POST['feedback']
				submission_id = request.POST['submit-feedback']
				submission = Submission.objects.get(id=submission_id)
				submission.feedback = feedback
				submission.save()
				messages.success(request,'Feedback added successfully for '+submission.user.username)
				notification = Notification.objects.create(user=request.user,class_room=class_room,assignment=assignment,title='New Feedback')
		if 'submit-grade' in request.POST:
			if grade_form.is_valid():
				grade = request.POST['grade']
				if grade > assignment.points:
					messages.warning(request,'Max points for this assignment is '+assignment.points)
				else:
					submission_id = request.POST['submit-grade']
					submission = Submission.objects.get(id=submission_id)
					submission.grade = grade
					submission.save()
					messages.success(request,"Submission graded successfully for "+submission.user.username)
					notification = Notification.objects.create(user=request.user,class_room=class_room,assignment=assignment,title='New Grade')
	context = {
		'class':get_object_or_404(ClassRoom, pk=class_id),
		'assignment':get_object_or_404(Assignment, pk=assignment_id),
		'submissions': submissions,
		"grade_form": grade_form,
		'feedback_form': feedback_form,
		'ungraded_sub':ungraded_sub,
		
	}
	return render(request,'classes/student_work.html',context)


@login_required
def s_class_info_view(request,id):
	assignments = Assignment.objects.filter(class_room = id)
	students = Student.objects.filter(class_room= id)
	instructors = Instructor.objects.filter(class_room= id)
	class_room = ClassRoom.objects.get(id=id)
	announcements = class_room.announcements.all().order_by('-announcement_date')
	quizes = Quiz.objects.filter(class_room=class_room)

	context = {
		'class':get_object_or_404(ClassRoom, pk=id),
		'assignments':assignments,
		'quizes':quizes,
		'instructors':instructors,
		'students':students,
		'announcements':announcements,

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

def delete_notification_view(request,notification_id):
	notification = Notification.objects.get(id=notification_id)
	notification.viewed = True
	notification.delete()
	return redirect('create_class')


def s_assignment_detail_view(request,class_id,assignment_id):
	classroom = ClassRoom.objects.get(id=class_id)
	assignment = Assignment.objects.get(id=assignment_id)
	submission_form = SubmitAssignment()
	
	if Submission.objects.filter(user=request.user,assignment=assignment).exists():
		s_submission = Submission.objects.get(user=request.user,assignment=assignment)
		submission_form = SubmitAssignment(instance=s_submission)
	else:
		s_submission = ''

	if request.method == 'POST':
		if 'submit_assignment' in request.POST:
			submission_form = SubmitAssignment(request.POST,request.FILES)
			if submission_form.is_valid():
				instance = submission_form.save(commit=False)
				instance.user = request.user
				instance.assignment = Assignment.objects.get(id=assignment_id)
				instance.save()
				messages.success(request, 'Assignment submitted successfully')
				return redirect('s_class_info',id=class_id)
		if 'resubmit_assignment' in request.POST:
			submission_form = SubmitAssignment(request.POST,request.FILES,instance=s_submission)
			if submission_form.is_valid():
				submission_form.save()
				s_submission.last_updated = datetime.datetime.now()
				s_submission.save()
				messages.success(request, 'Assignment edited successfully')

	context = {
		'assignment': assignment,
		'submission_form': submission_form,
		's_submission' : s_submission,
	}
	return render(request,'classes/s_assignment_detail.html',context)

def attendance_view(request,class_id):
	class_room = ClassRoom.objects.get(id=class_id)
	students = Student.objects.filter(class_room=class_room)
	attendanceForm = AttendanceForm()
	attendances = Attendance.objects.filter(class_room=class_room)
	
	if request.method == 'POST':
		if 'submit-date' in request.POST:
			attendanceForm = AttendanceForm(request.POST)
			if attendanceForm.is_valid():
				created_at = request.POST.get('created_at')
				if Attendance.objects.filter(created_at=created_at).exists():
					messages.warning(request,'You have already submitted attendance for this date')

	if request.is_ajax() and request.method == 'POST':
		created_at = request.POST.get('attDate')
		present_ids = request.POST.getlist('p_ids[]')
		absent_ids = request.POST.getlist('a_ids[]')

		for pid in present_ids:
			student = Student.objects.get(pk=pid)
			Attendance.objects.create(student=student,present=True,class_room=class_room,created_at=created_at)
		for aid in absent_ids:
			student = Student.objects.get(pk=aid)
			Attendance.objects.create(student=student,absent=True,class_room=class_room,created_at=created_at)

		messages.success(request,'Attendance submitted successfully')
		ps = Attendance.objects.filter(present=True)
		present_s = []
		for pr_s in ps:
			present_s.append((pr_s.student.student.first_name, pr_s.present,pr_s.created_at))
		return JsonResponse({
			'attendance':list(present_s),
		})
			
		

	context = {
		'students':students,
		'attendanceForm':attendanceForm,
		'class_room':class_room,
	}
	return render(request,'classes/attendance.html',context)

def view_attendance(request,class_id):
	class_room = ClassRoom.objects.get(id=class_id)
	if request.method=="POST":
		attendance_date = request.POST.get('attendance_date')
		sResult = Attendance.objects.filter(class_room=class_room,created_at=attendance_date)
		return render(request,'classes/view_attendance.html',{"data":sResult,"class_room":class_room})
	else:
		attendances = Attendance.objects.filter(class_room=class_room)
		return render(request,'classes/view_attendance.html',{"data":attendances,"class_room":class_room})

def edit_attendance(request,class_id,att_id):
	class_room = ClassRoom.objects.get(id=class_id)
	attendance = Attendance.objects.get(id=att_id)
	edit_att_form = EditAttendanceForm(instance=attendance)
	if request.method == 'POST':
		edit_att_form = EditAttendanceForm(request.POST,instance=attendance)
		if edit_att_form.is_valid():
			edit_att_form.save()
			messages.success(request, 'Attendance edited successfully')
			return redirect('http://127.0.0.1:8000/classes/class_info/'+str(class_id)+'/view_attendance')

	return render(request,'classes/edit_attendance.html',{'edit_att_form':edit_att_form,'attendance':attendance,'class_room':class_room})