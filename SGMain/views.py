import os
import codecs

from django.shortcuts import render, redirect
from django.contrib import messages
import django.core.exceptions as exceptions

from . import models as model
from . import forms
from . import tools
from users.models import CustomUser

def new_discipline(request):
	if not request.user or request.user.is_anonymous:
		return render(request, 'errors/401.html')
	if request.method == 'POST':
		form = forms.Discipline_Form(request.POST)
		if 'save' in request.POST and form.is_valid():
			form.save()
			messages.add_message(request, messages.SUCCESS, 'Nowa dyscyplina została dodana.')
			return redirect('all_disciplines')
	else:
		form = forms.Discipline_Form(initial={'polish_name': ''})
	context = {'form': form}
	return render(request, 'graph/add_new_discipline.html', context)

def new_section(request, parent_pk):
	try:
		discipline = model.Discipline.objects.get(pk = parent_pk)
	except exceptions.ObjectDoesNotExist:
		if parent_pk != 1:
			return redirect('new_section', parent_pk = 1)
		else:
			return render(request, 'errors/404.html')
	if not request.user or request.user.is_anonymous:
		return render(request, 'errors/401.html')
	if request.method == 'POST':
		form = forms.Section_Form(request.POST)
		if 'save' in request.POST and form.is_valid():
			section = form.save(commit = False)
			section.discipline = discipline
			section.save()
			messages.add_message(request, messages.SUCCESS, 'Nowy dział został dodany.')
			return redirect('view_discipline', pk = parent_pk)
	else:
		form = forms.Section_Form(initial={'polish_name': ''})
	context = {
		'this_discipline': discipline,
		'form': form,
	}
	return render(request, 'graph/add_new_section.html', context)

def new_subject(request, parent_pk):
	try:
		section = model.Section.objects.get(pk = parent_pk)
	except exceptions.ObjectDoesNotExist:
		if parent_pk != 1:
			return redirect('new_subject', parent_pk = 1)
		else:
			return render(request, 'errors/404.html')
	if not request.user or request.user.is_anonymous:
		return render(request, 'errors/401.html')
	if request.method == 'POST':
		form = forms.Subject_Form(request.POST)
		if 'save' in request.POST and form.is_valid():
			subject = form.save(commit = False)
			subject.section = section
			subject.discipline = section.discipline
			subject.save()
			messages.add_message(request, messages.SUCCESS, 'Nowy temat został dodany.')
			return redirect('view_section', pk = parent_pk)
	else:
		form = forms.Subject_Form(initial={'polish_name': ''})
	context = {
		'this_section': section,
		'form': form,
	}
	return render(request, 'graph/add_new_subject.html', context)

def all_disciplines(request):
	context = {
		'disciplines': model.Discipline.objects.all(), 
	}
	return render(request, 'graph/all_disciplines.html', context)

def view_discipline(request, pk):
	try:
		discipline = model.Discipline.objects.get(pk = pk)
	except exceptions.ObjectDoesNotExist:
		return render(request, 'errors/404.html')
	context = {
		'this_discipline': discipline, 
		'sections': model.Section.objects.filter(discipline = discipline),
	}
	return render(request, 'graph/view_discipline.html', context)

def view_section(request, pk):
	try:
		section = model.Section.objects.get(pk = pk)
	except exceptions.ObjectDoesNotExist:
		return render(request, 'errors/404.html')
	context = {
		'this_section': section, 
		'subjects': model.Subject.objects.filter(section = section),
	}
	return render(request, 'graph/view_section.html', context)

def view_subject(request, pk):
	try:
		subject = model.Subject.objects.get(pk = pk)
	except exceptions.ObjectDoesNotExist:
		return render(request, 'errors/404.html')
	context = {
		'this_subject': subject, 
		'vertices': model.Vertex.objects.filter(subject = subject),
	}
	return render(request, 'graph/view_subject.html', context)

