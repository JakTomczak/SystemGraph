import os
import codecs

from django.conf import settings
from django import forms

from .models import *

class Add_New_Vertex_Form(forms.ModelForm):
	preamble = forms.ModelChoiceField( queryset = Preamble.objects.none(), empty_label = None )
	vertex_class = forms.ModelChoiceField( queryset = Vertex_Class.objects.all(), empty_label = None )
	discipline = forms.ModelChoiceField( queryset = Discipline.objects.all(), empty_label = None )
	subject = forms.ModelChoiceField( queryset = Subject.objects.all(), empty_label = None )
	title = forms.CharField(max_length = 120)
	
	class Meta:
		model = Vertex
		fields = ('preamble', 'vertex_class', 'discipline', 'subject', 'title')
	
	def __init__(self, *args, **kwargs):
		user = kwargs.pop('user', None)
		super(Add_New_Vertex_Form, self).__init__(*args, **kwargs)
		self.fields['preamble'].queryset = Preamble.get_user_preambles(user)