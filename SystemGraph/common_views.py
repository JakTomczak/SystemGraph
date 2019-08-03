import os

from django.shortcuts import render

import SGMain.models as model
from users.models import CustomUser
from SGMain import tasks

def frontpage(request):
	already = False
	if request.user.is_authenticated:
		verts = model.Vertex.objects.filter( user = request.user )
		if verts:
			already = True
	context = {
		'already': already,
		'Vertices': model.Vertex.get_submitted()
	}
	return render(request, 'common/frontpage.html', context)
	
def search_vertices(request):
	context = {
		'Vertices': model.Vertex.get_submitted()
	}
	return render(request, 'common/vertex_search.html', context)
	
def search_users(request):
	context = {
		'Users': CustomUser.objects.all()
	}
	return render(request, 'common/user_search.html', context)

'''
When you didn't change database, but changed base directory of this project,
call this function.
'''
def I_HAVE_CHANGED_BASEDIR ():
	for user in CustomUser.objects.all():
		user.folder = None
		user.get_folder(save = True)
	for P in model.Preamble.objects.all():
		P.directory = os.path.join( P.user.get_folder(), P.preamble_id + '.tex' )
		P.save()
	for V in model.Vertex.objects.all():
		V.content_dir = os.path.join( settings.COMP_DIR, V.vertex_id + '.txt' )
		if V.desc_dir:
			V.desc_dir = os.path.join( settings.COMP_DIR, V.vertex_id + 'desc.txt' )
		V.save()
	for E in model.Edge.objects.all():
		E.directory = os.path.join( settings.COMP_DIR, E.edge_id + '.txt' )
		E.save()
	A = model.Preamble.objects.get(preamble_id = 'AAAAAAAAAA')
	A.directory = os.path.join( settings.COMP_DIR, 'AAAAAAAAAA.tex' )
	A.save()
	B = model.Preamble.objects.get(preamble_id = 'AAAAAAAAAB')
	B.directory = os.path.join( settings.COMP_DIR, 'AAAAAAAAAB.tex' )
	B.save()
'''
When you run this project first time or you changed database without migrating records,
call this function ONCE.
'''
def I_HAVE_NEW_DATABASE():
	#I_GUESS_YOU_ARE_ADMIN = CustomUser.objects.get(username = 'YOUR_USERNAME')
	I_GUESS_YOU_ARE_ADMIN = CustomUser.objects.get(is_superuser = True)
	I_GUESS_YOU_ARE_ADMIN.get_folder()
	model.Preamble.FIRST_TIME_RUN_ADD_DEFAULT_PREAMBLES( I_GUESS_YOU_ARE_ADMIN )
	model.Vertex_Class.FIRST_TIME_RUN_ADD_DEFAULT_VCLASS()
	model.Discipline.FIRST_TIME_RUN_ADD_DEFAULT_DISCIPLINE()
	model.Vertex.FIRST_TIME_RUN_ADD_DEFAULT_VERTEX( I_GUESS_YOU_ARE_ADMIN )
	model.Edge_Class.FIRST_TIME_RUN_ADD_DEFAULT_ECLASS()
	i_want_math = True
	if i_want_math:
		FIRST_TIME_RUN_ADD_MATH_VCLASSES()
		
def FIRST_TIME_RUN_ADD_MATH_VCLASSES():
	mat = model.Discipline(polish_name = 'Matematyka')
	mat.save()
	top = model.Section(polish_name = 'Topologia', discipline = mat)
	top.save()
	model.Subject(polish_name = 'Podstawy topologii', section = top).save()
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