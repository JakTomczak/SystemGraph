import os

from django.dispatch import receiver
from django.db.models.signals import pre_delete, post_save
import django.core.exceptions as exceptions

from SGMain.models import *

# post_save.connect(create_activity_item, sender=Status, dispatch_uid="create_activity_item")

@receiver(pre_delete, sender = Vertex)
def delete_vertex_files (sender, instance, using, **kwargs):
	instance.delete_pre_dirs()
	try:
		os.remove( instance.desc_dir )
	except (TypeError, FileNotFoundError):
		pass
	try:
		os.remove( instance.content_dir )
	except (TypeError, FileNotFoundError):
		pass
	PEs = Path_Entry.objects.filter(vertex = instance)
	for entry in PEs:
		path = entry.path
		next_ones = Path_Entry.objects.filter(path = path, index__gt = entry.index)
		for e in next_ones:
			e.index -= 1
			e.save()
		path.length -= 1
		entry.delete()
		if path.length < 1:
			path.delete()
		else:
			path.save()
	for path in Path.objects.filter(first = instance):
		path.first = Path_Entry.objects.filter(path = path, index = 1)[0].vertex
		path.save()
	try:
		CompilationData.objects.get(fcode = instance.vertex_id).delete()
	except exceptions.ObjectDoesNotExist:
		pass
	try:
		CompilationData.objects.get(fcode = instance.vertex_id + 'desc').delete()
	except exceptions.ObjectDoesNotExist:
		pass
		
@receiver(post_save, sender = Vertex)
def add_vertex_compilation_objects (sender, instance, created, **kwargs):
	print('abba')
	print(created)
	if created:
		instance.create_pre_dirs()
		cd1 = CompilationData(fcode = instance.vertex_id)
		cd1.save()
		cd2 = CompilationData(fcode = instance.vertex_id + 'desc')
		cd2.save()

@receiver(pre_delete, sender = Preamble)
def delete_preamble_files (sender, instance, using, **kwargs):
	os.remove(instance.directory)
		
@receiver(pre_delete, sender = Edge)
def delete_edge_files (sender, instance, using, **kwargs):
	instance.delete_pre_dir()
	try:
		os.remove( instance.directory )
	except (TypeError, FileNotFoundError):
		pass
	CompilationData.objects.get(fcode = instance.edge_id).delete()
		
@receiver(post_save, sender = Edge)
def add_edge_compilation_objects (sender, instance, created, **kwargs):
	if created:
		instance.create_pre_dir()
		CompilationData(fcode = instance.edge_id).save()