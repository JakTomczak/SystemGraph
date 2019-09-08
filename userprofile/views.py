import os

from django.shortcuts import render
from django.contrib import messages
import django.core.exceptions as exceptions

import SGMain.models as model
from users.models import CustomUser
from . import forms 
	
def profile(request, username):
	try:
		user = CustomUser.objects.get(username = username)
	except exceptions.ObjectDoesNotExist:
		return render(request, 'errors/404.html')
	verts = model.Vertex.objects.filter(user = user, submitted = True).order_by('-date')[:4]
	paths = list( model.Path.objects.filter(user = user).order_by('-date') )
	if request.user == user:
		projects = model.Vertex.objects.filter(user = user, submitted = False).order_by('-date')
		preambles = model.Preamble.objects.filter(user = user)
		context = {
			'projects': projects, 
			'verts': verts, 
			'preambles': preambles, 
			'paths': paths,
			'edge_propositions': model.Edge_Proposition.get_user_propositions(user)
		}
		return render(request, 'common/profile_thisuser.html', context)
	else:
		context = {'this_user': user, 'verts': verts, 'paths': paths}
		return render(request, 'common/profile_notthisuser.html', context)
	
def edit_profile(request, username):
	try:
		user = CustomUser.objects.get(username = username)
	except exceptions.ObjectDoesNotExist:
		return render(request, 'errors/404.html')
	if request.user != user:
		return render(request, 'errors/403.html')
	if request.method == 'POST':
		form = forms.Edit_Profile_Form(data = request.POST, user = user)
		if 'save' in request.POST and form.is_valid():
			user.email = form.cleaned_data['email']
			user.save()
			messages.add_message(request, messages.SUCCESS, 'Dane użytkownika zostały zmienione.')
	else:
		form = forms.Edit_Profile_Form(user = user)
	context = {'thisuser': username, 'form': form}
	return render(request, 'common/edit_profile.html', context)
	
def all_user_vertices(request, username):
	try:
		user = CustomUser.objects.get(username = username)
	except exceptions.ObjectDoesNotExist:
		return render(request, 'errors/404.html')
	context = {
		'Vertices': model.Vertex.objects.filter(user = user, submitted = True).order_by('-date'),
		'this_user': user
	}
	return render(request, 'common/all_user_vertices.html', context)