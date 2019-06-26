
from django.urls import path

from SGMain.views import common as common_views
from SGMain.views import graph as graph_views

urlpatterns = [
	path('search/', common_views.SearchSite, name='vertex_search'),
	path('add_new_vertex/', graph_views.new_vertex, name='new_vertex'),
]