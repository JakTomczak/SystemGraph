
import datetime
import os
import codecs

from django.db import models
from django.conf import settings
from django.dispatch import receiver
import django.core.exceptions as exceptions
from django.urls import reverse

from users.models import CustomUser
import SGMain.tools as tools
	
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
	def make_proposal(cls, user, form):
		message = str(datetime.datetime.now()) + '\n'
		message += 'user: ' + user.username + '\n'
		message += 'polska pojedyncza: ' + form.cleaned_data['polish_name'] + '\n'
		message += 'polska mnoga: ' + form.cleaned_data['polish_name_plural'] + '\n'
#		message += 'angielska pojedyncza: ' + form.cleaned_data['english_name'] + '\n'
#		message += 'angielska mnoga: ' + form.cleaned_data['english_name_plural'] + '\n'
		message += 'top: ' + form.cleaned_data['top'] + '\n'
		message += 'left: ' + form.cleaned_data['left'] + '\n'
		message += 'right: ' + form.cleaned_data['right'] + '\n'
		message += 'bottom: ' + form.cleaned_data['bottom'] + '\n'
		message += 'info: \n' + form.cleaned_data['info']
		with open( os.path.join(settings.PROPOSALS_DIR, datetime.datetime.now().strftime('%Y %m %d godz %H.%M.%S') + '.txt'), 'w+' ) as file:
			file.write(message)
		
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
class Preamble (models.Model):
	preamble_id = models.CharField(max_length = 10, primary_key = True, default = 'AAAAAAAAAA')
	user = models.ForeignKey(CustomUser, on_delete = models.CASCADE)
	title = models.CharField(max_length = 60, default = 'My preamble')
	description = models.CharField(max_length = 200, null = True)
	directory = models.CharField(max_length = 200, default = os.path.join( settings.COMP_DIR, 'AAAAAAAAAA.txt' ))
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
		
	def create_content_dir(self, content = ''):
		self.directory = os.path.join( self.user.get_folder(), self.preamble_id + '.tex' )
		if content:
			self.write(content)
		else:
			open( self.directory, 'w+').close()
		
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
#			return Preamble.objects.filter(user = user) | Preamble.objects.filter(preamble_id = 'AAAAAAAAAA') | Preamble.objects.filter(preamble_id = 'AAAAAAAAAB')
			return Preamble.objects.filter(user = user) | Preamble.objects.filter(is_default = True)
		else:
#			return Preamble.objects.filter(preamble_id = 'AAAAAAAAAA') | Preamble.objects.filter(preamble_id = 'AAAAAAAAAB')
			return Preamble.objects.filter(is_default = True)
	
	@classmethod
	def FIRST_TIME_RUN_ADD_DEFAULT_PREAMBLES(cls, admin):
		A = Preamble(preamble_id = 'AAAAAAAAAA', user = admin, is_default = True)
		A.title = 'Default preamble'
		A.desciption = 'It works with english planar text and math formulas.'
		A.save()
		B = Preamble(preamble_id = 'AAAAAAAAAB', user = admin, is_default = True)
		B.directory = os.path.join( settings.COMP_DIR, 'AAAAAAAAAB.txt' )
		B.title = 'Domyślna preambuła'
		B.desciption = 'Działa z tekstem polskim i matematycznymi formułami.'
		B.save()

@receiver(models.signals.pre_delete, sender = Preamble)
def delete_preamble_files (sender, instance, using, **kwargs):
	os.remove(instance.directory)
	
class Discipline (models.Model):
	polish_name = models.CharField(max_length = 60, default = 'Nienazwana dyscyplina')
	is_default = models.BooleanField(default = False)
	
	def __str__(self):
		return self.polish_name
	
	@classmethod
	def FIRST_TIME_RUN_ADD_DEFAULT_DISCIPLINE(cls):
		Discipline(polish_name = 'Brak dyscypliny', is_default = True).save()
		
class Subject (models.Model):
	polish_name = models.CharField(max_length = 60, default = 'Nienazwany temat')
	is_default = models.BooleanField(default = False)
	
	def __str__(self):
		return self.polish_name
	
	@classmethod
	def FIRST_TIME_RUN_ADD_DEFAULT_SUBJECT(cls):
		Subject(polish_name = 'Brak tematu', is_default = True).save()