def edit_discipline(request, pk):
	try:
		discipline = model.Discipline.objects.get(pk = pk)
	except exceptions.ObjectDoesNotExist:
		return render(request, 'errors/404.html')
	if not request.user or request.user.is_anonymous:
		return render(request, 'errors/401.html')
	user = request.user
	can_delete, can_edit = discipline.perms(user)
	if request.method == 'POST':
		form = forms.Discipline_Form(request.POST, instance = discipline)
		action = request.POST['action'].split(',')
		if 'delete' in request.POST:
			discipline.delete()
			messages.add_message(request, messages.SUCCESS, 'Dyscyplina została usunięta.')
			return redirect('all_disciplines')
		elif 'save' in request.POST and form.is_valid():
			form.save()
			messages.add_message(request, messages.SUCCESS, 'Zmiany w dyscyplinie zostały zapisane.')
			return redirect('all_disciplines')
		elif 'prop_delete' in action:
			discipline.propose_deletion(user)
			messages.add_message(request, messages.SUCCESS, 'Wniosek został wysłany.')
			return redirect('all_disciplines')
		elif 'prop_change' in action and form.is_valid():
			discipline.propose_change(user, form.cleaned_data)
			messages.add_message(request, messages.SUCCESS, 'Wniosek został wysłany.')
			return redirect('all_disciplines')
	else:
		form = forms.Discipline_Form(instance = discipline)
	context = {
		'this_pk': pk,
		'form': form,
		'delete': can_delete,
		'edit': can_edit,
	}
	return render(request, 'graph/edit_discipline.html', context)

def edit_section(request, pk):
	try:
		section = model.Section.objects.get(pk = pk)
	except exceptions.ObjectDoesNotExist:
		return render(request, 'errors/404.html')
	if not request.user or request.user.is_anonymous:
		return render(request, 'errors/401.html')
	user = request.user
	can_delete, can_edit = section.perms(user)
	if request.method == 'POST':
		form = forms.Section_Form(request.POST, instance = section)
		action = request.POST['action'].split(',')
		if 'delete' in request.POST:
			dpk = section.discipline.pk
			section.delete()
			messages.add_message(request, messages.SUCCESS, 'Dział został usunięty.')
			return redirect('view_discipline', pk = dpk)
		elif 'save' in request.POST and form.is_valid():
			form.save()
			messages.add_message(request, messages.SUCCESS, 'Zmiany w dziale zostały zapisane.')
			return redirect('view_discipline', pk = section.discipline.pk)
		elif 'prop_delete' in action:
			section.propose_deletion(user)
			messages.add_message(request, messages.SUCCESS, 'Wniosek został wysłany.')
			return redirect('view_discipline', pk = section.discipline.pk)
		elif 'prop_change' in action and form.is_valid():
			section.propose_change(user, form.cleaned_data)
			messages.add_message(request, messages.SUCCESS, 'Wniosek został wysłany.')
			return redirect('view_discipline', pk = section.discipline.pk)
	else:
		form = forms.Section_Form(instance = section)
	context = {
		'this_section': section,
		'form': form,
		'delete': can_delete,
		'edit': can_edit,
	}
	return render(request, 'graph/edit_section.html', context)

def edit_subject(request, pk):
	try:
		subject = model.Subject.objects.get(pk = pk)
	except exceptions.ObjectDoesNotExist:
		return render(request, 'errors/404.html')
	if not request.user or request.user.is_anonymous:
		return render(request, 'errors/401.html')
	user = request.user
	can_delete, can_edit = subject.perms(user)
	if request.method == 'POST':
		form = forms.Subject_Form(request.POST, instance = subject)
		action = request.POST['action'].split(',')
		if 'delete' in request.POST:
			spk = subject.section.pk
			subject.delete()
			messages.add_message(request, messages.SUCCESS, 'Temat został usunięty.')
			return redirect('view_section', pk = spk)
		elif 'save' in request.POST and form.is_valid():
			form.save()
			messages.add_message(request, messages.SUCCESS, 'Zmiany w temacie zostały zapisane.')
			return redirect('view_section', pk = subject.section.pk)
		elif 'prop_delete' in action:
			subject.propose_deletion(user)
			messages.add_message(request, messages.SUCCESS, 'Wniosek został wysłany.')
			return redirect('view_section', pk = subject.section.pk)
		elif 'prop_change' in action and form.is_valid():
			subject.propose_change(user, form.cleaned_data)
			messages.add_message(request, messages.SUCCESS, 'Wniosek został wysłany.')
			return redirect('view_section', pk = subject.section.pk)
	else:
		form = forms.Subject_Form(instance = subject)
	context = {
		'this_subject': subject,
		'form': form,
		'delete': can_delete,
		'edit': can_edit,
	}
	return render(request, 'graph/edit_subject.html', context)

