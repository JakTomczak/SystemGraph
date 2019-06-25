
from django.urls import path

from SGMain.views import common as common_views

urlpatterns = [
	path('search/', common_views.SearchSite, name='vertex_search'),
	path('profile/<username>/', common_views.profile, name='profile'),
]