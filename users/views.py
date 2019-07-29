from django.shortcuts import render
from django.contrib import messages
from django.urls import reverse
from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordResetView, PasswordChangeView

from django_registration.backends.activation.views import RegistrationView, ActivationView

from . import forms as user_forms

class SG_RegistrationView(RegistrationView):
	form_class = user_forms.SG_RegistrationForm
	success_url = reverse_lazy('registration_complete')
	template_name = 'users/registration.html'
	email_body_template = 'users/activation_email_body.txt'
	email_subject_template = 'users/activation_email_subject.txt'

class SG_ActivationView(ActivationView):
	template_name = 'users/activation_failed.html'
	success_url = reverse_lazy('activation_complete')
	
class SG_PasswordResetView(PasswordResetView):
	email_template_name = 'users/password_reset_body.txt'
	subject_template_name = 'users/password_reset_subject.txt'
	template_name = 'users/password_reset.html'
	title = 'Reset hasla'
	
class SG_PasswordChangeView(PasswordChangeView):
	template_name = 'users/password_change.html'
	title = 'Zmiana hasla'
	success_url = reverse_lazy('frontpage')
	
	def form_valid(self, form):
		messages.success(self.request, 'Hasło zostało zmienione.')
		return super().form_valid(form)