
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
	
@csrf_exempt
def update_compilation_status(request):
	return JsonResponse(data)
	
@csrf_exempt
def vertex_save(request, vertex_id):
	return JsonResponse({'ok': True})
	
@csrf_exempt
def start_compilation(request, vertex_id):
	return JsonResponse(data)
	
@csrf_exempt
def start_edge_compilation(request, vertex_id):
	return JsonResponse(data)
	
@csrf_exempt
def edge_save(request, vertex_id):
	return JsonResponse(data)