from django.apps import AppConfig


class SgmainConfig(AppConfig):
	name = 'SGMain'
	def ready(self):
		import SGMain.signals