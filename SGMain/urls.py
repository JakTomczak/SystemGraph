
from django.urls import path
from django.shortcuts import redirect

from SystemGraph import common_views
from . import views

urlpatterns = [
	path('search/', common_views.SearchSite, name='vertex_search'),
	
	path('add_new_discipline/', views.new_discipline, name = 'new_discipline'),
	path('add_new_section/<parent_pk>/', views.new_section, name = 'new_section'),
	path('add_new_section/', lambda request: redirect('new_section', parent_pk = 1, permanent = False), name='new_section'),
	path('add_new_subject/<parent_pk>/', views.new_subject, name = 'new_subject'),
	path('add_new_subject/', lambda request: redirect('new_subject', parent_pk = 1, permanent = False), name='new_subject'),
	
	path('all_disciplines/', views.all_disciplines, name = 'all_disciplines'),
	path('discipline/<pk>', views.view_discipline, name = 'view_discipline'),
	path('section/<pk>', views.view_section, name = 'view_section'),
	path('subject/<pk>', views.view_subject, name = 'view_subject'),
	
	path('edit_discipline/<pk>/', views.edit_discipline, name = 'edit_discipline'),
	path('edit_section/<pk>/', views.edit_section, name = 'edit_section'),
	path('edit_subject/<pk>/', views.edit_subject, name = 'edit_subject'),
	
	path('add_new_vertex/<subject_pk>', views.new_vertex, name='new_vertex'),
	path('add_new_vertex/', lambda request: redirect('new_vertex', subject_pk = 1, permanent = False), name='new_vertex'),
	path('edit_vertex/<vertex_id>/', views.edit_vertex, name = 'edit_vertex'),
	path('vertex/<vertex_id>', views.view_vertex, name = 'view_vertex'),
	
	path('add_new_edge/', views.new_edge, name='new_edge'),
	path('add_new_path/', views.new_path, name='new_path'),
	path('add_new_preamble/', views.new_preamble, name='new_preamble'),
	path('add_new_vertex/', views.new_vertex, name='new_vertex'),
	path('add_new_vertex_class/', views.new_vertex_class, name = 'new_vertex_class'),
	
	path('edit_edge/<edge_id>/', views.edit_edge, name='edit_edge'),
	path('edit_path/<path_id>/', views.edit_path, name='edit_path'),
	path('edit_preamble/<preamble_id>/', views.edit_preamble, name='edit_preamble'),
]