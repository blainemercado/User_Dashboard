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
		return redirect(reverse('dashboard_admin_dash'))
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
		pass1 = pass1.encode(encoding="utf-8", errors="strict")
		hashed = bcrypt.hashpw(pass1, bcrypt.gensalt())
		print hashed
		my_user = User.objects.create(first_name=first, last_name=last, email=email, password=hashed)
		print my_user
		print my_user.password
		print User.objects.all()
		if len(User.objects.all()) == 1:
			my_user.user_level = 9
			my_user.save()
		request.session['currentUser'] = first
		request.session['userID'] = my_user.id
		request.session['userLevel'] = my_user.user_level
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
		return redirect('/register')
	return redirect('/dash')

def add(request):
	first = request.POST['first']
	last = request.POST['last']
	email = request.POST['email']
	pass1 = request.POST['pass1']
	pass2 = request.POST['confirm']
	
	stuff = User.validateUserManager.validate(first, last, email, pass1, pass2)
	print stuff
	if stuff == True:
		pass1 = pass1.encode(encoding="utf-8", errors="strict")
		hashed = bcrypt.hashpw(pass1, bcrypt.gensalt())
		print hashed
		my_user = User.objects.create(first_name=first, last_name=last, email=email, password=hashed)
		print my_user
		print my_user.password
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
		return redirect('/register')
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

def new(request):
	return render(request, 'dashboard/new.html')

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
	print "made it to update and here's the user ID:", id
	print request.session['userID']
	first = request.POST['first']
	last = request.POST['last']
	email = request.POST['email']
	newUser = User.objects.get(id=id)
	newUser.user_level = request.POST['level']
	if User.userManager.validName(first, last) == True:
		newUser.first_name = first
		newUser.last_name = last
	else:
		return redirect('/users/edit/'+id) 
	if User.userManager.validEmail(email) == True:
		newUser.email = email
	else:
		return redirect('/users/edit/'+id)
	newUser.save()
	if str(request.session['userID']) == id:
		return redirect('/users/show/'+id)
	else:
		return redirect(reverse('dashboard_admin_dash'))
	
def updatePassword(request, id):
	newUser = User.objects.get(id=id)
	pass1 = request.POST['pass1']
	if len(pass1) > 7 and pass1 == request.POST['pass2']:
		pass1 = pass1.encode(encoding="utf-8", errors="strict")
		print newUser.password
		newUser.password  = bcrypt.hashpw(pass1, bcrypt.gensalt())
		newUser.save()
		print newUser.password
	else:
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





