
import datetime

from django.db import models
import django.core.exceptions as exceptions
import django.utils.timezone as timezone
from django.contrib.postgres.fields import ArrayField

class CompilationData(models.Model):
	fcode = models.CharField(max_length = 20, null = True)
	last_end_time = models.DateTimeField(default = timezone.now)
	step = models.IntegerField(default = -1)
	state = models.CharField(max_length = 30, default = "IDLE")
	messages = models.TextField(default = '')
	
	def check_if_idle(self):
		now = timezone.now()
		if self.state == "CLOSING" and now > self.last_end_time + datetime.timedelta(seconds = 12):
			self.clean()
		if self.step != -1:
			return 'Kompilacja w toku.'
		if now < self.last_end_time + datetime.timedelta(seconds = 4):
			return 'Zaczekaj chwilę pomiędzy kompilacjami.'
		minutes_ago = now - datetime.timedelta(minutes = 4)
		launches = CompilationLaunch.objects.filter(compilation = self, time__gte = minutes_ago)
		if len(launches) >= 10:
			return 'Możesz uruchamiać kompilację jedynie 10 razy w ciągu 4 minut.'
		return ''
		
	def launch(self):
		self.step = 0
		self.save()
		cl = CompilationLaunch(compilation = self)
		cl.save()
		
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
#		return self.messages.split(';;') or []
#		m = self.messages.split(';;')
#		if m :
#			return m[:-1]
#		else:
#			return []
			
	def close(self):
		self.state = "CLOSED"
		self.last_end_time = timezone.now()
		self.add_message('Compilation successful')
		#self.save()
	
	def clean(self):
		self.step = -1
		self.state = "IDLE"
		self.messages = ''
		self.last_end_time = timezone.now()
		self.save()
	
	# returns (still_running, error, m) where m is one ise message or list of compilation messages
	@classmethod
	def check_status(cls, fcode):
		try:
			cdata = CompilationData.objects.get(fcode = fcode)
		except exceptions.ObjectDoesNotExist:
			return False, True, 'Internal server error A'
		# now = timezone.now()
		if cdata.state == "CLOSED":
			m = cdata.read_messages()
			cdata.clean()
			return False, False, m
		elif cdata.state == "ERROR":
			m = cdata.read_messages()
			cdata.clean()
			return False, True, m
		elif cdata.state == "IDLE":
			return False, False, []
		return True, False, cdata.read_messages()
		
class CompilationLaunch(models.Model):
	compilation = models.ForeignKey(CompilationData, on_delete = models.CASCADE)
	time = models.DateTimeField(auto_now_add = True)