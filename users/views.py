from django.shortcuts import render
from django.urls import reverse_lazy

from django_registration.backends.activation.views import RegistrationView, ActivationView

from . import forms as user_forms

class SG_RegistrationView(RegistrationView):
	form_class = user_forms.CustomRegistrationForm
	template_name = 'users/registration_form.html'

class SG_ActivationView(ActivationView):
	template_name = 'users/activation_failed.html'
	success_url = reverse_lazy('activation_complete')