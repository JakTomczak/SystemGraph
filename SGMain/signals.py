import os

from django.dispatch import receiver
from django.db.models import signals

from . import models
		
@receiver(signals.pre_delete, sender = models.Vertex)
def delete_vertex_files (sender, instance, using, **kwargs):
	instance.delete_pre_dirs()
	try:
		os.remove( instance.desc_dir )
	except FileNotFoundError:
		pass
	try:
		os.remove( instance.content_dir )
	except FileNotFoundError:
		pass
	PEs = models.Path_Entry.objects.filter(vertex = instance)
	for entry in PEs:
		path = entry.path
		next_ones = models.Path_Entry.objects.filter(path = path, index__gt = entry.index)
		for e in next_ones:
			e.index -= 1
			e.save()
		path.length -= 1
		entry.delete()
		if path.length < 1:
			path.delete()
		else:
			path.save()
	for path in models.Path.objects.filter(first = instance):
		path.first = models.Path_Entry.objects.filter(path = path, index = 1)[0].vertex
		path.save()
	models.CompilationData.objects.get(fcode = instance.vertex_id).delete()
	models.CompilationData.objects.get(fcode = instance.vertex_id + 'desc').delete()
		
@receiver(signals.post_save, sender = models.Vertex)
def add_vertex_compilation_objects (sender, instance, created, **kwargs):
	if created:
		instance.create_pre_dirs()
		cd1 = models.CompilationData(fcode = instance.vertex_id)
		cd1.save()
		cd2 = models.CompilationData(fcode = instance.vertex_id + 'desc')
		cd2.save()

@receiver(signals.pre_delete, sender = models.Preamble)
def delete_preamble_files (sender, instance, using, **kwargs):
	os.remove(instance.directory)
		
@receiver(signals.pre_delete, sender = models.Edge)
def delete_edge_files (sender, instance, using, **kwargs):
	instance.delete_pre_dir()
	try:
		os.remove( instance.directory )
	except (TypeError, FileNotFoundError):
		pass
	models.CompilationData.objects.get(fcode = instance.edge_id).delete()
		
@receiver(signals.post_save, sender = models.Edge)
def add_vertex_compilation_objects (sender, instance, created, **kwargs):
	if created:
		instance.create_pre_dir()
		models.CompilationData(fcode = instance.edge_id).save()