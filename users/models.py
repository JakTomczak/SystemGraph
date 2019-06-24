import os

from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
	folder = models.CharField(max_length = 200, null = True)
	
	def __str__(self):
		return self.username
		
	def get_folder(self, save = True):
		if not self.folder:
			dir = os.path.join( settings.BASE_DIR, 'userfiles', self.username )
			if not os.path.isdir(dir):
				os.mkdir(dir)
			self.folder = dir
			if save:
				self.save()
		return self.folder