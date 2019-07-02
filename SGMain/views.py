import os
import codecs

from django.shortcuts import render, redirect
from django.contrib import messages
import django.core.exceptions as exceptions

from . import models as model
from . import forms
from . import tools
from users.models import CustomUser

def new_vertex(request):
	if not request.user or request.user.is_anonymous:
		return render(request, 'errors/401.html')
	if request.method == 'POST':
		form = forms.Add_New_Vertex_Form(request.POST, user = request.user)
		if 'save' in request.POST and form.is_valid():
			vertex = form.save(commit = False)
			vertex.user = request.user
			vertex.vertex_id = model.Vertex.new_id()
			vertex.create_pre_dirs()
			vertex.save()
			messages.add_message(request, messages.SUCCESS, 'Nowy wierzchołek został dodany.')
			return redirect('edit_vertex', vertex_id = vertex.vertex_id)
	else:
		form = forms.Add_New_Vertex_Form(user = request.user)
	context = {'form': form}
	return render(request, 'graph/add_new_vertex.html', context)

def edit_vertex(request, vertex_id):
	try:
		this_vertex = model.Vertex.objects.get(vertex_id = vertex_id)
	except exceptions.ObjectDoesNotExist:
		return render(request, 'errors/404.html')
	if not request.user == this_vertex.user:
		return render(request, 'errors/403.html')
	successors = this_vertex.get_successors()
#	edges = [ {'edge': edge, 'edge_content': edge.content()} for edge in successors ]
	if request.method == 'POST':
		form = forms.Edit_Vertex_Form(request.POST, vertex = this_vertex)
		action = request.POST['action'].split(',')
		if 'save_all' in request.POST and form.is_valid():
			this_vertex.vertex_class = form.cleaned_data['vertex_class']
			this_vertex.preamble = form.cleaned_data['preamble']
			this_vertex.discipline = form.cleaned_data['discipline']
			this_vertex.subject = form.cleaned_data['subject']
			this_vertex.title = form.cleaned_data['title']
			this_vertex.shorttitle = form.cleaned_data['shorttitle']
			this_vertex.save()
			this_vertex.save_pre_content( form.cleaned_data['content'] )
			this_vertex.save_pre_desc( form.cleaned_data['description'] )
			messages.add_message(request, messages.SUCCESS, "Właściwości wierzchołka zostały zapisane.")
		elif 'delete' in action:
			user = this_vertex.user
			this_vertex.delete()
			messages.add_message(request, messages.SUCCESS, 'Wierzchołek został usunięty.')
			return redirect('profile', username = user.username)
		elif 'newedge' in request.POST:
			request.session['pred'] = this_vertex.vertex_id
			return redirect('new_edge')
	else:
		form = forms.Edit_Vertex_Form(vertex = this_vertex)
	context = {'form': form, 'vid': this_vertex.vertex_id, 'submitted': this_vertex.submitted, 'successors': successors}
	return render(request, 'graph/edit_vertex.html', context)

def view_vertex(request, vertex_id): # Needs big enhancements
	try:
		this_vertex = model.Vertex.objects.get(vertex_id = vertex_id, submitted = True)
	except exceptions.ObjectDoesNotExist:
		return render(request, 'errors/404.html')
	edges = this_vertex.get_successors()
	with codecs.open( this_vertex.content_dir, 'r', encoding = 'utf-8') as file:
		content = file.read()
	sglinks = []
	for e in edges:
		if e.links:
			cont = e.get_true_content()
			cont = cont.replace('\n', '')
			cont = cont.replace('\r', '')
			links = e.links.split(',')
			for link in links:
				sglinks.append( {'id': link, 'content': cont, 'successor_id': e.get_successor_id()} )
	(bolist, lelist, rilist, tolist) = tools.four_directions(this_vertex)
	if request.user == this_vertex.user:
		thisuser = True
	else:
		thisuser = False
	context = {'float': 1, 'edges': sglinks, 'thisuser': thisuser, 'thisvertex': this_vertex, 'thisvertexcontent': content, 'bottom': bolist, 'left': lelist, 'right': rilist, 'top': tolist}
	return render(request, 'graph/view_vertex.html', context)

