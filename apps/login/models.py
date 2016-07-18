from __future__ import unicode_literals

from django.db import models

import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')
#import birthday

class UserLoginManager(models.Manager):
	def verifyLogin(self, email, password):
		print "made it here!!!!"
		if len(User.objects.filter(email=email)) == 0:
			print "Made it here too!!!!!"
			return False
		else:
			print "Hoping to make it here though!!!"
			userInfo = User.objects.filter(email=email)
		print userInfo
		if userInfo[0].password == password:
			return True
		else:
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
			return True
	def validEmail(self, email):
		if len(email) < 1:
			print "Not a long enough email"
			return (False, "email")
		elif not re.match(EMAIL_REGEX, email):
			print "Not a valid email"
			return (False, "email")
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
			return True
		else:
			print passResults
			return passResults

# Create your models here.
class User(models.Model):
	first_name = models.CharField(max_length=50)
	last_name = models.CharField(max_length=50)
	email = models.CharField(max_length=200)
	#birthday = birthday.fields.BirthdayField()
	password = models.CharField(max_length=200)
	confirmation = models.CharField(max_length=200)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	userManager = UserManager()
	validateUserManager = ValidateUserManager()
	userLoginManager = UserLoginManager()
	objects = models.Manager()
	#objects = birthday.managers.BirthdayManager()