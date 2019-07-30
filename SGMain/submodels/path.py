
from django.db import models
import django.core.exceptions as exceptions
from django.urls import reverse

from . import vertex as vertex_models
import users.models as user_model
import SGMain.tools as tools
			
class Path(models.Model):
	path_id = models.CharField(max_length = 10, primary_key = True, default = 'PAAAAAAAAA')
	user = models.ForeignKey(user_model.CustomUser, on_delete = models.CASCADE)
	name = models.CharField(max_length = 50, default = 'Nienazwana ścieżka')
	description = models.CharField(max_length = 200, blank = True)
	date = models.DateField(auto_now = True)
	first = models.ForeignKey(vertex_models.Vertex, on_delete = models.SET_NULL, null = True)
	length = models.IntegerField(default = 0)
	
	def __str__(self):
		return self.name
		
	@classmethod
	def new_id(cls):
		id = tools.id_generator('P')
		while len( cls.objects.filter(path_id = id) ):
			id = tools.id_generator('P')
		return id
			
	def get_url(self):
		return reverse('edit_path', kwargs={'path_id': self.path_id})
	
	def read(self):
		PEs = Path_Entry.objects.filter(path = self).order_by('index')
		i = 0
		for entry in PEs:
			i += 1
			if entry.index != i:
				raise Exception('Path error A')
			if not entry.vertex:
				raise Exception('Path error B')
		if self.length != i:
			raise Exception('Path error C')
		return PEs
	
	def read_verticies(self):
		return [entry.vertex for entry in self.read()]
		
	def get_first_str(self):
		if self.first:
			return str(self.first)
		else:
			return 'Pierwszy wierzchołek tej ścieżki jest niedostępny.'
		
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
		Path_Entry(
			path = self,
			index = where,
			vertex = vertex
			).save()
		self.length += 1
		self.save()
			
	def add_at_end_and_save(self, vertex):
		if not vertex:
			return
		self.length += 1
		Path_Entry(
			path = self,
			index = self.length,
			vertex = vertex
			).save()
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
		
	def delete_one(self, where):
		try:
			E = Path_Entry.objects.get(path = self, index = where)
		except exceptions.ObjectDoesNotExist:
			return False
		else:
			after = Path_Entry.objects.filter(path = self, index__gt = where).order_by('index')
			if len(after) > 0:
				if where == 1:
					self.first = after[0].vertex
				for entry in after:
					entry.index -= 1
					entry.save()
			elif where == 1:
				self.first = None
			self.length -= 1
			self.save()
			E.delete()
			return True
	
class Path_Entry(models.Model):
	path = models.ForeignKey(Path, on_delete = models.CASCADE)
	index = models.IntegerField()
	vertex = models.ForeignKey(vertex_models.Vertex, on_delete = models.SET_NULL, null = True)
	
	class Meta:
		verbose_name_plural = "Path Entries"