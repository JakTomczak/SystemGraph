import datetime
import os
import codecs

from django.db import models
from django.conf import settings
import django.core.exceptions as exceptions
from django.urls import reverse

import users.models as user_model
import SGMain.tools as tools
	
'''
Vertex_Class is what your Vertex is in the context of meta-narration, ie. 
Vertex "definition of integral" is of Class "definition",
or Vertex "how to use SystemGraph's Vertex Classes" if of Class "tutorial point",
or Vertex "yo mamma fat" is of Class "universal truth".
'''
class Vertex_Class(models.Model):
	polish_name = models.CharField(max_length = 50, default = 'Nienazwany wierzchołek')
	polish_name_plural = models.CharField(max_length = 50, default = 'Nienazwane wierzchołki')
	left = models.ForeignKey('self', null = True, on_delete = models.SET_NULL, related_name='onleft')
	right = models.ForeignKey('self', null = True, on_delete = models.SET_NULL, related_name='onright')
	top = models.ForeignKey('self', null = True, on_delete = models.SET_NULL, related_name='ontop')
	bottom = models.ForeignKey('self', null = True, on_delete = models.SET_NULL, related_name='onbottom')
	is_default = models.BooleanField(default = False)
		
	class Meta:
		verbose_name_plural = "Vertexes Classes"
	
	def __str__(self):
		return self.polish_name
	
	'''
	This model is central to SystemGraph, so I cannot just let users create it,
	but nevertheless users may want to add new vertex classes with custom behaviour,
	so I created this method for users to easily propose new VC to me.
	'''
	@classmethod
	def make_proposal(cls, user, data_dict):
		message = str(datetime.datetime.now()) + '\nNew Vertex_Class\n'
		message += 'user: ' + user.username + '\n'
		for key in data_dict:
			message += key + ': ' + data_dict[key] + '\n'
		tools.userproposal(message)
		
	@classmethod
	def FIRST_TIME_RUN_ADD_DEFAULT_VCLASS(cls):
		default = Vertex_Class(polish_name = 'testowy', polish_name_plural = 'testowe', is_default = True)
		default.save()
		default.left = default
		default.right = default
		default.top = default
		default.bottom = default
		default.save()

'''
Preamble is essential during LaTeX -> HTML compilation.
It basically holds your settings for this compilation.
'''
class Preamble(models.Model):
	preamble_id = models.CharField(max_length = 10, primary_key = True, default = settings.DEFAULT_PREAMBLE_ID)
	user = models.ForeignKey(user_model.CustomUser, on_delete = models.CASCADE)
	title = models.CharField(max_length = 60, default = 'My preamble')
	description = models.CharField(max_length = 200, null = True)
	directory = models.CharField(max_length = 200, default = os.path.join( settings.COMP_DIR, settings.DEFAULT_PREAMBLE_ID + '.tex' ))
	is_default = models.BooleanField(default = False)
	
	def __str__(self):
		if self.description:
			return self.title + ' (' + self.description + ')'
		else:
			return self.title
		
	@classmethod
	def new_id(cls):
		id = tools.id_generator('A')
		while len( cls.objects.filter(preamble_id = id) ):
			id = tools.id_generator('A')
		return id
		
	def create_content_dir(self, content = '', save = False):
		self.directory = os.path.join( self.user.get_folder(), self.preamble_id + '.tex' )
		if content:
			self.write(content)
		else:
			open( self.directory, 'w+').close()
		if save:
			self.save()
		
	def write(self, text):
		with codecs.open( self.directory, 'w+', encoding = 'utf-8') as file:
			file.truncate()
			file.write( text )
		
	def read(self):
		with codecs.open( self.directory, 'r', encoding = 'utf-8') as file:
			return file.read()
	
	# Because there are default Preambles available to everyone.
	@classmethod
	def get_user_preambles(cls, user):
		if user:
			return Preamble.objects.filter(user = user) | Preamble.objects.filter(is_default = True)
		else:
			return Preamble.objects.filter(is_default = True)
	
	@classmethod
	def FIRST_TIME_RUN_ADD_DEFAULT_PREAMBLES(cls, admin):
		A = Preamble(preamble_id = 'AAAAAAAAAA', user = admin, is_default = True)
		A.title = 'Default preamble'
		A.description = 'It works with plain english text and math formulas.'
		A.save()
		B = Preamble(preamble_id = 'AAAAAAAAAB', user = admin, is_default = True)
		B.directory = os.path.join( settings.COMP_DIR, 'AAAAAAAAAB.tex' )
		B.title = 'Domyślna preambuła'
		B.description = 'Działa z tekstem polskim i matematycznymi formułami.'
		B.save()
	
