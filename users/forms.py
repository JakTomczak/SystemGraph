
from django import forms
from django_registration.forms import RegistrationForm

from .models import CustomUser
		
class CustomRegistrationForm(RegistrationForm):
	
	class Meta(RegistrationForm.Meta):
		model = CustomUser
		
	def save(self, commit = True):
		user = super(CustomRegistrationForm, self).save(commit = False)
		user.get_folder(save = commit)
		return user
			
class Edit_Profile_Form(forms.Form):
	email = forms.CharField(max_length = 100)
	
	class Meta:
#		model = CustomUser
		fields = ('email',)
		
	def __init__(self, *args, **kwargs):
		user = kwargs.pop('user', None)
		super(Edit_Profile_Form, self).__init__(*args, **kwargs)
		self.initial['email'] = user.email