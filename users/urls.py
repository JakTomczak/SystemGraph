
from django.urls import path
from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views

from . import views as users_views
from SystemGraph import common_views

urlpatterns = [
	path('search/', common_views.search_users, name='user_search'),
	
    path('register/', users_views.SG_RegistrationView.as_view(), name='register'),
	path('registration_complete/', TemplateView.as_view(template_name = 'users/registration_complete.html'), name='registration_complete'),
	path('activate/<activation_key>/', users_views.SG_ActivationView.as_view(), name='activate'),
	path('activation_complete/', TemplateView.as_view( template_name = 'users/activation_complite.html' ), name='activation_complete'),
    path('delete/', users_views.delete_user, name='delete'),
    path('login/', auth_views.LoginView.as_view(template_name = 'users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name = 'users/logout.html'), name='logout'),
    path('password_change/', users_views.SG_PasswordChangeView.as_view(), name='password_change'),
    path('password_reset/', users_views.SG_PasswordResetView.as_view(), name='password_reset'),
	path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name = 'users/password_reset_done.html'), name='password_reset_done'),
	path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name = 'users/password_reset_newpassword.html'), name='password_reset_confirm'),
	path('reset/done/', TemplateView.as_view(template_name = 'users/password_reset_complete.html'), name='password_reset_complete'),
]