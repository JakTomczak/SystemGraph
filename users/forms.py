
from django_registration.forms import RegistrationForm

from .models import CustomUser
		
class CustomRegistrationForm(RegistrationForm):
	
	class Meta(RegistrationForm.Meta):
		model = CustomUser
		
	def save(self, commit = True):
		user = super(CustomRegistrationForm, self).save(commit = False)
		user.get_folder(save = commit)
		return user