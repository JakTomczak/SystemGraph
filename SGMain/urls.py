
from django.urls import path

from SystemGraph import common_views
from . import views

urlpatterns = [
	path('search/', common_views.SearchSite, name='vertex_search'),
	
	path('add_new_discipline/', views.new_discipline, name = 'new_discipline'),
	path('add_new_edge/', views.new_edge, name='new_edge'),
	path('add_new_path/', views.new_path, name='new_path'),
	path('add_new_preamble/', views.new_preamble, name='new_preamble'),
	path('add_new_subject/', views.new_subject, name = 'new_subject'),
	path('add_new_vertex/', views.new_vertex, name='new_vertex'),
	path('add_new_vertex_class/', views.new_vertex_class, name = 'new_vertex_class'),
	
	path('edit_preamble/<preamble_id>/', views.edit_preamble, name='edit_preamble'),
	path('edit_vertex/<vertex_id>/', views.edit_vertex, name = 'edit_vertex'),
	
	path('vertex/<vertex_id>', views.view_vertex, name = 'view_vertex'),
]