import os, glob
import subprocess
import codecs
import time

from TexSoup import TexSoup
from bs4 import BeautifulSoup, Comment

from django.conf import settings
import django.core.exceptions as exceptions

import SGMain.models as model

def rreplace(s, old, new, occurrence):
	li = s.rsplit(old, occurrence)
	return new.join(li)
	
class SGlink (object):
	valid = True
	errortext = 'Error with sglink. '
	
	def __init__(self, vertex, link = None):
		if link is not None:
			try:
				t = link.args[0]
			except IndexError:
				self.errortext += '<sglink> takes exactly two arguments.'
				self.valid = False
				return
			try:
				e = link.args[1]
			except IndexError:
				self.errortext += '<sglink> takes exactly two arguments.'
				self.valid = False
				return
			try:
				edge = model.Edge.objects.get(edge_id = e)
			except exceptions.ObjectDoesNotExist:
				self.errortext += 'There is no edge with id {0}.'.format(e)
				self.valid = False
				return
			self.load(t, edge, vertex)
		
	def load(self, text, edge, vertex):
		if edge.predecessor != vertex:
			self.errortext += 'The edge {0} does not start in this vertex.'.format(e)
			self.valid = False
			return
		self.text = text
		self.edge_id = edge.edge_id
		
	def set_id(self, number):
		if number >= 100:
			self.errortext += 'Sorry, 100 sglinks of the same edge in single vertex is the limit.'
			self.valid = False
			return
		self.number = str(number).zfill(2)
		self.id = self.edge_id + '_' + self.number
		self.tag = '<a id="' + self.id + '" class="fancy-a">' + self.text + '</a>'
		
	def add_self(self, text):
		return text + self.edge_id + ',' + self.number + ';'
		
class CompilationCore(object):
	cwd = settings.COMP_DIR
	begin_document_file = settings.BEGINTEX_FILE
	end_document_file = settings.ENDTEX_FILE
	errortext = b''
	error = False
	pk = 'pk'
