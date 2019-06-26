
import datetime
import os
import codecs

from django.db import models
from django.conf import settings
from django.dispatch import receiver
import django.core.exceptions as exceptions
from django.urls import reverse

from users.models import CustomUser
	
'''
Vertex_Class is what your Vertex is in the context of meta-narration, ie. 
Vertex "definition of integral" is of Class "definition",
or Vertex "how to use SystemGraph's Vertex Classes" if of Class "tutorial point",
or Vertex "yo mamma fat" is of Class "universal truth".

'''
class Vertex_Class (models.Model):
	polish_name = models.CharField(max_length = 50, default = 'Nienazwany wierzchołek')
	polish_name_plural = models.CharField(max_length = 50, default = 'Nienazwane wierzchołki')
	left = models.ForeignKey('self', null = True, on_delete = models.SET_NULL, related_name='onleft')
	right = models.ForeignKey('self', null = True, on_delete = models.SET_NULL, related_name='onright')
	top = models.ForeignKey('self', null = True, on_delete = models.SET_NULL, related_name='ontop')
	bottom = models.ForeignKey('self', null = True, on_delete = models.SET_NULL, related_name='onbottom')
	
	def __str__(self):
		return self.polish_name
		
	class Meta:
		verbose_name_plural = "Vertexes Classes"
		
	@classmethod
	def FIRST_TIME_RUN_ADD_DEFAULT_VCLASS(cls):
		default = Vertex_Class()
		default.polish_name = 'testowy'
		default.polish_name_plural = 'testowe'
		default.save()
		default.left = default
		default.right = default
		default.top = default
		default.bottom = default
		default.save()

'''
Preamble is essential during LaTeX -> HTML compilation.
It basicly holds your settings for this compilation.

'''
class Preamble (models.Model):
	preamble_id = models.CharField(max_length = 10, primary_key = True, default = 'AAAAAAAAAA')
	user = models.ForeignKey(CustomUser, on_delete = models.CASCADE)
	title = models.CharField(max_length = 60, default = 'My preamble')
	description = models.CharField(max_length = 200, null = True)
	directory = models.CharField(max_length = 200, default = os.path.join( settings.BASE_DIR, 'static', 'AAAAAAAAAA.txt' ))
	
	def __str__(self):
		if self.description:
			return self.title + ' (' + self.description + ')'
		else:
			return self.title
	
	# Because there are default Preambles available to everyone.
	@classmethod
	def get_user_preambles(cls, user):
		if user:
			return Preamble.objects.filter(user = user) | Preamble.objects.filter(preamble_id = 'AAAAAAAAAA') | Preamble.objects.filter(preamble_id = 'AAAAAAAAAB')
		else:
			return Preamble.objects.filter(preamble_id = 'AAAAAAAAAA') | Preamble.objects.filter(preamble_id = 'AAAAAAAAAB')
	
	@classmethod
	def FIRST_TIME_RUN_ADD_DEFAULT_PREAMBLES(cls, admin):
		A = Preamble(preamble_id = 'AAAAAAAAAA', user = admin)
		A.title = 'Default preamble'
		A.desciption = 'It works with english planar text and math formulas.'
		A.save()
		B = Preamble(preamble_id = 'AAAAAAAAAB', user = admin)
		B.directory = os.path.join( settings.BASE_DIR, 'static', 'AAAAAAAAAB.txt' )
		B.title = 'Domyślna preambuła'
		B.desciption = 'Działa z tekstem polskim i matematycznymi formułami.'
		B.save()

@receiver(models.signals.pre_delete, sender = Preamble)
def delete_preamble_files (sender, instance, using, **kwargs):
	os.remove(instance.directory)
	
class Discipline (models.Model):
	polish_name = models.CharField(max_length = 60, default = 'Nienazwana dyscyplina')
	
	def __str__(self):
		return self.polish_name
		
class Subject (models.Model):
	polish_name = models.CharField(max_length = 60, default = 'Nienazwany temat')
	
	def __str__(self):
		return self.polish_name

class Vertex (models.Model):
	vertex_id = models.CharField(max_length = 10, primary_key = True, default = 'VAAAAAAAAA')
	vertex_class = models.ForeignKey(Vertex_Class, on_delete = models.SET_NULL, null = True)
	preamble = models.ForeignKey(Preamble, on_delete = models.SET_DEFAULT, default = 'AAAAAAAAAA')
	user = models.ForeignKey(CustomUser, on_delete = models.CASCADE)
	discipline = models.ForeignKey(Discipline, on_delete = models.SET_NULL, null = True)
	subject = models.ForeignKey(Subject, on_delete = models.SET_NULL, null = True)
	date = models.DateTimeField(auto_now = True)
	title = models.CharField(max_length = 120, default = 'default title')
	shorttitle = models.CharField(max_length = 40, null = True, blank = True)
	submitted = models.BooleanField(default = False)
	desc_dir = models.CharField(max_length = 200, null = True)
	content_dir = models.CharField(max_length = 200, null = True)
	
	def __str__(self):
		return str(self.discipline) + ', ' + str(self.user) + ': ' + self.title
		
	class Meta:
		verbose_name_plural = "Vertices"
		
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
		return reverse('vertex', kwargs={'vertex_id': self.vertex_id})

	'''
	Note there are two desc and content dirs: 
	one pair pre-compilation and second after-compilation.
	As after-compilation are stored as fields, this two functions gets you the pre-compilation ones.
	'''
	def get_pre_content_dir(self):
		return os.path.join( self.user.folder, self.vertex_id + '.txt' )
		
	def get_pre_desc_dir(self):
		return os.path.join( self.user.folder, self.vertex_id + 'desc.txt' )
		
	def delete_pre_dirs(self):
		try:
			os.remove( self.get_pre_content_dir() )
		except FileNotFoundError:
			pass
		try:
			os.remove( self.get_pre_desc_dir() )
		except FileNotFoundError:
			pass
		
