import datetime

from django.db import models
import django.core.exceptions as exceptions
import django.utils.timezone as timezone

import SGMain.tools as tools

class CompilationData(models.Model):
	fcode = models.CharField(max_length = 20, null = True)
	last_end_time = models.DateTimeField(default = timezone.now)
	step = models.IntegerField(default = -1)
	state = models.CharField(max_length = 30, default = "IDLE")
	messages = models.TextField(default = '')
	
	def __str__(self):
		return self.fcode
		
	def launch(self):
		CompilationLaunch(compilation = self).save()
		self.step = 0
		self.save()
		
	def add_message(self, m, error = False):
		if m:
			while ';;' in m:
				m.replace(';;', ';')
			self.messages += m + ';;'
			if error:
				self.state = "ERROR"
			self.save()
			
	def read_messages(self):
		return self.messages.split(';;')[:-1]
			
	def close(self):
		self.state = "CLOSED"
		self.last_end_time = timezone.now()
		self.add_message('Compilation successful')
	
	def clean(self):
		self.step = -1
		self.state = "IDLE"
		self.messages = ''
		self.last_end_time = timezone.now()
		self.save()
	
	@classmethod
	def check_if_idle(cls, vertex_id = None, desc = False, edge_id = None):
		fcode = tools.fcode_from_id(vertex_id = vertex_id, desc = desc, edge_id = edge_id)
		try:
			cdata = CompilationData.objects.get(fcode = fcode)
		except exceptions.ObjectDoesNotExist:
			return 'Niewłaściwy fcode'
		now = timezone.now()
		if cdata.state == "CLOSED" and now > cdata.last_end_time + datetime.timedelta(seconds = 8):
			cdata.clean()
			return ''
		if cdata.step != -1:
			return 'Kompilacja w toku.'
		if now < cdata.last_end_time + datetime.timedelta(seconds = 5):
			return 'Zaczekaj chwilę pomiędzy kompilacjami.'
		minutes_ago = now - datetime.timedelta(minutes = 5)
		launches = CompilationLaunch.objects.filter(compilation = cdata, time__gte = minutes_ago)
		if len(launches) >= 10:
			return 'Możesz uruchamiać kompilację jedynie 10 razy w ciągu 5 minut.'
		return ''
	
	# returns (still_running, error, m) where m is one ise message or list of compilation messages
	@classmethod
	def check_status(cls, vertex_id = None, desc = False, edge_id = None):
		fcode = tools.fcode_from_id(vertex_id = vertex_id, desc = desc, edge_id = edge_id)
		try:
			cdata = CompilationData.objects.get(fcode = fcode)
		except exceptions.ObjectDoesNotExist:
			return False, True, 'Internal server error A'
		if cdata.state == "IDLE":
			return False, False, []
		else:
			m = cdata.read_messages()
			if cdata.state == "CLOSED":
				cdata.clean()
				return False, False, m
			if cdata.state == "ERROR":
				cdata.clean()
				return False, True, m
			return True, False, m
		
class CompilationLaunch(models.Model):
	compilation = models.ForeignKey(CompilationData, on_delete = models.CASCADE)
	time = models.DateTimeField(auto_now_add = True)
	
	class Meta:
		verbose_name_plural = "Compilation launches"
	
	def __str__(self):
		return str(self.compilation)