#	state = 'IDLE'
	_mode = 0
	
	def __init__(self, cdata, text = None, vertex_id = None, desc = False, edge_id = None):
		self.output = ''
		self.cdata = cdata
		if self.check_text(text):
			self.text = text
		else:
			return
		if vertex_id and edge_id:
			raise Exception('One compilation at a time please.')
		elif vertex_id:
			try:
				vertex = model.Vertex.objects.get(vertex_id = vertex_id)
			except exceptions.ObjectDoesNotExist:
				return
			else:
				self._load_vertex(vertex, desc)
		elif edge_id:
			try:
				edge = model.Edge.objects.get(edge_id = edge_id)
			except exceptions.ObjectDoesNotExist:
				return
			else:
				self._load_edge(edge)
		else:
			return
		
	# to do
	def check_text(self, text):
		return True
			
	def _load_vertex(self, vertex, desc):
		self._mode = 1
		self.object = vertex
		self.pk = 'vertex_id'
		self.fcode = vertex.vertex_id
		if desc:
			self._mode = 2
			self.fcode += 'desc'
		self.set_state('PROGRESS')
			
	def _load_edge(self, edge):
		self._mode = 3
		self.object = edge
		self.pk = 'edge_id'
		self.fcode = edge.edge_id
		self.set_state('PROGRESS')
	
	def log_info(self, info, **kwargs):
		print(info, **kwargs)
	
	def _log_progress(self, step, state, m):
		self.cdata.step = step
		self.cdata.state = state
		if m:
			self.cdata.add_message(m)
		self.cdata.save()
			
	def _log_error(self):
		self.error = True
		self.cdata.add_message('Compilation failed.', error = True)
		self.cdata.add_message(self.errortext)
		
	def _get_message(self, step):
		if self._mode == 1:
			if step == 1:
				return "Vertex's main content compilation begun."
		elif self._mode == 2:
			if step == 1:
				return "Vertex's description compilation begun."
		elif self._mode == 3:
			if step == 1:
				return "Edge's content compilation begun."
		return None
		
	def set_state(self, state, step = None):
		if step is None:
			step = self.cdata.step + 1
		m = self._get_message(step)
		self._log_progress(step, state, m)
		
	def prepare(self):
		if self._mode == 1:
			texsoup, sglinks, self.errortext = CompilationCore.get_sglinks(self.text, self.object)
			if self.errortext:
				self._log_error()
				return
			self.text = str(texsoup)
		self.set_state('PROGRESS')
		self.make_tex_file()
		self.set_state('PROGRESS')
		
	def make_tex_file(self, texfilename = None):
		if texfilename is None:
			self.texfilename = self.fcode + '.tex'
		else:
			self.texfilename = texfilename
		with codecs.open(self.object.preamble.directory, 'r', encoding = 'utf-8') as P:
			ptext = P.read()
		fulldir = os.path.join(self.cwd, self.texfilename)
		with open( fulldir, 'w+') as file:
			file.truncate()
			file.write(ptext)
			with open( self.begin_document_file, 'r') as temp:
				for line in temp:
					file.write(line)
			for line in self.text.splitlines():
				# log_info(line)
				file.write(line)
				file.write('\n')
			with open( self.end_document_file, 'r') as temp:
				for line in temp:
					file.write(line)
		
	@classmethod
	def get_sglinks(cls, textext, vertex):
		texsoup = TexSoup(textext)
		sglinks = []
		used_edges = {}
		for sgl in soup.find_all(name = 'sglink'):
			sglink = SGlink(vertex, sgl)
			if not sglink.valid:
				return texsoup, sglinks, sglink.errortext
			if sglink.edge_id in used_edges:
				used_edges[sglink.edge_id] += 1
			else:
				used_edges[sglink.edge_id] = 0
			sglink.set_id( used_edges[sglink.edge_id] )
			if not sglink.valid:
				return texsoup, sglinks, sglink.errortext
			while sglink.id in textext:	# for users who would put sglink id directly in their content
				used_edges[sglink.edge_id] += 1
				sglink.set_id( used_edges[sglink.edge_id] )
				if not sglink.valid:
					return texsoup, sglinks, sglink.errortext
			sgl.replace(sglink.id)
			sglinks.append( sglink )
		return texsoup, sglinks, None
		
	def run(self):
		self._run()
		if self.error:
			self.errortext = self.errortext.decode('utf-8')
			self._log_error()
			return
		self.set_state('PROGRESS')
		self.output = CompilationCore.work_on_output_html(self.cwd, self.fcode)
		if self._mode == 1:
			self.paste_sglinks()
		self.set_state('PROGRESS')
	
	def _run(self):
		self._make4ht()
		i = 0
		STILL = False
		for line in iter(self.process.stdout.readline, b''):
			# self.log_info('got line: {0}'.format(line.decode('cp1252')), end='')
			if not self.error and line.startswith(b'!'):
				self.error = True
				STILL = True
			if line.startswith(b'Output'):
				STILL = False
			if self.error and i < 5 and STILL:
				self.errortext += line
				i += 1	
		self.process.wait()
		
	def _make4ht(self):
		self.command = 'make4ht -uc mathjax.cfg -e config.mk4 ' + self.texfilename
		self.log_info(self.command)
		command_list = self.command.split(' ')
		self.process = subprocess.Popen(command_list, cwd = self.cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		
	@classmethod
	def work_on_output_html(cls, cwd, fcode):
		htmlfile = os.path.join( cwd, fcode + '.html' )
		with codecs.open( htmlfile, 'r', encoding = 'utf-8') as file:
			soup = BeautifulSoup( file.read(), 'html.parser' )
			comments = soup.findAll( text = lambda text:isinstance(text, Comment) )
			[comment.extract() for comment in comments]
			output = soup.body.prettify()
			output = output.replace('<body>', '<div class="postmake4ht">', 1)
			output = rreplace(output, '</body>', '</div>', 1)
		return output
		
	def paste_sglinks(self):
		t = ''
		for link in sglinks:
			self.output = self.output.replace(link.id, link.tag)
			t = link.add_self(t)
		self.object.write_sglinks(t, self.cwd)
		
	def clean_up(self, output_fulldir = None):
		if output_fulldir is None:
			self.outputfile = os.path.join(self.cwd, self.fcode + '.txt')
		else:
			self.outputfile = output_fulldir
		with codecs.open( self.outputfile, 'w+', encoding = 'utf-8') as file:
			file.truncate()
			file.write(self.output)
		self.set_state('PROGRESS')
		for filename in glob.glob( os.path.join(self.cwd, self.fcode) + '.*' ):
			if not filename.endswith('txt'):
				# log_info(filename)
				os.remove(filename)
		if self._mode == 1:
			self.object.content_dir = self.outputfile
			self.object.submitted = True
		if self._mode == 2:
			self.object.desc_dir = self.outputfile
		if self._mode == 3:
			self.object.directory = self.outputfile
		self.object.save()
		self.set_state('PROGRESS')
		
	@classmethod
	def empty_vdesc(cls, vertex_id):
		outputfile = os.path.join(settings.COMP_DIR, vertex_id + 'desc.txt')
		try:
			vertex = model.Vertex.objects.get(vertex_id = vertex_id)
		except exceptions.ObjectDoesNotExist:
			return
		with codecs.open( self.outputfile, 'w+', encoding = 'utf-8') as file:
			file.truncate()
		vertex.desc_dir = outputfile
		vertex.save()
	
def compile_v1(cdata = None, vertex_id = None, desc = False, edge_id = None, text = ''):
	print('D-')
	if cdata is None:
		return
	print('DA')
	cdata.launch()
	print('DB')
	ccore = CompilationCore(cdata, vertex_id = vertex_id, desc = desc, edge_id = edge_id, text = text)
	if not ccore.error:
		ccore.prepare()
	if not ccore.error:
		ccore.run()
	if not ccore.error:
		ccore.clean_up()
	if not ccore.error:
		cdata.close()