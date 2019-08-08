import os
import codecs
import datetime

from django.db import models
from django.conf import settings
import django.core.exceptions as exceptions
from django.urls import reverse
import django.utils.timezone as timezone

from . import vertex as vertex_models
import users.models as user_model
import SGMain.tools as tools
	
class Edge_Class(models.Model):
	code = models.CharField(max_length = 10, default = 'Unknown')
	polish_name = models.CharField(max_length = 60, default = 'Nienazwana krawędź')
		
	class Meta:
		verbose_name_plural = "Edge Classes"
	
	def __str__(self):
		return self.polish_name
		
	@classmethod
	def FIRST_TIME_RUN_ADD_ECLASSES(cls):
		Edge_Class(code = 'simple', polish_name = 'Prosta').save()
	
class Edge(models.Model):
	edge_id = models.CharField(max_length = 10, primary_key = True, default = 'EAAAAAAAAA')
	edge_class = models.ForeignKey(Edge_Class, on_delete = models.SET_NULL, null = True)
	preamble = models.ForeignKey(vertex_models.Preamble, on_delete = models.SET_DEFAULT, default = settings.DEFAULT_PREAMBLE_ID)
	user = models.ForeignKey(user_model.CustomUser, on_delete = models.SET_DEFAULT, default = 1)
	predecessor = models.ForeignKey(vertex_models.Vertex, on_delete = models.CASCADE, related_name='predecessor', null = True)
	successor = models.ForeignKey(vertex_models.Vertex, on_delete = models.CASCADE, related_name='successor', null = True)
	directory = models.CharField(max_length = 200, null = True)
	frozen = models.BooleanField(default = False)
	
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
				return self.successor.description().replace('\n', '').replace('\r', '')
			else:
				return ''
		else:
			t = f.read()
			f.close()
			return t.replace('\n', '').replace('\r', '')
			
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
		
	@classmethod
	def sglink(cls, edge_id, number):
		link_id = edge_id + '_' + number
		edge = Edge.objects.get(edge_id = edge_id)
		return {
			'id': link_id,
			'content': edge.get_true_content(),
			'succ_url': edge.get_successor_url()
		}

'''
There should be edges between vertices.
But no one should be able to just add edge to other user's vertex.
Therefore division to internal and external edges is needed.
Moreover third party user can propose edge between any to vertices.
'''
int_ok = 'Int-ok' # Simple internal, nothing to accept
ext_post = 'Ext-post' # External after acceptation
ext_pre = 'Ext-pre' # External before acceptation
inc = 'Incoming' # External proposition, but successor acceptation is already gotten
int_prop = 'Int-prop' # Internal proposition
ext_prop = 'Ext-prop' # External proposition

specifics = {
	'accept_functions': {
		ext_pre: 'accept_external',
		inc: 'accept_incoming',
		int_prop: 'accept_in_proposition',
		ext_prop: 'accept_ex_proposition',
	},
}

maxproposals = 14
maxrejectionsin24hours = 3
maxproposalsin10minutes = 6
			
class Edge_Proposition(models.Model):
	prop_id = models.CharField(max_length = 10, primary_key = True, default = 'RAAAAAAAAA')
	code = models.CharField(max_length = 10, default = 'Unknown')
	father = models.ForeignKey(user_model.CustomUser, on_delete = models.CASCADE)
	predecessor = models.ForeignKey(vertex_models.Vertex, on_delete = models.CASCADE, related_name='prop_predecessor')
	successor = models.ForeignKey(vertex_models.Vertex, on_delete = models.CASCADE, related_name='prop_successor')
	time = models.DateTimeField(auto_now_add = True)
	rejected = models.BooleanField(default = False)
	accepted = models.BooleanField(default = False)
	
	@classmethod
	def new_id(cls):
		id = tools.id_generator('R')
		while len( cls.objects.filter(prop_id = id) ):
			id = tools.id_generator('R')
		return id
		
	@classmethod
	def get_user_propositions(cls, user):
		from_pred = Edge_Proposition.objects.filter(predecessor__user = user, rejected = False, accepted = False)
		from_succ = Edge_Proposition.objects.filter(successor__user = user, rejected = False, accepted = False)
		one = from_succ.filter(code = ext_pre)
		two = from_pred.filter(code = inc)
		three = from_pred.filter(code = int_prop)
		four = from_pred.filter(code = ext_prop)
		return one | two | three | four
	
	@classmethod
	def check_if_can(cls, father, predecessor, successor):
		try:
			Edge.objects.get(predecessor = predecessor, successor = successor)
		except exceptions.ObjectDoesNotExist:
			pass
		else:
			return False, 'Taka krawędź juź istnieje.'
		props = Edge_Proposition.objects.filter(father = father)
		try:
			props.get(predecessor = predecessor, successor = successor)
		except exceptions.ObjectDoesNotExist:
			pass
		else:
			return False, 'Już złożyłeś taką propozycję krawędzi.'
		if len( props.filter(rejected = False, accepted = False) ) >= maxproposals:
			return False, 'Na raz możesz mieć jedynie {} otwartych propozycji krawędzi.'.format(maxproposals)
		minutes_ago = timezone.now() - datetime.timedelta(minutes = 10)
		if len( props.filter(time__gte = minutes_ago) ) >= maxproposalsin10minutes:
			return False, 'Zbyt szybko dodajesz kolejne propozycje krawędzi. Zaczekaj chwilę.'
		hours_ago = timezone.now() - datetime.timedelta(hours = 24)
		if len( props.filter(rejected = True, time__gte = hours_ago) ) >= maxrejectionsin24hours:
			return False, 'Twoje ostatnie krawędzie były często odrzucane. Ze względów bezpieczeństwa nie możesz proponować więcej krawędzi dzisiaj. Spróbuj jutro.'
		return True, ''
	
	@classmethod
	def make(cls, father, predecessor, successor):
		ok, message = Edge_Proposition.check_if_can(father, predecessor, successor)
		if not ok:
			return None, message
		if father == predecessor.user:
			code = ext_pre
		else:
			if father == successor.user:
				code = inc
			else:
				if predecessor.user == successor.user:
					code = int_prop
				else:
					code = ext_prop
		Pr = Edge_Proposition(
			prop_id = Edge_Proposition.new_id(),
			code = code,
			father = father,
			predecessor = predecessor,
			successor = successor
		)
		Pr.save()
		return Pr, None
	
	def get_validation_user(self):
		if self.code == ext_pre:
			return self.successor.user
		return self.predecessor.user
		
	def reject(self):
		self.rejected = True
		self.save()
		user_model.Messages.add_user_rejected_your_edge_proposal(self)
	
	def accept(self):
		func = getattr( self, specifics['accept_functions'][self.code] )
		func()
		user_model.Messages.add_user_accepted_your_edge_proposal(self)
		self.accepted = True
		self.save()
		
	def accept_external(self):
		self._new_edge(True)
		
	def accept_incoming(self):
		self._new_edge(True)
		
	def accept_ex_proposition(self):
		self._new_edge_prop()
		
	def accept_in_proposition(self):
		self._new_edge(False)
		
	def _new_edge(self, frozen):
		Edge(
			edge_id = Edge.new_id(),
			user = self.predecessor.user,
			predecessor = self.predecessor,
			successor = self.successor,
			frozen = frozen
		).save()
		
	def _new_edge_prop(self):
		Edge_Proposition(
			prop_id = Edge_Proposition.new_id(),
			father = self.predecessor.user,
			predecessor = self.predecessor,
			successor = self.successor,
			code = ext_pre
		).save()
	
	def only_show(self):
		if self.code == ext_pre:
			return True
		return False