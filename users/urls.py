
from django.urls import path
from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views

from . import views as users_views

urlpatterns = [
    path('register/', users_views.SG_RegistrationView.as_view(), name='register'),
	path('register/complete/', TemplateView.as_view(template_name = 'users/registration_complete.html'), name='registration_complete'),
	path('activate/<activation_key>/', users_views.SG_ActivationView.as_view( template_name = 'registration/activate.html' ), name='activate'),
	path('activation_complite/', TemplateView.as_view( template_name = 'users/activation_complite.html' ), name='activation_complete'),
    path('login/', auth_views.LoginView.as_view(template_name = 'users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name = 'users/logout.html'), name='logout'),
]