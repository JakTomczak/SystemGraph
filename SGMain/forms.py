import os
import codecs

from django.conf import settings
from django import forms

from .models import *

Discipline_Form = forms.modelform_factory(Discipline, fields=('polish_name', ))
Section_Form = forms.modelform_factory(Section, fields=('polish_name', ))
Section_Form_Full = forms.modelform_factory(Section, fields=('polish_name', 'discipline'))
Subject_Form = forms.modelform_factory(Subject, fields=('polish_name', ))
Vertex_Form = forms.modelform_factory(Vertex, fields=('title', 'vertex_class', ))
Path_Form = forms.modelform_factory(Path, fields=('name', 'description', ))
		
class Edit_Vertex_Form (forms.ModelForm):
	description = forms.CharField(widget = forms.Textarea, required = False)
	content = forms.CharField(widget = forms.Textarea, required = False)
	
	class Meta:
		model = Vertex
		fields = ('preamble', 'vertex_class', 'title', 'shorttitle', 'content', 'description')
	
	def __init__(self, *args, **kwargs):
		super(Edit_Vertex_Form, self).__init__(*args, **kwargs)
		vertex = kwargs.pop('instance', None)
		self.fields['preamble'].queryset = Preamble.get_user_preambles(vertex.user)
		self.initial['preamble'] = vertex.preamble
		with codecs.open( vertex.get_pre_content_dir(), 'r', encoding = 'utf-8') as file:
			self.initial['content'] = file.read()
		with codecs.open( vertex.get_pre_desc_dir(), 'r', encoding = 'utf-8') as file:
			self.initial['description'] = file.read()
			
class Add_New_Preamble_Form(forms.ModelForm):
	description = forms.CharField(widget = forms.Textarea, required = False)
	content = forms.CharField(widget = forms.Textarea, required = False)
	
	class Meta:
		model = Preamble
		fields = ('title', 'description', 'content')
			
class Edit_Preamble_Form(Add_New_Preamble_Form):	
	def __init__(self, *args, **kwargs):
		super(Edit_Preamble_Form, self).__init__(*args, **kwargs)
		preamble = kwargs.pop('instance', None)
		self.initial['content'] = preamble.read()

class Add_New_Vertex_Class_Form(forms.Form):
	polish_name = forms.CharField(max_length = 50, required = False)
	polish_name_plural = forms.CharField(max_length = 50, required = False)
	left = forms.CharField(max_length = 50)
	right = forms.CharField(max_length = 50)
	top = forms.CharField(max_length = 50)
	bottom = forms.CharField(max_length = 50)
	info = forms.CharField(widget = forms.Textarea, required = False)
			
class Edit_Edge_Form(forms.ModelForm):
	content = forms.CharField(widget = forms.Textarea, required = False)
	
	class Meta:
		model = Edge
		fields = ('preamble', 'content', )
	
	def __init__(self, *args, **kwargs):
		super(Edit_Edge_Form, self).__init__(*args, **kwargs)
		edge = kwargs.pop('instance', None)
		self.fields['preamble'].queryset = Preamble.get_user_preambles(edge.user)
		self.initial['preamble'] = edge.preamble
		self.initial['content'] = edge.read_pre_dir()