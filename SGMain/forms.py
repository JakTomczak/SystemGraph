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
			
class Edit_Vertex_Form (forms.Form):
	title = forms.CharField(max_length = 120)
	preamble = forms.ModelChoiceField( queryset = Preamble.objects.none(), empty_label = None )
	vertex_class = forms.ModelChoiceField( queryset = Vertex_Class.objects.all(), empty_label = None )
	discipline = forms.ModelChoiceField( queryset = Discipline.objects.all(), empty_label = None )
	subject = forms.ModelChoiceField( queryset = Subject.objects.all(), empty_label = None )
	description = forms.CharField(widget = forms.Textarea, required = False)
	content = forms.CharField(widget = forms.Textarea, required = False)
	ifshorttitle = forms.BooleanField(required = False)
	shorttitle = forms.CharField(max_length = 40, required = False)
	
	def __init__(self, *args, **kwargs):
		vertex = kwargs.pop('vertex', None)
		super(Edit_Vertex_Form, self).__init__(*args, **kwargs)
		user = vertex.user
		self.fields['preamble'].queryset = Preamble.get_user_preambles(user)
		
		self.initial['title'] = vertex.title
		self.initial['preamble'] = vertex.preamble
		self.initial['vertex_class'] = vertex.vertex_class
		self.initial['discipline'] = vertex.discipline
		self.initial['subject'] = vertex.subject
		with codecs.open( vertex.get_pre_content_dir(), 'r', encoding = 'utf-8') as file:
			self.initial['content'] = file.read()
		with codecs.open( vertex.get_pre_desc_dir(), 'r', encoding = 'utf-8') as file:
			self.initial['description'] = file.read()
		if vertex.shorttitle:
			self.initial['ifshorttitle'] = True
			self.initial['shorttitle'] = vertex.shorttitle
		else:
			self.initial['ifshorttitle'] = False
			
class Add_New_Discipline_Form(forms.ModelForm):
	polish_name = forms.CharField(max_length = 60)
	
	class Meta:
		model = Discipline
		fields = ('polish_name', )
			
class Add_New_Subject_Form(forms.ModelForm):
	polish_name = forms.CharField(max_length = 60)
	
	class Meta:
		model = Subject
		fields = ('polish_name', )
			
class Add_New_Preamble_Form(forms.ModelForm):
	title = forms.CharField(max_length = 60)
	description = forms.CharField(widget = forms.Textarea, required = False)
	content = forms.CharField(widget = forms.Textarea, required = False)
	
	class Meta:
		model = Preamble
		fields = ('title', 'description')
			
class Edit_Preamble_Form(forms.Form):
	title = forms.CharField(max_length = 60)
	description = forms.CharField(widget = forms.Textarea, required = False)
	content = forms.CharField(widget = forms.Textarea, required = False)
	
	def __init__(self, *args, **kwargs):
		preamble = kwargs.pop('preamble', None)
		super(Edit_Preamble_Form, self).__init__(*args, **kwargs)
		self.initial['title'] = preamble.title
		self.initial['description'] = preamble.description
		self.initial['content'] = preamble.read()

class Add_New_Vertex_Class_Form(forms.Form):
	polish_name = forms.CharField(max_length = 50, required = False)
	polish_name_plural = forms.CharField(max_length = 50, required = False)
	left = forms.CharField(max_length = 50)
	right = forms.CharField(max_length = 50)
	top = forms.CharField(max_length = 50)
	bottom = forms.CharField(max_length = 50)
	info = forms.CharField(widget = forms.Textarea, required = False)
			
class Edit_Edge_Form(forms.Form):
	preamble = forms.ModelChoiceField( queryset = Preamble.objects.none(), empty_label = None )
	content = forms.CharField(widget = forms.Textarea, required = False)
	
	def __init__(self, *args, **kwargs):
		edge = kwargs.pop('edge', None)
		super(Edit_Edge_Form, self).__init__(*args, **kwargs)
		self.fields['preamble'].queryset = Preamble.get_user_preambles(edge.user)
		self.initial['preamble'] = edge.preamble
		self.initial['content'] = edge.read_pre_dir()
			
class Add_New_Path_Form(forms.Form):
	name = forms.CharField(max_length = 50)
	description = forms.CharField(widget = forms.Textarea, max_length = 200, required = False)
			
class Edit_Path_Form(forms.Form):
	name = forms.CharField(max_length = 50)
	description = forms.CharField(widget = forms.Textarea, max_length = 200, required = False)
	
	def __init__(self, *args, **kwargs):
		path = kwargs.pop('path', None)
		super(Edit_Path_Form, self).__init__(*args, **kwargs)
		self.initial['name'] = path.name
		self.initial['description'] = path.description