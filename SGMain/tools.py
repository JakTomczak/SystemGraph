import os
import string
import subprocess
import random
from datetime import datetime
from operator import itemgetter

from django.conf import settings

from . import models

def id_generator(letter, size = 9, chars = string.ascii_uppercase):
	if len(letter) != 1 or letter not in chars:
		raise Exception('Expected letter')
	return letter + ''.join(random.choice(chars) for _ in range(size))
	
def fcode_from_id(vertex_id = None, desc = False, edge_id = None):
	if vertex_id is None:
		if edge_id is None:
			return
		else:
			return edge_id
	else:
		if edge_id is None:
			if desc:
				return vertex_id + 'desc'
			else:
				return vertex_id
		else:
			return

def rreplace(s, old, new, occurrence):
	li = s.rsplit(old, occurrence)
	return new.join(li)

def userproposal(message):
	with open( os.path.join(settings.PROPOSALS_DIR, datetime.now().strftime('%Y %m %d godz %H.%M.%S') + '.txt'), 'w+' ) as file:
		file.write(message)

weights = {
	'initial': {
		0: 0.1, # not the same disciplines
		1: 1, # only the same discipline
		2: 3, # only the same section
		3: 6, # the same subject
	},
	'modifiers': {
		'the_same_author': 1.3,
	},
	'from_edge': {
		'outgoing': 1,
		'incoming': 0.7,
	},
	'edge_modifier': {
		'user_is_not_father': 0.7,
	}
}
seconds_in_thousand_years = 60*60*24*365*1000

class Displayer (object):
	
	def __init__(self, vertex):
		self.vertex = vertex
		self.user = vertex.user
		self.discipline = vertex.discipline
		self.section = vertex.section
		self.subject = vertex.subject
		self.big_queryset = models.Vertex.get_submitted().exclude(vertex_id = vertex.vertex_id)
		self.big_outgoing = models.Edge.objects.filter(predecessor = vertex).exclude(successor__isnull = True).exclude(successor = vertex)
		self.big_incoming = models.Edge.objects.filter(successor = vertex).exclude(predecessor = vertex)
	
	def run(self, vertex_class):
		self.queryset = self.big_queryset.filter(vertex_class = vertex_class)
		self.outgoing = self.big_outgoing.filter(successor__vertex_class = vertex_class)
		self.incoming = self.big_outgoing.filter(predecessor__vertex_class = vertex_class)
		if len(self.queryset) > 32:
			self.shrink_queryset()
		return self.prepare_to_show()
	
	'''
	Exclude all vertices of different discipline, which don't share edge with current vertex.
	'''
	def shrink_queryset(self):
		out_edges_qs = self.outgoing.filter(successor__discipline__ne = self.discipline)
		inc_edges_qs = self.incoming.filter(predecessor__discipline__ne = self.discipline)
		vertices_to_not_exclude = set()
		for edge in out_edges_qs:
			vertices_to_not_exclude.add(edge.successor)
		for edge in inc_edges_qs:
			vertices_to_not_exclude.add(edge.predecessor)
		vertices_of_the_same_discipline = set( self.queryset.filter(discipline = self.discipline) )
		vertices_filtered = vertices_of_the_same_discipline.union(vertices_to_not_exclude)
		if len(vertices_filtered) >= 16:
			self.queryset = vertices_filtered
	
	def prepare_to_show(self):
		output = []
		for vertex in self.queryset:
			weight = self._weight(vertex)
			vert_dict = {
				'vertex': vertex,
				'weight': weight,
				'description': vertex.get_description(),
				'title': vertex.shorttitle if vertex.shorttitle else vertex.title
			}
			output.append(vert_dict)
		return sorted( output, key = itemgetter('weight'), reverse = True )[:16]
	
	def _weight(self, vertex):
		init = int(vertex.discipline == self.discipline) + int(vertex.section == self.section) + int(vertex.subject == self.subject)
		weight = weights['initial'][init]
		if vertex.user == self.user:
			weight *= weights['modifiers']['the_same_author']
		for edge in self.outgoing.filter(successor = vertex):
			weight += self.edge_weight(edge, 'outgoing')
		for edge in self.incoming.filter(predecessor = vertex):
			weight += self.edge_weight(edge, 'incoming')
		seconds_between = (vertex.date - self.vertex.date).total_seconds()
		weight += seconds_between / seconds_in_thousand_years
		return weight
	
	def edge_weight(self, edge, type):
		eweight = weights['from_edge'][type]
		if edge.father != self.user:
			eweight *= weights['edge_modifier']['user_is_not_father']
		return eweight