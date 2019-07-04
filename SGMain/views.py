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
			this_vertex.write_pre_content( form.cleaned_data['content'] )
			this_vertex.write_pre_desc( form.cleaned_data['description'] )
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

def new_edge(request):
	if not request.user or request.user.is_anonymous:
		return render(request, '401.html')
	if request.method == 'POST':
		form = forms.Add_New_Edge_Form(request.POST, user = request.user )
		if form.is_valid():
			verts = request.POST['action'].split(',')
			if verts:
				pred = verts[0].split(':')[1]
				succ = verts[1].split(':')[1]
				edge = form.save(commit = False)
				edge.user = request.user
				edge.edge_id = model.Edge.new_id()
				edge.create_pre_dirs()
				edge.predecessor = model.Vertex.objects.get(vertex_id = pred)
				if succ.startswith('V'):
					edge.successor = model.Vertex.objects.get(vertex_id = succ)
				else:
					edge.successor = None
				edge.save()
				messages.add_message(request, messages.SUCCESS, 'Nowa krawędź została dodana.')
				del request.session['pred']
				return redirect('edit_edge', edge = edge.edge_id)
	else:
		form = forms.Add_New_Edge_Form(user = request.user)
	previous_vertex_id = request.session.get('pred')
	context = {'form': form, 'pred': previous_vertex_id, 'Plist': list( model.Vertex.objects.filter(user = request.user) ), 'Slist': list( model.Vertex.objects.filter(user = request.user) )}
	return render(request, 'graph/add_new_edge.html', context)

def edit_edge(request, edge_id):
	try:
		this_edge = model.Edge.objects.get(edge_id = edge_id)
	except exceptions.ObjectDoesNotExist:
		return render(request, 'errors/404.html')
	user = request.user
	if user != this_edge.user:
		return render(request, 'errors/403.html')
	dummy = model.Vertex.objects.get(is_default = True)
	if request.method == 'POST':
		form = forms.Edit_Edge_Form(request.POST, edge = this_edge)
		action = request.POST['action'].split(',')
		if 'save_all' in request.POST and form.is_valid():
			this_edge.preamble = form.cleaned_data['preamble']
			this_edge.successor = form.cleaned_data['successor']
			this_edge.write_pre_dir( form.cleaned_data['content'] )
			this_edge.save()
			messages.add_message(request, messages.INFO, 'Zmiany w krawędzi zostały zapisane.')
		elif 'limituser' in request.POST or 'limitdiscipline' in request.POST:
			if form.is_valid():
				u = form.cleaned_data['limituser']
				d = form.cleaned_data['limitdiscipline']
				if u:
					if d:
						form.both_limitation(u, d)
					else:
						form.user_limitation(u)
				else:
					if d:
						form.discipline_limitation(d)
					else:
						form.nolimitation()
		if 'delete' in action:
			pred = this_edge.predecessor.vertex_id
			this_edge.delete()
			messages.add_message(request, messages.SUCCESS, 'Krawędź została usunięta.')
			return redirect('edit_vertex', vertex = pred)
	else:
		form = forms.Edit_Edge_Form(edge = this_edge)
	context = {'form': form, 'predecessor': this_edge.predecessor, 'edge_id': edge_id, 'dummy': dummy}
	return render(request, 'graph/edit_edge.html', context)

def new_path(request):
	if not request.user or request.user.is_anonymous:
		return render(request, 'errors/401.html')
	if request.method == 'POST':
		form = forms.Add_New_Path_Form(request.POST)
		if 'save' in request.POST and form.is_valid():
			path = model.Path(user = request.user, name = form.cleaned_data['name'])
			path.description = form.cleaned_data['description'] or None
			path.path_id = model.Path.new_id()
			path.save()
			path.write_and_save( [form.cleaned_data['beginnig'], ] )
			messages.add_message(request, messages.SUCCESS, 'Nowa ścieżka została dodana.')
			return redirect('edit_path', path_id = path.path_id)
	else:
		form = forms.Add_New_Path_Form()
	context = {'form': form, 'Vlist': list( model.Vertex.objects.all() )}
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
			messages.add_message(request, messages.INFO, 'Zmiany w ścieżce zostały zapisane.')
		if 'delete-path' in action:
			this_path.delete()
			messages.add_message(request, messages.SUCCESS, 'Ścieżka została usunięta.')
			return redirect('profile', username = user.username)
		if 'change' in action:
			i = action.index('change')
			which = action[i+1]
			vid = action[i+2]
			V = model.Vertex.objects.get(vertex_id = vid)
			if which == 'end':
				this_path.write_at_end_and_save( V )
			else:
				Vertexes = this_path.read_verticies()
				w = float(which)
				if abs(w - int(w)) < 0.001:
					Vertexes[int(w) - 1] = V
				else:
					Vertexes.insert(int(w), V)
				this_path.write_and_save(Vertexes)
		elif 'delete-entry' in action:
			i = action.index('delete-entry')
			which = action[i+1] - 1
			this_path.delete_one(which)
	else:
		form = forms.Edit_Path_Form(path = this_path)
	context = {'form': form, 'start': this_path.first, 'the_rest': this_path.read_verticies()[1:], 'Vlist': list( model.Vertex.objects.all() )}
	return render(request, 'graph/edit_path.html', context)