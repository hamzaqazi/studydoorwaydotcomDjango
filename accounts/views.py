from django.shortcuts import render,redirect
from django.contrib.sessions.models import Session
from django.contrib import messages

from django.contrib.auth import(
	authenticate,
	get_user_model,
	login,
	logout,
) 

from .forms import UserLoginForm, UserRegisterForm,UserProfileForm

def login_view(request):
	next = request.GET.get('next')
	form = UserLoginForm(request.POST or None)
	if form.is_valid():
		username = form.cleaned_data.get('username')
		password = form.cleaned_data.get('password')
		user = authenticate(username=username, password=password)
		login(request,user)
		messages.success(request,'loged-in successfully!')
		if next:
			return redirect(next)

		request.session['is_loged'] = True	
		return redirect('/')
	

	context = {
		'form':form,
	}
	return render(request, 'accounts/login.html',context)		



def register_view(request):
	next = request.GET.get('next')
	form = UserRegisterForm(request.POST or None)
	
	if form.is_valid():
		user = form.save(commit=False)
		password = form.cleaned_data.get('password')
		user.set_password(password)
		user.save()
		new_user = authenticate(username=user.username, password=password)
		login(request, new_user)

		if next:
			return redirect(next)
		return redirect('/')
	

	context = {
		'form':form,
	}
	return render(request, 'accounts/signup.html',context)		



def logout_view(request):
	if request.method =="POST":
		logout(request)
		messages.success(request,'loged-out successfully')
		return redirect('/')
	return render(request,'accounts/logout.html') 	

def userprofile_view(request):
	user_profile = request.user.userprofile
	form = UserProfileForm(instance=user_profile)
	if request.method =='POST':
		form = UserProfileForm(request.POST,request.FILES,instance=user_profile)
		if form.is_valid():
			form.save()
			messages.success(request,'Userprofile updated successfully')
	context = {'form':form}	
	return render(request,'accounts/userprofile.html',context)