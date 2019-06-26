import os

from django.shortcuts import render

import SGMain.models as model
from users.models import CustomUser

def frontpage(request):
	return render(request, 'common/frontpage.html', {})
	
def profile(request, username):
	return render(request, 'common/profile_thisuser.html', {})
	
def SearchSite(request):
	return render(request, 'common/search_vertexes.html', {})

'''
When you didn't change database, but changed base directory of this project,
call this function ONCE.
'''
def I_HAVE_CHANGED_BASEDIR ():
	Users = CustomUser.objects.all()
	for user in Users:
		user.folder = None
		user.get_folder()
		user.save()
	Prems = model.Preamble.objects.all()
	for P in Prems:
		P.directory = os.path.join( P.user.folder, P.preamble_id + '.tex' )
		P.save()
	Verts = model.Vertex.objects.all()
	for V in Verts:
		V.content_dir = os.path.join( settings.PUF_DIR, V.vertex_id + '.txt' )
		if V.desc_dir:
			V.desc_dir = os.path.join( settings.PUF_DIR, V.vertex_id + 'desc.txt' )
		V.save()
	Edges = model.Edge.objects.all()
	for E in Edges:
		E.directory = os.path.join( settings.PUF_DIR, E.edge_id + '.txt' )
		E.save()
	A = model.Preamble.objects.get(preamble_id = 'AAAAAAAAAA')
	A.directory = os.path.join( settings.BASE_DIR, 'static', 'AAAAAAAAAA.tex' )
	A.save()
	B = model.Preamble.objects.get(preamble_id = 'AAAAAAAAAB')
	B.directory = os.path.join( settings.BASE_DIR, 'static', 'AAAAAAAAAB.tex' )
	B.save()
'''
When you run this project first time or you changed database without migrating records,
call this function ONCE.
'''
def I_HAVE_NEW_DATABASE():
	#I_GUESS_YOU_ARE_ADMIN = CustomUser.objects.get(username = 'YOUR_USERNAME')
	I_GUESS_YOU_ARE_ADMIN = CustomUser.objects.get(is_superuser = True)
	model.Preamble.FIRST_TIME_RUN_ADD_DEFAULT_PREAMBLES( I_GUESS_YOU_ARE_ADMIN )
	model.Vertex_Class.FIRST_TIME_RUN_ADD_DEFAULT_VCLASS()
	model.Edge_Class.FIRST_TIME_RUN_ADD_DEFAULT_ECLASS()
	i_want_math = True
	if i_want_math:
		FIRST_TIME_RUN_ADD_MATH_VCLASSES()
		
def FIRST_TIME_RUN_ADD_MATH_VCLASSES():
	definition = model.Vertex_Class( polish_name = 'Definicja', polish_name_plural = 'Definicje' )
	definition.save()
	example = model.Vertex_Class( polish_name = 'Przykład', polish_name_plural = 'Przykłady' )
	example.bottom = definition
	example.save()
	theorem = model.Vertex_Class( polish_name = 'Twierdzenie', polish_name_plural = 'Twierdzenia' )
	theorem.bottom = definition
	theorem.top = example
	theorem.save()
	proof = model.Vertex_Class( polish_name = 'Dowód', polish_name_plural = 'Dowody' )
	proof.bottom = definition
	proof.top = example
	proof.right = theorem
	proof.save()
	note = model.Vertex_Class( polish_name = 'Uwaga', polish_name_plural = 'Uwagi' )
	note.bottom = definition
	note.top = example
	note.right = theorem
	note.save()
	note.left = note
	note.save()
	definition.bottom = definition
	definition.left = note
	definition.right = theorem
	definition.top = example
	definition.save()
	example.left = note
	example.right = theorem
	example.top = example
	example.save()
	theorem.left = note
	theorem.right = proof
	theorem.save()
	proof.left = note
	proof.save()