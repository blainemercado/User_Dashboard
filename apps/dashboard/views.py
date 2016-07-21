from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.urlresolvers import reverse
from .models import User, Post, Comment
import bcrypt

# Create your views here.
def index(request):
	return render(request, 'dashboard/index.html')

def login(request):
	return render(request, 'dashboard/login.html')

def logout(request):
	del request.session['currentUser']
	del request.session['userID']
	del request.session['userLevel']
	return render(request, 'dashboard/login.html')

def login_validation(request):
	if User.userLoginManager.verifyLogin(request.POST['email'], request.POST['pass1']) == True:
		curUserInfo = User.objects.filter(email = request.POST['email'])
		request.session['userLevel'] = curUserInfo[0].user_level
		request.session['currentUser'] = curUserInfo[0].first_name
		request.session['userID'] = curUserInfo[0].id
		if request.session['userLevel'] == 9:
			return redirect(reverse('dashboard_admin_dash'))
		else:
			return redirect(reverse('dashboard_dash'))
	else:
		messages.warning(request, 'Email and Password do not match')
		return redirect(reverse('dashboard_login'))

def register(request):
	return render(request, 'dashboard/register.html')

def registration(request):
	first = request.POST['first']
	last = request.POST['last']
	email = request.POST['email']
	pass1 = request.POST['pass1']
	pass2 = request.POST['confirm']
	
	stuff = User.validateUserManager.validate(first, last, email, pass1, pass2)
	print stuff
	if stuff == True:
		my_user = User.objects.get(email=email)
		request.session['currentUser'] = first
		request.session['userID'] = my_user.id
		request.session['userLevel'] = my_user.user_level
	else:
		if stuff[1] == "email":
			messages.info(request, 'Please enter a valid email')
		if stuff[1] == "emailExists":
			messages.info(request, 'That email already exists. Did you forget your password?')
		return redirect('/register')
	return redirect('/dash')

def new(request):
	return render(request, 'dashboard/new.html')

def add(request):
	first = request.POST['first']
	last = request.POST['last']
	email = request.POST['email']
	pass1 = request.POST['pass1']
	pass2 = request.POST['confirm']
	
	stuff = User.validateUserManager.validate(first, last, email, pass1, pass2)
	print stuff
	if stuff == True:
		print "added user"
	else:
		if stuff[1] == "email":
			messages.info(request, 'Please enter a valid email')
		if stuff[1] == "emailExists":
			messages.warning(request, 'That email already exists')
		return redirect('/users/new')
	return redirect('/admin_dash')

def admin_dash(request):
	context = {
		"users": User.objects.all()
	}
	print context
	return render(request, 'dashboard/admin_dash.html', context)

def remove(request, id):
	remUser = User.objects.filter(id=id)
	remUser.delete()
	return redirect(reverse('dashboard_admin_dash'))

def dash(request):
	context = {
		"users": User.objects.all()
	}
	return render(request, 'dashboard/dash.html', context)

def edit_user(request, id):
	context = {
		"user": User.objects.filter(id=id)
	}
	return render(request, 'dashboard/edit_user.html', context)

def edit(request):
	context = {
		"user": User.objects.filter(id=request.session['userID'])
	}
	return render(request, 'dashboard/edit.html', context)

def updateInfo(request, id):
	first = request.POST['first']
	last = request.POST['last']
	email = request.POST['email']
	user_level = int(request.POST['level'])

	edit_user = User.objects.get(id=id)
	edit_user_level = edit_user.user_level
	edit_user_email = edit_user.email
	if edit_user_email == email:
		if User.updateRemoveManager.updateInfoNoE(id, first, last, user_level) == True:
			pass
		else:
			return redirect('/users/edit/'+id)
	else:
	 	if User.updateRemoveManager.updateInfo(id, first, last, email, user_level) == True:
	 		pass
		else:
			return redirect('/users/edit/'+id)
	if edit_user_level != user_level:
		request.session['userLevel'] = user_level
	if str(request.session['userID']) == id:
		return redirect('/users/show/'+id)
	else:
		return redirect(reverse('dashboard_admin_dash'))
	
def updatePassword(request, id):
	newUser = User.objects.get(id=id)
	password = request.POST['pass1']
	confirmation = request.POST['pass2']
	if User.updateRemoveManager.updatePassword(id, password, confirmation) == False:
		return redirect('/users/edit/'+id)
	if str(request.session['userID']) == id:
		return redirect('/users/show/'+id)
	return redirect(reverse('dashboard_admin_dash'))

def updateDescription(request, id):
	newUser = User.objects.get(id=id)
	newUser.description = request.POST['description']
	newUser.save()
	return redirect('/users/show/'+id)

def show(request, id):
	context = {
		"users": User.objects.filter(id=id),
		"posts": Post.objects.filter(post_host=id),
		"comments": Comment.objects.filter()
	}
	return render(request, 'dashboard/show.html', context)

def post(request, id):
	Post.objects.create(post=request.POST['post'], post_creator=User.objects.get(id=request.POST['post_creator']), post_host=User.objects.get(id=id))
	return redirect('/users/show/'+id)

def comment(request, id):
	Comment.objects.create(comment=request.POST['comment'], comment_creator=User.objects.get(id=request.POST['comment_creator']), post=Post.objects.get(id=id))
	userID = request.POST['userID']
	return redirect('/users/show/'+userID)





