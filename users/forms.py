
from django import forms
from django_registration.forms import RegistrationForm
from django.contrib.auth.forms import PasswordResetForm

from .models import CustomUser
		
class SG_RegistrationForm(RegistrationForm):
	
	class Meta(RegistrationForm.Meta):
		model = CustomUser
		
	def save(self, commit = True):
		user = super(SG_RegistrationForm, self).save(commit = False)
		user.get_folder(save = commit)
		return user
		

class SG_PasswordResetForm(PasswordResetForm):
	pass