def new_vertex(request, subject_pk):
	if not request.user or request.user.is_anonymous:
		return render(request, 'errors/401.html')
	try:
		subject = model.Subject.objects.get(pk = subject_pk)
	except exceptions.ObjectDoesNotExist:
		if subject_pk != 1:
			return redirect('new_vertex', subject_pk = 1)
		else:
			return render(request, 'errors/404.html')
	if request.method == 'POST':
		form = forms.Vertex_Form(request.POST)
		if 'save' in request.POST and form.is_valid():
			vertex = form.save(commit = False)
			vertex.user = request.user
			vertex.vertex_id = model.Vertex.new_id()
			vertex.save()
			messages.add_message(request, messages.SUCCESS, 'Nowy wierzchołek został dodany.')
			return redirect('edit_vertex', vertex_id = vertex.vertex_id)
	else:
		form = forms.Vertex_Form(initial={'title': ''})
	context = {
		'form': form,
		'subjects': model.Subject.objects.all(),
		'initial_subject': subject,
	}
	return render(request, 'graph/add_new_vertex.html', context)

def edit_vertex(request, vertex_id):
	try:
		this_vertex = model.Vertex.objects.get(vertex_id = vertex_id)
	except exceptions.ObjectDoesNotExist:
		return render(request, 'errors/404.html')
	if not request.user == this_vertex.user:
		return render(request, 'errors/403.html')
	outgoing_edges = this_vertex.get_successors()
	if request.method == 'POST':
		form = forms.Edit_Vertex_Form(request.POST, instance = this_vertex)
		action = request.POST['action'].split(',')
		if 'delete' in action:
			user = this_vertex.user
			this_vertex.delete()
			messages.add_message(request, messages.SUCCESS, 'Wierzchołek został usunięty.')
			return redirect('profile', username = user.username)
		if 'newedge' in request.POST:
			request.session['pred'] = this_vertex.vertex_id
			return redirect('new_edge')
		if 'save' in action and form.is_valid():
			subject_pk = request.POST['dss_pk'] or '1'
			this_vertex.change_dss_from_pk( int(subject_pk) )
			this_vertex.save_from_dict(form.cleaned_data)
			messages.add_message(request, messages.SUCCESS, "Właściwości wierzchołka zostały zapisane.")
	else:
		form = forms.Edit_Vertex_Form(instance = this_vertex)
	context = {
		'form': form, 
		'vertex_id': this_vertex.vertex_id, 
		'submitted': this_vertex.submitted, 
		'outgoing_edges': outgoing_edges,
		'subjects': model.Subject.objects.all(),
		'this_subject': this_vertex.subject
	}
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
			model.Vertex_Class.make_proposal(request.user, form.cleaned_data)
			messages.add_message(request, messages.SUCCESS, 'Wniosek został wysłany.')
			return redirect('profile', username = request.user.username)
	else:
		form = forms.Add_New_Vertex_Class_Form()
	context = {'form': form}
	return render(request, 'graph/add_new_vertex_class.html', context)

def new_edge(request):
	if not request.user or request.user.is_anonymous:
		return render(request, '401.html')
	if request.method == 'POST':
		action = request.POST['action'].split(',')
		if 'save' in action:
			i = action.index('save')
			pred = action[i+1]
			succ = action[i+2]
			edge = model.Edge()
			edge.user = request.user
			edge.edge_id = model.Edge.new_id()
			edge.predecessor = model.Vertex.objects.get(vertex_id = pred)
			if succ.startswith('V'):
				edge.successor = model.Vertex.objects.get(vertex_id = succ)
			else:
				edge.successor = None
			edge.save()
			messages.add_message(request, messages.SUCCESS, 'Nowa krawędź została dodana.')
			del request.session['pred']
			return redirect('edit_edge', edge_id = edge.edge_id)
	context = {
		'pred_is_chosen': True, 
		'predecessor': model.Vertex.objects.get( vertex_id = request.session.get('pred') ), 
		'succ_is_chosen': False,
		'successor': model.Vertex.get_default(), 
		'vertices': model.Vertex.objects.filter(user = request.user)
	}
	return render(request, 'graph/add_new_edge.html', context)

