
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

class DeleteAccountForm(forms.Form):
	password = forms.CharField(widget=forms.PasswordInput)
	
	def __init__(self, *args, **kwargs):
		self.user = kwargs.pop('user', None)
		super(DeleteAccountForm, self).__init__(*args, **kwargs)
	
	def clean_password(self):
		valid = self.user.check_password(self.cleaned_data['password'])
		if not valid:
			raise forms.ValidationError("Password Incorrect")
		return valid