@receiver(models.signals.pre_delete, sender = Vertex)
def delete_vertex_files (sender, instance, using, **kwargs):
	instance.delete_pre_dirs()
	try:
		os.remove( instance.desc_dir )
	except FileNotFoundError:
		pass
	try:
		os.remove( instance.content_dir )
	except FileNotFoundError:
		pass
	
class Edge_Class (models.Model):
	polish_name = models.CharField(max_length = 60, default = 'Nienazwana krawędź')
	
	def __str__(self):
		return self.polish_name
		
	class Meta:
		verbose_name_plural = "Edge Classes"
		
	@classmethod
	def FIRST_TIME_RUN_ADD_DEFAULT_ECLASS(cls):
		default = Edge_Class( polish_name = 'Od wewnątrz do wewnątrz.' )
		default.save()
	
class Edge (models.Model):
	edge_id = models.CharField(max_length = 10, primary_key = True, default = 'EAAAAAAAAA')
	edge_class = models.ForeignKey(Edge_Class, on_delete = models.SET_NULL, null = True)
	preamble = models.ForeignKey(Preamble, on_delete = models.SET_DEFAULT, default = 'AAAAAAAAAA')
	user = models.ForeignKey(CustomUser, on_delete = models.SET_DEFAULT, default = 1)
	predecessor = models.ForeignKey(Vertex, on_delete = models.CASCADE, related_name='predecessor', null = True)
	successor = models.ForeignKey(Vertex, on_delete = models.CASCADE, related_name='successor', null = True)
	validated = models.BooleanField(default = False)
	directory = models.CharField(max_length = 200, null = True)
	links = models.CharField(max_length = 200, blank = True)
	
	def __str__(self):
		return self.edge_id
		
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
			
	def get_links(self):
		if self.links:
			return self.link
		return ''
	
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
			
class Path (models.Model):
	path_id = models.CharField(max_length = 10, primary_key = True, default = 'TAAAAAAAAA')
	user = models.ForeignKey(CustomUser, on_delete = models.CASCADE)
	name = models.CharField(max_length = 50, default = 'Nienazwana ścieżka')
	description = models.CharField(max_length = 200, null = True)
	date = models.DateField(auto_now = True)
	first = models.ForeignKey(Vertex, on_delete = models.SET_NULL, null = True)
	length = models.IntegerField(default = 0)
	
	def __str__(self):
		return self.name
	
	def read(self):
		return list( Path_Entry.objects.filter(path=self) )
	
	def read_verticies(self):
		return [entry.vertex for entry in self.read()]
		
	def get_first_str(self):
		if first:
			return str(self.first)
		else:
			return 'Pierwszy wierzchołek tej ścieżki został usunięty.'
		
	def get_first_url(self):
		if first:
			return self.first.get_url()
		else:
			return '#'
	
	def write_and_save(self, vertexes):
		for entry in Path_Entry.objects.filter(path=self):
			entry.delete() 
		self.first = vertexes[0]
		i = 0
		for V in vertexes:
			if V:
				i += 1
				E = Path_Entry()
				E.path = self
				E.index = i
				E.vertex = V
				E.save()
		self.length = i
		self.save()
			
	def write_at_end_and_save(self, Vert):
		if Vert:
			i = self.length + 1
			E = Path_Entry()
			E.path = self
			E.index = i
			E.vertex = Vert
			E.save()
			self.length = i
			self.save()
		
	def delete_one(self, ind):
		try:
			E = Path_Entry.objects.get(path = self, index = ind)
		except exceptions.ObjectDoesNotExist:
			return False
		else:
			after = Path_Entry.objects.filter(path = self, index__gt = ind).order_by('index')
			if len(after) > 0:
				if ind == 1:
					self.first = after[0].vertex
				for entry in after:
					entry.index = entry.index - 1
					entry.save()
			elif ind == 1:
				self.first = None
			self.length = self.length - 1
			self.save()
			E.delete()
			return True
	
class Path_Entry (models.Model):
	path = models.ForeignKey(Path, on_delete = models.CASCADE)
	index = models.IntegerField()
	vertex = models.ForeignKey(Vertex, on_delete = models.SET_NULL, null = True)
	
	class Meta:
		verbose_name_plural = "Path Entries"