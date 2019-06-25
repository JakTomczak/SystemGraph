from django.shortcuts import render
from django.urls import reverse_lazy

from django_registration.backends.activation.views import RegistrationView, ActivationView

from . import forms as user_forms

class SG_RegistrationView(RegistrationView):
	form_class = user_forms.CustomRegistrationForm
	success_url = reverse_lazy('registration_complete')
	template_name = 'users/registration_form.html'
	email_body_template = 'users/activation_email_body.txt'
	email_subject_template = 'users/activation_email_subject.txt'

class SG_ActivationView(ActivationView):
	template_name = 'users/activation_failed.html'
	success_url = reverse_lazy('activation_complete')