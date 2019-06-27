
from django import forms
			
class Edit_Profile_Form(forms.Form):
	email = forms.CharField(max_length = 100)
	
	class Meta:
		fields = ('email',)
		
	def __init__(self, *args, **kwargs):
		user = kwargs.pop('user', None)
		super(Edit_Profile_Form, self).__init__(*args, **kwargs)
		self.initial['email'] = user.email