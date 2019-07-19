from django.apps import AppConfig


class SgmainConfig(AppConfig):
	name = 'SGMain'
	def ready(self):
		print("at ready")
		import SGMain.signals