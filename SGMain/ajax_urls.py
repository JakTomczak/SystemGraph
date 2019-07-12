
from django.urls import path

from . import ajax_views as views

urlpatterns = [
	path('add_vertex_to_path_from_id/', views.add_vertex_to_path_from_id, name='add_vertex_to_path_from_id'),
	path('change_vertex_in_path_from_id/', views.change_vertex_in_path_from_id, name='change_vertex_in_path_from_id'),
	path('check_compilation/', views.update_compilation_status, name='check_compilation'),
	path('compile_edge/<edge_id>/', views.start_edge_compilation, name='compile_edge'),
	path('compile_vertex/<vertex_id>/', views.start_compilation, name='compile_vertex'),
	path('delete_vertex_from_path/', views.delete_vertex_from_path, name='delete_vertex_from_path'),
	path('get_vertex_from_id/', views.get_vertex_from_id, name='get_vertex_from_id'),
	path('save_edge/<edge_id>/', views.edge_save, name='save_edge'),
	path('save_vertex/<vertex_id>/', views.vertex_save, name='save_vertex'),
]