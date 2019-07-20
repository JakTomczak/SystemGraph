import threading
import time

from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import django.core.exceptions as exceptions
from datetime import datetime

from . import tasks
from . import tools
from . import compilation
from .models import Vertex, Path, CompilationData

@csrf_exempt
def add_vertex_to_path_from_id(request):
	path_id = request.POST.get('path_id', '')
	try:
		P = Path.objects.get(path_id = path_id)
	except exceptions.ObjectDoesNotExist:
		return JsonResponse(context)
	where = request.POST.get('where', 'end')
	vertex_id = request.POST.get('vid', '')
	try:
		vertex = Vertex.objects.get(vertex_id = vertex_id)
	except exceptions.ObjectDoesNotExist:
		return JsonResponse(context)
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
		return JsonResponse(context)
	where = request.POST.get('where', '0')
	vertex_id = request.POST.get('vid', '')
	try:
		vertex = Vertex.objects.get(vertex_id = vertex_id)
	except exceptions.ObjectDoesNotExist:
		return JsonResponse(context)
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
		return JsonResponse(context)
	which = request.POST.get('which', '0')
	try:
		which = int(which)
	except ValueError:
		pass
	else:
		P.delete_one(which)
	return JsonResponse({})

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
def vertex_save(request, vertex_id):
	return JsonResponse({})
	
@csrf_exempt
def save_vertex_cd(request, vertex_id):
	vertex = Vertex.objects.get(vertex_id = vertex_id)
	content = request.POST.get('content', '')
	vertex.write_pre_content(content)
	description = request.POST.get('description', '')
	vertex.write_pre_desc(description)
	return JsonResponse({})
	
@csrf_exempt
def save_vertex_props(request, vertex_id):
	vertex = Vertex.objects.get(vertex_id = vertex_id)
	content = request.POST.get('content', '')
	vertex.write_pre_content(content)
	description = request.POST.get('description', '')
	vertex.write_pre_desc(description)
	return JsonResponse({})
	
@csrf_exempt
def start_vertex_cont_compilation(request, vertex_id):
	content = request.POST.get('content', '')
	context = {'ok': False, 'error_message': ''}
	if content:
		fcode = tools.fcode_from_id(vertex_id = vertex_id, desc = False)
		context['error_message'] = CompilationData.check_if_idle(fcode)
		if context['error_message'] == '':
			context['ok'] = True
			tasks.test.delay(fcode = fcode, vertex_id = vertex_id, desc = False, text = content)
			time.sleep(1)
	else:
		context['error_message'] = 'Nie możesz opublikować pustego wierzchołka'
	return JsonResponse(context)
	
@csrf_exempt
def start_vertex_desc_compilation(request, vertex_id):
	description = request.POST.get('description', '')
	context = {'ok': False, 'error_message': ''}
	if description:
		fcode = tools.fcode_from_id(vertex_id = vertex_id, desc = True)
		context['error_message'] = CompilationData.check_if_idle(fcode)
		if context['error_message'] == '':
			context['ok'] = True
			threading.Thread( target = compilation.compile_v1, kwargs = {'cdata': cdata, 'vertex_id': vertex_id, 'desc': True, 'text': description} )
			time.sleep(1)
	else:
		compilation.CompilationCore.empty_vdesc(vertex_id)
	return JsonResponse(context)
	
@csrf_exempt
def update_compilation_status(request):
	vertex_id = request.POST.get('vertex_id', None)
	desc = request.POST.get('desc', False)
	edge_id = request.POST.get('edge_id', None)
	fcode = tools.fcode_from_id(vertex_id = vertex_id, desc = desc, edge_id = edge_id)
	mlength = int(request.POST.get('mlength', '0'))
	if fcode:
		running, error, messages = CompilationData.check_status(fcode)
		if messages:
			if type(messages) == list:
				messages = messages[mlength:]
			else:
				messages = [messages, ]
		context = {'still': running, 'error': error, 'messages': messages}
	else:
		context = {'still': False, 'error': True, 'messages': []}
	return JsonResponse(context)

@csrf_exempt
def start_compilation(request, vertex_id):
	content = request.POST.get('content', '')
	description = request.POST.get('description', '')
	v = Vertex.objects.get(vertex_id = vertex_id)
	if content is not None:
		v.save_pre_content(content)
		tasks.nocompiler (v, False)
	if description is not None:
		v.save_pre_desc(content)
		tasks.nocompiler (v, True)
	return JsonResponse({})
	
@csrf_exempt
def start_edge_compilation(request, edge_id):
	return JsonResponse({})
	
@csrf_exempt
def edge_save(request, edge_id):
	time.sleep(3);
	return JsonResponse({})