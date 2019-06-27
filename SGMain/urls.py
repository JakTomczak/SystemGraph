
from django.urls import path

from SystemGraph import common_views
from . import views

urlpatterns = [
	path('search/', common_views.SearchSite, name='vertex_search'),
	path('add_new_path/', views.new_path, name='new_path'),
	path('add_new_preamble/', views.new_preamble, name='new_preamble'),
	path('add_new_vertex/', views.new_vertex, name='new_vertex'),
	path('edit_preamble/<preamble_id>/', views.edit_preamble, name='edit_preamble'),
]