def new_discipline(request):
	if not request.user or request.user.is_anonymous:
		return render(request, 'errors/401.html')
	if request.method == 'POST':
		form = forms.Add_New_Discipline_Form(request.POST)
		if 'save' in request.POST and form.is_valid():
			form.save()
			messages.add_message(request, messages.SUCCESS, 'Nowa dyscyplina została dodana.')
			return redirect('profile', username = request.user.username)
	else:
		form = forms.Add_New_Discipline_Form()
	context = {'form': form}
	return render(request, 'graph/add_new_discipline.html', context)

def new_subject(request):
	if not request.user or request.user.is_anonymous:
		return render(request, 'errors/401.html')
	if request.method == 'POST':
		form = forms.Add_New_Subject_Form(request.POST)
		if 'save' in request.POST and form.is_valid():
			form.save()
			messages.add_message(request, messages.SUCCESS, 'Nowy temat został dodany.')
			return redirect('profile', username = request.user.username)
	else:
		form = forms.Add_New_Subject_Form()
	context = {'form': form}
	return render(request, 'graph/add_new_subject.html', context)

def new_preamble(request):
	if not request.user or request.user.is_anonymous:
		return render(request, 'errors/401.html')
	if request.method == 'POST':
		form = forms.Add_New_Preamble_Form(request.POST)
		if form.is_valid():
			preamble = form.save(commit = False)
			preamble.user = request.user
			preamble.preamble_id = model.Preamble.new_id()
			preamble.create_content_dir( form.cleaned_data['content'] )
			preamble.save()
			messages.add_message(request, messages.SUCCESS, 'Nowa preambuła została dodana.')
			return redirect('profile', username = request.user.username)
	else:
		form = forms.Add_New_Preamble_Form()
	context = {'form': form}
	return render(request, 'graph/add_new_preamble.html', context)

def edit_preamble(request, preamble_id):
	try:
		this_preamble = model.Preamble.objects.get(preamble_id = preamble_id)
	except exceptions.ObjectDoesNotExist:
		return render(request, 'errors/404.html')
	if not request.user == this_preamble.user:
		return render(request, 'errors/403.html')
	if request.method == 'POST':
		form = forms.Edit_Preamble_Form(request.POST, preamble = this_preamble)
		action = request.POST['action'].split(',')
		if 'save' in request.POST and form.is_valid():
			this_preamble.title = form.cleaned_data['title']
			this_preamble.description = form.cleaned_data['description']
			this_preamble.write( form.cleaned_data['content'] )
			this_preamble.save()
			messages.add_message(request, messages.SUCCESS, 'Zmiany w preambule zostały zapisane.')
		if 'delete' in action:
			this_preamble.delete()
			messages.add_message(request, messages.SUCCESS, 'Preambuła została usunięta.')
			return redirect('profile', username = request.user.username)
	else:
		form = forms.Edit_Preamble_Form(preamble = this_preamble)
	context = {'form': form}
	return render(request, 'graph/edit_preamble.html', context)

def new_vertex_class(request):
	if not request.user or request.user.is_anonymous:
		return render(request, 'errors/401.html')
	if request.method == 'POST':
		form = forms.Add_New_Vertex_Class_Form(request.POST)
		if 'save' in request.POST and form.is_valid():
			model.Vertex_Class.make_proposal(request.user, form)
			messages.add_message(request, messages.SUCCESS, 'Wniosek został wysłany.')
			return redirect('profile', username = request.user.username)
	else:
		form = forms.Add_New_Vertex_Class_Form()
	context = {'form': form}
	return render(request, 'graph/add_new_vertex_class.html', context)

def new_path(request):
	return render(request, 'graph/add_new_path.html', context)