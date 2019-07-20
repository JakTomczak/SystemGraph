# -*- coding: utf-8 -*-
import string
import subprocess
import random
from operator import itemgetter

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
		
def weighting (thevertex, queryset):
	default_weight = 1
	the_same_author_modifier = 1.3
	not_the_same_discipline_modifier = 0.01
	the_same_subject_modifier = 1.4
	outgoing_edge_weight = 1
	incoming_edge_weight = 0.6
	not_the_same_author_of_edge_modifier = 0.8
	no_edges_modifier = 0.2
	seconds_in_ten_thousand_years = 60*60*24*365*10000
	li = []
	for vert in queryset:
		weight = default_weight
		
		if vert.user == thevertex.user:
			weight *= the_same_author_modifier
			
		if vert.discipline != thevertex.discipline:
			weight *= not_the_same_discipline_modifier
			
		if vert.subject == thevertex.subject:
			weight *= the_same_subject_modifier
		
		from_edges_modifier = 0
		edges = SGmodels.Edge.objects.filter( predecessor = thevertex, successor = vert )
		for edge in edges:
			if edge.user == thevertex.user:
				from_edges_modifier += outgoing_edge_weight
			else:
				from_edges_modifier += outgoing_edge_weight * not_the_same_author_of_edge_modifier
		edges = SGmodels.Edge.objects.filter( predecessor = vert, successor = thevertex )
		for edge in edges:
			if edge.user == thevertex.user:
				from_edges_modifier += incoming_edge_weight
			else:
				from_edges_modifier += incoming_edge_weight * not_the_same_author_of_edge_modifier
		if from_edges_modifier == 0:
			weight *= no_edges_modifier
		elif from_edges_modifier < 1:
			pass
		else:
			weight *= from_edges_modifier
			
		seconds_between = (vert.date - thevertex.date).total_seconds()
		weight += seconds_between / seconds_in_ten_thousand_years
			
		# li.append( {'vert': vert, 'weight': weight, 'vdesc': vert.description()} )
		vtitle = vert.shorttitle if vert.shorttitle else vert.title
		li.append( {'vert': vert, 'weight': weight, 'vdesc': vert.description(), 'vtitle': vtitle} )
			
	return li
		
def four_directions (vertex):
	bottom = models.Vertex.objects.filter( vertex_class = vertex.vertex_class.bottom ).exclude( vertex_id = vertex.vertex_id )
	bolist = weighting (vertex, bottom)
	bolist = sorted( bolist, key = itemgetter('weight'), reverse = True )
	left = models.Vertex.objects.filter( vertex_class = vertex.vertex_class.left ).exclude( vertex_id = vertex.vertex_id )
	lelist = weighting (vertex, left)
	lelist = sorted( lelist, key = itemgetter('weight'), reverse = True )
	right = models.Vertex.objects.filter( vertex_class = vertex.vertex_class.right ).exclude( vertex_id = vertex.vertex_id )
	rilist = weighting (vertex, right)
	rilist = sorted( rilist, key = itemgetter('weight'), reverse = True )
	top = models.Vertex.objects.filter( vertex_class = vertex.vertex_class.top ).exclude( vertex_id = vertex.vertex_id )
	tolist = weighting (vertex, top)
	tolist = sorted( tolist, key = itemgetter('weight'), reverse = True )#[:4]
	return (bolist[:4], lelist[:4], rilist[:4], tolist[:4])