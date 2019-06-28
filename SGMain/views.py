import os

from django.shortcuts import render, redirect
from django.contrib import messages

from . import models as model
from . import forms
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
	return render(request, 'graph/edit_vertex.html', context)

def view_vertex(request, vertex_id):
	return render(request, 'graph/view_vertex.html', context)

def new_vertex_class(request):
	return render(request, 'graph/add_new_vertex_class.html', context)

def new_preamble(request):
	return render(request, 'graph/add_new_preamble.html', context)

def edit_preamble(request, preamble_id):
	return render(request, 'graph/edit_preamble.html', context)

def new_discipline(request):
	return render(request, 'graph/add_new_discipline.html', context)

def new_subject(request):
	return render(request, 'graph/add_new_subject.html', context)

def new_path(request):
	return render(request, 'graph/add_new_path.html', context)