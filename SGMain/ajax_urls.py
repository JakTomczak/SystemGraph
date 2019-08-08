
from django.urls import path

from . import ajax_views as views

urlpatterns = [
	path('add_vertex_to_path_from_id/', views.add_vertex_to_path_from_id, name='add_vertex_to_path_from_id'),
	path('change_vertex_in_path_from_id/', views.change_vertex_in_path_from_id, name='change_vertex_in_path_from_id'),
	path('delete_vertex_from_path/', views.delete_vertex_from_path, name='delete_vertex_from_path'),
	
	path('get_subject_from_pk/', views.get_subject_from_pk, name='get_subject_from_pk'),
	path('get_vertex_from_id/', views.get_vertex_from_id, name='get_vertex_from_id'),
	
	path('save_vertex_cd/<vertex_id>/', views.save_vertex_cd, name='save_vertex_cd'),
	path('start_vertex_cont_compilation/<vertex_id>/', views.start_vertex_cont_compilation, name='start_vertex_cont_compilation'),
	path('start_vertex_desc_compilation/<vertex_id>/', views.start_vertex_desc_compilation, name='start_vertex_desc_compilation'),
	
	path('check_compilation/', views.update_compilation_status, name='check_compilation'),
	
	path('save_edge_content/<edge_id>/', views.save_edge_content, name='save_edge_content'),
	path('start_edge_compilation/<edge_id>/', views.start_edge_compilation, name='start_edge_compilation'),
	
	path('reject_eprop/', views.reject_eprop, name='reject_eprop'),
	path('accept_eprop/', views.accept_eprop, name='accept_eprop'),
]