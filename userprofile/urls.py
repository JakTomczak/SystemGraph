from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
	path('<username>/', views.profile, name='profile'),
	path('<username>/edit/', views.edit_profile, name='edit_profile'),
	path('<username>/all_user_vertices/', views.all_user_vertices, name='all_user_vertices'),
]