
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import django.core.exceptions as exceptions
import time

from . import tasks
from .models import Vertex, Path

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
def update_compilation_status(request):
	return JsonResponse({})
	
@csrf_exempt
def vertex_save(request, vertex_id):
	return JsonResponse({})
	
@csrf_exempt
def start_compilation(request, vertex_id):
	print('abba')
	# task = tasks.test1.apply_async(task_id = vertex_id)
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