class Discipline(models.Model):
	polish_name = models.CharField(max_length = 60, default = 'Nienazwana dyscyplina')
	is_default = models.BooleanField(default = False)
	
	def __str__(self):
		return self.polish_name
	
	def perms(self, user):
		perms_dict = user.is_authorized('discipline')
		empty = len( Vertex.objects.filter(discipline = self) ) < 1
		edit_p = perms_dict['full_edit'] or ( perms_dict['empty_edit'] and empty )
		delete_p = perms_dict['delete'] or ( perms_dict['empty_delete'] and empty )
		return delete_p, edit_p
		
	def propose_deletion(self, user):
		message = str(datetime.datetime.now()) + '\n'
		message += 'user: ' + user.username + '\n'
		message += 'delete discipline\nstr: ' + str(self) + ', pk: ' + str(self.pk) + '\n'
		tools.userproposal(message)
	
	def propose_change(self, user, data_dict):
		message = str(datetime.datetime.now()) + '\nDiscipline change\n'
		message += 'user: ' + user.username + '\n'
		message += 'discipline str: ' + str(self) + ', pk: ' + str(self.pk) + '\n'
		for key in data_dict:
			message += key + ': ' + data_dict[key] + '\n'
		tools.userproposal(message)
	
	@classmethod
	def FIRST_TIME_RUN_ADD_DEFAULT_DISCIPLINE(cls):
		Discipline(polish_name = 'Brak dyscypliny', is_default = True).save()
		
class Section(models.Model):
	polish_name = models.CharField(max_length = 60, default = 'Nienazwany dział')
	discipline = models.ForeignKey(Discipline, on_delete = models.CASCADE)
	is_default = models.BooleanField(default = False)
	
	def __str__(self):
		return self.polish_name
	
	def perms(self, user):
		perms_dict = user.is_authorized('section')
		empty = len( Vertex.objects.filter(section = self) ) < 1
		edit_p = perms_dict['full_edit'] or ( perms_dict['empty_edit'] and empty )
		delete_p = perms_dict['delete'] or ( perms_dict['empty_delete'] and empty )
		return delete_p, edit_p
		
	def propose_deletion(self, user):
		message = str(datetime.datetime.now()) + '\n'
		message += 'user: ' + user.username + '\n'
		message += 'delete section\nstr: ' + str(self) + ', pk: ' + str(self.pk) + '\n'
		tools.userproposal(message)
	
	def propose_change(self, user, data_dict):
		message = str(datetime.datetime.now()) + '\nSection change\n'
		message += 'user: ' + user.username + '\n'
		message += 'section str: ' + str(self) + ', pk: ' + str(self.pk) + '\n'
		for key in data_dict:
			message += key + ': ' + data_dict[key] + '\n'
		tools.userproposal(message)
	
	@classmethod
	def FIRST_TIME_RUN_ADD_DEFAULT_SECTION(cls):
		Section(
			polish_name = 'Brak działu', 
			discipline = Discipline.objects.get(is_default = True), 
			is_default = True
		).save()
		
class Subject(models.Model):
	polish_name = models.CharField(max_length = 60, default = 'Nienazwany temat')
	section = models.ForeignKey(Section, on_delete = models.CASCADE)
	discipline = models.ForeignKey(Discipline, on_delete = models.CASCADE)
	is_default = models.BooleanField(default = False)
	
	def __str__(self):
		return self.polish_name
	
	def big_str(self):
		return str(self.discipline) + ' --> ' + str(self.section) + ' --> ' + str(self)
		
	def ajax(self):
		return {
			'big_str': self.big_str(), 
			'pk': self.pk, 
			'edit_url': self.get_edit_url() 
		}
	
	def get_edit_url(self):
		return reverse('edit_subject', kwargs={'pk': self.pk})
	
	@classmethod
	def get_default(cls):
		try:
			return Subject.objects.get(is_default = True)
		except exceptions.ObjectDoesNotExist:
			return Subject.objects.all()[0]
	
	def perms(self, user):
		perms_dict = user.is_authorized('subject')
		empty = len( Vertex.objects.filter(subject = self) ) < 1
		edit_p = perms_dict['full_edit'] or ( perms_dict['empty_edit'] and empty )
		delete_p = perms_dict['delete'] or ( perms_dict['empty_delete'] and empty )
		return delete_p, edit_p
		
	def propose_deletion(self, user):
		message = str(datetime.datetime.now()) + '\n'
		message += 'user: ' + user.username + '\n'
		message += 'delete subject\nstr: ' + str(self) + ', pk: ' + str(self.pk) + '\n'
		tools.userproposal(message)
	
	def propose_change(self, user, data_dict):
		message = str(datetime.datetime.now()) + '\nSubject change\n'
		message += 'user: ' + user.username + '\n'
		message += 'subject str: ' + str(self) + ', pk: ' + str(self.pk) + '\n'
		for key in data_dict:
			message += key + ': ' + data_dict[key] + '\n'
		tools.userproposal(message)
	
	@classmethod
	def FIRST_TIME_RUN_ADD_DEFAULT_SUBJECT(cls):
		Subject(
			polish_name = 'Brak tematu', 
			discipline = Discipline.objects.get(is_default = True), 
			section = Section.objects.get(is_default = True, discipline = discipline),
			is_default = True
		).save()

