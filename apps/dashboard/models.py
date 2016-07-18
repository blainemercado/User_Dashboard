from __future__ import unicode_literals

from django.db import models

from ..login.models import User

import bcrypt

import re


# Create your models here.
class Post(models.Model):
	post = models.TextField(max_length=1000)
	post_creator = models.ForeignKey(User)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)