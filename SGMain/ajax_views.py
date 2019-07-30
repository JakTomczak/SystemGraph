import threading
import time

from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import django.core.exceptions as exceptions
from datetime import datetime

from . import tasks
from . import compilation
from .models import Vertex, Path, CompilationData, Subject, Edge

def request_is_NOT_valid(request, vertex_id = None, edge_id = None):
	if int(vertex_id is not None) + int(edge_id is not None) != 1:
		return True
	object = None
	if vertex_id:
		try:
			object = Vertex.objects.get(vertex_id = vertex_id)
		except exceptions.ObjectDoesNotExist:
			pass
	elif edge_id:
		try:
			object = Edge.objects.get(edge_id = edge_id)
		except exceptions.ObjectDoesNotExist:
			pass
	if object and object.user == request.user:
		return False
	# log
	return True

@csrf_exempt
def add_vertex_to_path_from_id(request):
	path_id = request.POST.get('path_id', '')
	try:
		P = Path.objects.get(path_id = path_id)
	except exceptions.ObjectDoesNotExist:
		return JsonResponse({})
	if P.user != request.user:
		return JsonResponse({})
	where = request.POST.get('where', 'end')
	vertex_id = request.POST.get('vid', '')
	try:
		vertex = Vertex.objects.get(vertex_id = vertex_id)
	except exceptions.ObjectDoesNotExist:
		return JsonResponse({})
	if where == 'end':
		P.add_at_end_and_save(vertex)
	else:
		try:
			where = int(where)
		except ValueError:
			pass
		else:
			P.add_here_and_save(where + 1, vertex)
	return JsonResponse({})

@csrf_exempt
def change_vertex_in_path_from_id(request):
	path_id = request.POST.get('path_id', '')
	try:
		P = Path.objects.get(path_id = path_id)
	except exceptions.ObjectDoesNotExist:
		return JsonResponse({})
	if P.user != request.user:
		return JsonResponse({})
	where = request.POST.get('where', '0')
	vertex_id = request.POST.get('vid', '')
	try:
		vertex = Vertex.objects.get(vertex_id = vertex_id)
	except exceptions.ObjectDoesNotExist:
		return JsonResponse({})
	try:
		where = int(where)
	except ValueError:
		pass
	else:
		P.change_this_one_and_save(where, vertex)
	return JsonResponse({})

@csrf_exempt
def delete_vertex_from_path(request):
	path_id = request.POST.get('path_id', '')
	try:
		P = Path.objects.get(path_id = path_id)
	except exceptions.ObjectDoesNotExist:
		return JsonResponse({})
	if P.user != request.user:
		return JsonResponse({})
	which = request.POST.get('which', '0')
	try:
		which = int(which)
	except ValueError:
		pass
	else:
		P.delete_one(which)
	return JsonResponse({})

@csrf_exempt
def get_subject_from_pk(request):
	pk = int( request.POST.get('pk', '') )
	try:
		S = Subject.objects.get(pk = pk)
	except exceptions.ObjectDoesNotExist:
		S = Subject.get_default()
	context = {'subject': S.ajax()}
	return JsonResponse(context)

@csrf_exempt
def get_vertex_from_id(request):
	vid = request.POST.get('vid', '')
	try:
		V = Vertex.objects.get(vertex_id = vid)
	except exceptions.ObjectDoesNotExist:
		V = Vertex.get_default()
	context = {'vertex': V.ajax()}
	return JsonResponse(context)
	
@csrf_exempt
def save_vertex_cd(request, vertex_id):
	vertex = Vertex.objects.get(vertex_id = vertex_id)
	if vertex.user != request.user:
		return JsonResponse({})
	content = request.POST.get('content', '')
	vertex.write_pre_content(content)
	description = request.POST.get('description', '')
	vertex.write_pre_desc(description)
	return JsonResponse({})
	
@csrf_exempt
def start_vertex_cont_compilation(request, vertex_id):
	context = {'ok': False, 'error_message': ''}
	if request_is_NOT_valid(request, vertex_id = vertex_id):
		return JsonResponse(context)
	content = request.POST.get('content', '')
	if content:
		context['error_message'] = CompilationData.check_if_idle(vertex_id = vertex_id, desc = False)
		if context['error_message'] == '':
			context['ok'] = True
			tasks.start_compilation.delay(vertex_id = vertex_id, desc = False, text = content)
			time.sleep(1)
	else:
		context['error_message'] = 'Nie możesz opublikować pustego wierzchołka'
	return JsonResponse(context)
	
@csrf_exempt
def start_vertex_desc_compilation(request, vertex_id):
	context = {'ok': False, 'error_message': ''}
	if request_is_NOT_valid(request, vertex_id = vertex_id):
		return JsonResponse(context)
	description = request.POST.get('description', '')
	if description:
		context['error_message'] = CompilationData.check_if_idle(vertex_id = vertex_id, desc = True)
		if context['error_message'] == '':
			context['ok'] = True
			tasks.start_compilation.delay(vertex_id = vertex_id, desc = True, text = description)
			time.sleep(1)
	else:
		compilation.CompilationCore.empty_vdesc(vertex_id)
	return JsonResponse(context)
	
@csrf_exempt
def update_compilation_status(request):
	vertex_id = request.POST.get('vertex_id', None)
	edge_id = request.POST.get('edge_id', None)
	if request_is_NOT_valid(request, vertex_id = vertex_id, edge_id = edge_id):
		return JsonResponse({'still': False, 'error': True, 'messages': []})
	
	desc = (request.POST.get('desc', None) == 'true')
	
	running, error, messages = CompilationData.check_status(vertex_id = vertex_id, desc = desc, edge_id = edge_id)
	if messages:
		if type(messages) == list:
			mlength = int(request.POST.get('mlength', '0'))
			messages = messages[mlength:]
		else:
			messages = [messages, ]
	context = {'still': running, 'error': error, 'messages': messages}
	return JsonResponse(context)
	
@csrf_exempt
def save_edge_content(request, edge_id):
	edge = Edge.objects.get(edge_id = edge_id)
	if edge.user != request.user:
		return JsonResponse({})
	content = request.POST.get('content', '')
	edge.write_pre_dir(content)
	return JsonResponse({})
	
@csrf_exempt
def start_edge_compilation(request, edge_id):
	context = {'ok': False, 'error_message': ''}
	if request_is_NOT_valid(request, edge_id = edge_id):
		return JsonResponse(context)
	content = request.POST.get('content', '')
	if content:
		context['error_message'] = CompilationData.check_if_idle(edge_id = edge_id)
		if context['error_message'] == '':
			context['ok'] = True
			tasks.start_compilation.delay(edge_id = edge_id, text = content)
			time.sleep(1)
	else:
		compilation.CompilationCore.empty_edge(edge_id)
	return JsonResponse(context)