class Vertex (models.Model):
	vertex_id = models.CharField(max_length = 10, primary_key = True, default = 'VAAAAAAAAA')
	vertex_class = models.ForeignKey(Vertex_Class, on_delete = models.SET_DEFAULT, default = 1)
	preamble = models.ForeignKey(Preamble, on_delete = models.SET_DEFAULT, default = 'AAAAAAAAAA')
	user = models.ForeignKey(CustomUser, on_delete = models.CASCADE)
	discipline = models.ForeignKey(Discipline, on_delete = models.SET_DEFAULT, default = 1)
	subject = models.ForeignKey(Subject, on_delete = models.SET_DEFAULT, default = 1)
	date = models.DateTimeField(auto_now = True)
	title = models.CharField(max_length = 120, default = 'default title')
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
		return Edge.objects.filter(predecessor = self)

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
	
	# More then one default Vertex is forbidden in this project.
	@classmethod
	def get_default(cls):
		try:
			return Vertex.objects.get(is_default = True)
		except exceptions.ObjectDoesNotExist:
			return Vertex.objects.all()[0]
		
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
	PEs = Path_Entry.objects.filter(vertex = instance)
	for entry in PEs:
		path = entry.path
		next_ones = Path_Entry.objects.filter(path = path, index__gt = entry.index)
		for e in next_ones:
			e.index -= 1
			e.save()
		path.length -= 1
		entry.delete()
		if path.length < 1:
			path.delete()
		else:
			path.save()
	for path in Path.objects.filter(first = instance):
		path.first = Path_Entry.objects.filter(path = path, index = 1)[0].vertex
		path.save()
	
class Edge_Class (models.Model):
	polish_name = models.CharField(max_length = 60, default = 'Nienazwana krawędź')
		
	class Meta:
		verbose_name_plural = "Edge Classes"
	
	def __str__(self):
		return self.polish_name
		
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
		
	def create_pre_dirs(self):
		codecs.open( self.get_pre_dir(), 'w', encoding = 'utf-8').close()
		
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
		
@receiver(models.signals.pre_delete, sender = Edge)
def delete_vertex_files (sender, instance, using, **kwargs):
	instance.delete_pre_dir()
	try:
		os.remove( instance.directory )
	except (TypeError, FileNotFoundError):
		pass
			
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
		
	@classmethod
	def new_id(cls):
		id = tools.id_generator('P')
		while len( cls.objects.filter(path_id = id) ):
			id = tools.id_generator('P')
		return id
	
	def read(self):
		PEs = Path_Entry.objects.filter(path = self).order_by('index')
		i = 0
		for entry in PEs:
			i += 1
			if entry.index != i:
				raise Exception('Path error')
			if not entry.vertex:
				raise Exception('Path error')
		if self.length != i:
			raise Exception('Path error')
		return PEs
	
	def read_verticies(self):
		return [entry.vertex for entry in self.read()]
		
	def get_first_str(self):
		if self.first:
			return str(self.first)
		else:
			return 'Pierwszy wierzchołek tej ścieżki został usunięty.'
		
	def get_first_url(self):
		if self.first:
			return self.first.get_url()
		else:
			return '#'
	
	def write_and_save(self, vertexes):
		for entry in Path_Entry.objects.filter(path = self):
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
		
	def add_here_and_save(self, where, vertex):
		if not vertex:
			return
		if where > self.length:
			self.add_at_end_and_save(vertex)
			return
		if where <= 1:
			self.first = vertex
			where = 1
		for entry in Path_Entry.objects.filter(path = self, index__gte = where):
			entry.index += 1
			entry.save()
		E = Path_Entry(
			path = self,
			index = where,
			vertex = vertex
			)
		E.save()
		self.length += 1
		self.save()
			
	def add_at_end_and_save(self, vertex):
		if not vertex:
			return
		E = Path_Entry()
		E.path = self
		self.length += 1
		E.index = self.length
		E.vertex = vertex
		E.save()
		self.save()
		
	def change_this_one_and_save(self, where, to_which):
		if where < 1 or where > self.length:
			return
		E = Path_Entry.objects.get(path = self, index = where)
		E.vertex = to_which
		E.save()
		if where == 1:
			self.first = to_which
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
					entry.index -= 1
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