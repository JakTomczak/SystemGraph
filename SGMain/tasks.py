import time
import subprocess
import codecs
import os

from celery import shared_task

from django.conf import settings

from . import compilation

@shared_task
def test(fcode = None, vertex_id = None, desc = False, edge_id = None, text = ''):
	cdata = CompilationData.objects.get(fcode = fcode)
	print('D--')
	compilation.compile_v1(cdata = cdata, vertex_id = vertex_id, desc = desc, edge_id = edge_id, text = text)
	
def test2():
	print( make4ht_compile('VALLLGXKSAdesc.tex', settings.COMP_DIR) )
	
def nocompiler(vertex, desc):
	if not desc:
		pre = vertex.get_pre_content_dir()
		fcode = vertex.vertex_id
	else:
		pre = vertex.get_pre_desc_dir()
		fcode = vertex.vertex_id + 'desc'
	with codecs.open( pre, 'r', encoding = 'utf-8') as file:
		text = file.read()
	dir = os.path.join(settings.COMP_DIR, fcode + '.txt')
	with codecs.open( dir, 'w+', encoding = 'utf-8') as file:
		file.truncate()
		file.write(text)
	if desc:
		vertex.desc_dir = dir
	else:
		vertex.content_dir = dir
		vertex.submitted = True
	vertex.save()
	
def use_noconverter (id, content, desc = False):
	if desc:
		fcode = id + 'desc'
	else:
		fcode = id
	dir = os.path.join(settings.COMP_DIR, fcode + '.txt')
	with codecs.open( dir, 'w+', encoding = 'utf-8') as file:
		file.truncate()
		file.write(content)
		return dir	

def start_make4ht_compilation(filename, cwd):
	print ('make4ht -uc mathjax.cfg -e config.mk4 ' + filename)
	proc = subprocess.Popen(['make4ht', '-uc', 'mathjax.cfg', '-e', 'config.mk4', filename], cwd = cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	return proc
	
def make4ht_compile(texfilename, cwd):	
	proc = start_make4ht_compilation (texfilename, cwd)
	errortext = b''
	error = False
	i = 0
	STILL = False
	for line in iter(proc.stdout.readline, b''):
		# print('got line: {0}'.format(line.decode('cp1252')), end='')
		if not error and line.startswith(b'!'):
			error = True
			STILL = True
		if line.startswith(b'Output'):
			STILL = False
		if error and i < 5 and STILL:
			errortext += line
			i += 1
			
	proc.wait()
	return errortext