import os
import codecs

from django.db import models
from django.conf import settings
import django.core.exceptions as exceptions
from django.urls import reverse

from . import vertex as vertex_models
import users.models as user_model
import SGMain.tools as tools
	
class Edge_Class(models.Model):
	polish_name = models.CharField(max_length = 60, default = 'Nienazwana krawędź')
		
	class Meta:
		verbose_name_plural = "Edge Classes"
	
	def __str__(self):
		return self.polish_name
		
	@classmethod
	def FIRST_TIME_RUN_ADD_DEFAULT_ECLASS(cls):
		default = Edge_Class( polish_name = 'Od wewnątrz do wewnątrz.' )
		default.save()
	
class Edge(models.Model):
	edge_id = models.CharField(max_length = 10, primary_key = True, default = 'EAAAAAAAAA')
	edge_class = models.ForeignKey(Edge_Class, on_delete = models.SET_NULL, null = True)
	preamble = models.ForeignKey(vertex_models.Preamble, on_delete = models.SET_DEFAULT, default = settings.DEFAULT_PREAMBLE_ID)
	user = models.ForeignKey(user_model.CustomUser, on_delete = models.SET_DEFAULT, default = 1)
	predecessor = models.ForeignKey(vertex_models.Vertex, on_delete = models.CASCADE, related_name='predecessor', null = True)
	successor = models.ForeignKey(vertex_models.Vertex, on_delete = models.CASCADE, related_name='successor', null = True)
	validated = models.BooleanField(default = False)
	directory = models.CharField(max_length = 200, null = True)
	
	def __str__(self):
		return self.edge_id
		
	@classmethod
	def new_id(cls):
		id = tools.id_generator('E')
		while len( cls.objects.filter(edge_id = id) ):
			id = tools.id_generator('E')
		return id
		
	'''
	Content of edge is meant to represent description of relationship between
	its predecessor and successor. If no content is given,
	it's assumed that successor desciption is enough.
	This two methods are not fused together, because they are called in django templates,
	so they cannot take arguments, lol.
	'''
	def get_content (self):
		try:
			f = codecs.open( self.directory, 'r', encoding = 'utf-8')
		except (TypeError, IOError):
			return ''
		else:
			t = f.read()
			f.close()
			return t
		
	def get_true_content (self):
		try:
			f = codecs.open( self.directory, 'r', encoding = 'utf-8')
		except (TypeError, IOError):
			if self.successor:
				return self.successor.description()
			else:
				return ''
		else:
			t = f.read()
			f.close()
			return t
			
	'''
	Similar to Vertices, Edges also have their content in pre- and post compilation versions
	and similar to Vertices, pres are not stored as model fields.
	'''
	def get_pre_dir(self):
		return os.path.join( self.user.get_folder(), self.edge_id + '.txt' )
		
	def create_pre_dir(self):
		codecs.open( self.get_pre_dir(), 'w+', encoding = 'utf-8').close()
		
	def write_pre_dir(self, text):
		with codecs.open( self.get_pre_dir(), 'w', encoding = 'utf-8') as file:
			file.truncate()
			file.write( text )
			
	def read_pre_dir(self):
		with codecs.open( self.get_pre_dir(), 'r', encoding = 'utf-8') as file:
			return file.read()
	
	def delete_pre_dir(self):
		try:
			os.remove( self.get_pre_dir() )
		except FileNotFoundError:
			pass
	
	def get_links(self):
		if self.links:
			return self.link
		return ''
			
	def get_url(self):
		return reverse('edit_edge', kwargs={'edge_id': self.edge_id})
	
	def get_successor_id(self):
		if self.successor:
			return self.successor.vertex_id
		else:
			return None
		
	def get_successor_url(self):
		if self.successor:
			return self.successor.get_url()
		else:
			return '#'