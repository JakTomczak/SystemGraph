
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import django.core.exceptions as exceptions
import time

from . import tasks
from .models import Vertex

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