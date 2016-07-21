from __future__ import unicode_literals

from django.db import models

import bcrypt
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')
#import birthday

class UserLoginManager(models.Manager):
	def verifyLogin(self, email, password):
		print "made it here!!!!"
		if len(User.objects.filter(email=email)) == 0:
			print "Email does not match any email in database"
			return False
		else:
			print "Email does exist, grabbing user info from email to use password for validation"
			userInfo = User.objects.filter(email=email)
		print userInfo[0].password
		if bcrypt.hashpw(password.encode(encoding="utf-8", errors="strict"), userInfo[0].password.encode(encoding="utf-8", errors="strict")) == userInfo[0].password.encode(encoding="utf-8", errors="strict"):
			print "validated"
			return True
		else:
			print "no match"
			return False

class UserManager(models.Manager):
	def validName(self, first_name, last_name):
		if len(first_name) < 2:
			print first_name, "first not long enough"
			return (False, "name1")
		else:
			print "first name is good"
		if len(last_name) < 2:
			print last_name, "last not long enough"
			return (False, "name2")
		else:
			print "both first and last names came back true"
			return True
	def validEmail(self, email):
		if len(email) < 1:
			print "Not a long enough email"
			return (False, "email")
		elif not re.match(EMAIL_REGEX, email):
			print "Not a valid email"
			return (False, "email")
		elif len(User.objects.filter(email=email)) > 0:
			print "email already exists"
			return (False, "emailExists")
		print "The EmailManager validate function is working", email
		return True
	def confirmPass(self, password, confirmation):
		if len(password) < 8:
			print password, "Password needs 8 chars. min."
			return (False, "pass1")
		else:
			pass
		if confirmation == password:
			return True
		else:
			return (False, "pass2")

class ValidateUserManager(models.Manager):
	def validate(self, first_name, last_name, email, password, confirmation):
		nameResults = User.userManager.validName(first_name, last_name)
		print nameResults
		emailResults = User.userManager.validEmail(email)
		print emailResults
		passResults = User.userManager.confirmPass(password, confirmation)
		print passResults
		if nameResults==True:
			pass
		else:
			print nameResults
			return nameResults 
		if emailResults==True:
			pass
		else:
			print emailResults
			return emailResults 
		if passResults==True:
			print "all 3 equal True"
			pass1 = password.encode(encoding="utf-8", errors="strict")
			hashed = bcrypt.hashpw(pass1, bcrypt.gensalt())
			print hashed
			my_user = User.objects.create(first_name=first_name, last_name=last_name, email=email, password=hashed)
			if len(User.objects.all()) == 1:
				my_user.user_level = 9
				my_user.save()
			return True
		else:
			print passResults
			return passResults

class UpdateRemoveManager(models.Manager):
	def updateInfo(self, id, first_name, last_name, email, user_level):
		editUser = User.objects.get(id=id)
		editUser.user_level = user_level
		if User.userManager.validName(first_name, last_name) == True:
			editUser.first_name = first_name
			editUser.last_name = last_name
		else:
			return False
		if User.userManager.validEmail(email) == True:
			editUser.email = email
		else:
			return False
		editUser.save()
		return True

	def updateInfoNoE(self, id, first_name, last_name, user_level):
		editUser = User.objects.get(id=id)
		editUser.user_level = user_level
		if User.userManager.validName(first_name, last_name) == True:
			editUser.first_name = first_name
			editUser.last_name = last_name
			editUser.save()
			return True
		else:
			return False
	
	def updatePassword(self, id, password, confirmation):
		editUser = User.objects.get(id=id)
		if User.userManager.confirmPass(password, confirmation) == True:
			pass1 = password.encode(encoding="utf-8", errors="strict")
			editUser.password  = bcrypt.hashpw(pass1, bcrypt.gensalt())
			editUser.save()
			return True
		else:
			return False

	def remove(self, id):
		pass

# Create your models here.
class User(models.Model):
	first_name = models.CharField(max_length=50)
	last_name = models.CharField(max_length=50)
	email = models.CharField(max_length=200)
	password = models.CharField(max_length=200)
	user_level = models.IntegerField(default=1)
	description = models.TextField(max_length=1000, default="Welcome to the Group! You can edit your personal description by clicking on the 'Edit Profile' button")
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	userManager = UserManager()
	validateUserManager = ValidateUserManager()
	userLoginManager = UserLoginManager()
	updateRemoveManager = UpdateRemoveManager()
	objects = models.Manager()
