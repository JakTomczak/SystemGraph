import os

from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser

permissions = {
	'discipline': {
		'delete': 400,
		'empty_delete': 200,
		'full_edit':  300,
		'empty_edit': 100,
		'new_language': 101,
	},
	'section': {
		'delete': 310,
		'empty_delete': 110,
		'full_edit':  200,
		'empty_edit': 10,
		'new_language': 1,
	},
	'subject': {
		'delete': 310,
		'empty_delete': 1,
		'full_edit':  100,
		'empty_edit': 1,
		'new_language': 1,
	},
}

class CustomUser(AbstractUser):
	folder = models.CharField(max_length = 200, null = True)
	permissions = models.IntegerField(default = 0)
	
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
		
	def is_authorized(self, to_what):
		perms =  permissions[to_what]
		out = {}
		for key in perms:
			out[key] = self.permissions >= perms[key]
		return out
	
	def how_many_vertices(self):
		from SGMain.models import Vertex
		return len( Vertex.objects.filter(user = self, submitted = True) )