class Vertex(models.Model):
	vertex_id = models.CharField(max_length = 10, primary_key = True, default = 'VAAAAAAAAA')
	vertex_class = models.ForeignKey(Vertex_Class, on_delete = models.SET_DEFAULT, default = 1)
	preamble = models.ForeignKey(Preamble, on_delete = models.SET_DEFAULT, default = settings.DEFAULT_PREAMBLE_ID)
	user = models.ForeignKey(user_model.CustomUser, on_delete = models.CASCADE)
	discipline = models.ForeignKey(Discipline, on_delete = models.SET_DEFAULT, default = 1)
	section = models.ForeignKey(Section, on_delete = models.SET_DEFAULT, default = 1)
	subject = models.ForeignKey(Subject, on_delete = models.SET_DEFAULT, default = 1)
	date = models.DateTimeField(auto_now = True)
	title = models.CharField(max_length = 120, default = 'no title')
	shorttitle = models.CharField(max_length = 40, null = True, blank = True)
	submitted = models.BooleanField(default = False)
	desc_dir = models.CharField(max_length = 200, null = True)
	content_dir = models.CharField(max_length = 200, null = True)
	is_default = models.BooleanField(default = False)
		
	class Meta:
		verbose_name_plural = "Vertices"
	
	def __str__(self):
		return str(self.discipline) + ': ' + self.title + ' (' + self.vertex_id + ')'
	
	def str2(self):
		return str(self.discipline) + ', ' + str(self.user) + ': ' + self.title
		
	def ajax(self):
		return { 'str': str(self), 'vid': self.vertex_id, 'description': self.description(), 'view_url': self.get_url(), 'edit_url': self.get_edit_url() }
		
	@classmethod
	def new_id(cls):
		id = tools.id_generator('V')
		while len( cls.objects.filter(vertex_id = id) ):
			id = tools.id_generator('V')
		return id
		
	@classmethod
	def get_submitted(cls):
		return Vertex.objects.filter( submitted = True )
		
	def description (self):
		if self.submitted:
			try:
				f = codecs.open( self.desc_dir, 'r', encoding = 'utf-8')
			except (TypeError, IOError):
				return ''
			else:
				t = f.read()
				f.close()
				return t
		else:
			return ''
			
	def get_url(self):
		return reverse('view_vertex', kwargs={'vertex_id': self.vertex_id})
			
	def get_edit_url(self):
		return reverse('edit_vertex', kwargs={'vertex_id': self.vertex_id})
		
	def get_successors(self):
		from . import edge as edge_models
		return edge_models.Edge.objects.filter(predecessor = self)
			
	def save_from_dict(self, dict):
		for key in dict:
			setattr(self, key, dict[key])
		self.save()

	'''
	Note there are two desc and content dirs: 
	one pair pre-compilation and second after-compilation.
	As after-compilation are stored as fields, this functions operates on the pre-compilation ones.
	'''
	def get_pre_content_dir(self):
		return os.path.join( self.user.get_folder(), self.vertex_id + '.txt' )
		
	def get_pre_desc_dir(self):
		return os.path.join( self.user.get_folder(), self.vertex_id + 'desc.txt' )
		
	def create_pre_dirs(self):
		open( self.get_pre_content_dir(), 'w+').close()
		open( self.get_pre_desc_dir(), 'w+').close()
	
	def delete_pre_dirs(self):
		try:
			os.remove( self.get_pre_content_dir() )
		except FileNotFoundError:
			pass
		try:
			os.remove( self.get_pre_desc_dir() )
		except FileNotFoundError:
			pass
			
	def write_pre_content(self, text):
		with codecs.open( self.get_pre_content_dir(), 'w', encoding = 'utf-8') as file:
			file.truncate()
			file.write( text )
			
	def write_pre_desc(self, text):
		with codecs.open( self.get_pre_desc_dir(), 'w', encoding = 'utf-8') as file:
			file.truncate()
			file.write( text )
			
	'''
	Another file related to every object of this class is file with encoded sglinks.
	Sglinks are part of compilation. And this file is then created.
	'''
	def get_sglinks_dir(self, cwd):
		return os.path.join( cwd, self.vertex_id + 'sglinks.txt' )
	
	def write_sglinks(self, text, cwd):
		with open( self.get_sglinks_dir(cwd), 'w+') as file:
			file.truncate()
			file.write( text )
	
	@classmethod
	def FIRST_TIME_RUN_ADD_DEFAULT_VERTEX(cls, admin):
		V = Vertex(user = admin, title = 'Dummy vertex', shorttitle = 'Dummy', submitted = True, is_default = True)
		V.create_pre_dirs()
		V.save()
	
	@classmethod
	def get_default(cls):
		try:
			return Vertex.objects.get(is_default = True)
		except exceptions.ObjectDoesNotExist: # More then one default Vertex is forbidden in this project.
			return Vertex.objects.all()[0]