
from django.urls import path

from . import ajax_views as views

urlpatterns = [
	path('check_compilation/', views.update_compilation_status, name='check_compilation'),
	path('compile_edge/<edge_id>/', views.start_edge_compilation, name='compile_edge'),
	path('compile_vertex/<vertex_id>/', views.start_compilation, name='compile_vertex'),
	path('save_edge/<edge_id>/', views.edge_save, name='save_edge'),
	path('save_vertex/<vertex_id>/', views.vertex_save, name='save_vertex'),
]