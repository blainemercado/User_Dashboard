from django.shortcuts import render, redirect
from .models import User
from django.contrib import messages
from django.core.urlresolvers import reverse

import re

# Create your views here.
def index(request):
	return render(request, 'login/index.html')

def register(request):
	first = request.POST['first']
	last = request.POST['last']
	email = request.POST['email']
	pass1 = request.POST['pass']
	pass2 = request.POST['confirm']
	
	stuff = User.validateUserManager.validate(first, last, email, pass1, pass2)
	print stuff
	if stuff == True:
		User.objects.create(first_name=first, last_name=last, email=email, password=pass1, confirmation=pass2)
	else:
		if stuff[1] == "name1":
			messages.info(request, 'Name must be at least 2 chars.')
		elif stuff[1] == "name2":
			messages.info(request, 'Name must be at least 2 chars.')
		elif stuff[1] == "email":
			messages.info(request, 'Please enter a valid email')
		elif stuff[1] == "pass1":
			messages.info(request, 'Password needs 8 chars. min')
		elif stuff[1] == "pass2":
			messages.info(request, 'Confirmation password did not match')
		return redirect('/')
	return redirect(reverse('login_success'))

def login(request):
	if User.userLoginManager.verifyLogin(request.POST['email'], request.POST['pass1']) == True:
		return redirect(reverse('login_success'))
	else:
		messages.warning(request, 'Email and Password do not match')
		return redirect(reverse('login_index'))
def success(request):
	context = {
		"names": User.objects.latest('created_at')
	}
	print context
	return render(request, 'login/success.html', context)