def edit_edge(request, edge_id):
	try:
		this_edge = model.Edge.objects.get(edge_id = edge_id)
	except exceptions.ObjectDoesNotExist:
		return render(request, 'errors/404.html')
	user = request.user
	if user != this_edge.user:
		return render(request, 'errors/403.html')
	if request.method == 'POST':
		form = forms.Edit_Edge_Form(request.POST, edge = this_edge)
		action = request.POST['action'].split(',')
		if 'save' in action and form.is_valid():
			this_edge.preamble = form.cleaned_data['preamble']
			i = action.index('save')
			successor_id = action[i+1]
			if successor_id.startswith('V'):
				this_edge.successor = model.Vertex.objects.get(vertex_id = successor_id)
			else:
				this_edge.successor = None
			this_edge.write_pre_dir( form.cleaned_data['content'] )
			this_edge.save()
			messages.add_message(request, messages.INFO, 'Zmiany w krawędzi zostały zapisane.')
		if 'delete' in action:
			pred = this_edge.predecessor
			this_edge.delete()
			messages.add_message(request, messages.SUCCESS, 'Krawędź została usunięta.')
			if pred:
				return redirect('edit_vertex', vertex_id = pred.vertex_id)
			else:
				return redirect('start')
	else:
		form = forms.Edit_Edge_Form(edge = this_edge)
	context = {
		'form': form, 
		'predecessor': this_edge.predecessor, 
		'edge_id': edge_id, 
		'vertices': model.Vertex.objects.filter(user = request.user)
	}
	if this_edge.successor:
		context['successor'] = this_edge.successor
		context['is_chosen'] = True
	else:
		context['successor'] = model.Vertex.get_default()
		context['is_chosen'] = False
	return render(request, 'graph/edit_edge.html', context)

def new_path(request):
	if not request.user or request.user.is_anonymous:
		return render(request, 'errors/401.html')
	if request.method == 'POST':
		form = forms.Add_New_Path_Form(request.POST)
		action = request.POST['action'].split(',')
		if 'save' in action and form.is_valid():
			path = model.Path(user = request.user, name = form.cleaned_data['name'])
			path.description = form.cleaned_data['description'] or None
			path.path_id = model.Path.new_id()
			i = action.index('save')
			first = model.Vertex.objects.get( vertex_id = action[i+1] )
			path.save()
			path.write_and_save( [first, ] )
			messages.add_message(request, messages.SUCCESS, 'Nowa ścieżka została dodana.')
			return redirect('edit_path', path_id = path.path_id)
	else:
		form = forms.Add_New_Path_Form()
	context = {
		'form': form, 
		'vertices': model.Vertex.objects.all(),
		'dummy': model.Vertex.get_default()
	}
	return render(request, 'graph/add_new_path.html', context)

def edit_path(request, path_id):
	try:
		this_path = model.Path.objects.get(path_id = path_id)
	except exceptions.ObjectDoesNotExist:
		return render(request, 'errors/404.html')
	user = request.user or None
	if user != this_path.user:
		return render(request, 'errors/403.html')
	if request.method == 'POST':
		form = forms.Edit_Path_Form(request.POST, path = this_path)
		action = request.POST['action'].split(',')
		if 'save' in request.POST and form.is_valid():
			this_path.name = form.cleaned_data['name']
			this_path.description = form.cleaned_data['description']
			this_path.save()
			messages.add_message(request, messages.SUCCESS, 'Zmiany w ścieżce zostały zapisane.')
		if 'delete' in action:
			this_path.delete()
			messages.add_message(request, messages.SUCCESS, 'Ścieżka została usunięta.')
			return redirect('profile', username = user.username)
	else:
		form = forms.Edit_Path_Form(path = this_path)
	context = {
		'form': form, 
		'path_id': path_id,
		'first': this_path.first, 
		'the_rest': this_path.read_verticies()[1:], 
		'vertices': model.Vertex.objects.all()
	}
	if this_path.length < 2:
		context['last_one'] = True
	return render(request, 'graph/edit_path.html', context)