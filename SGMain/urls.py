
from django.urls import path

from SGMain.views import common as common_views
from SGMain.views import graph as graph_views

urlpatterns = [
	path('search/', common_views.SearchSite, name='vertex_search'),
	path('add_new_path/', graph_views.new_path, name='new_path'),
	path('add_new_preamble/', graph_views.new_preamble, name='new_preamble'),
	path('add_new_vertex/', graph_views.new_vertex, name='new_vertex'),
	path('edit_preamble/<preamble_id>/', graph_views.edit_preamble, name='edit_preamble'),
]