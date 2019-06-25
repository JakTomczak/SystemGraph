
from django.shortcuts import render

from users.models import CustomUser

def ONE_MORE_TIME ():
	Users = CustomUser.objects.all()
	for user in Users:
		user.folder = None
		user.get_folder()
		user.save()
	# Prems = model.Preamble.objects.all()
	# for P in Prems:
		# P.directory = os.path.join( P.user.folder, P.preamble_id + '.tex' )
		# P.save()
	# Verts = model.Vertex.objects.all()
	# for V in Verts:
		# V.content_dir = os.path.join( settings.PUF_DIR, V.vertex_id + '.txt' )
		# if V.desc_dir:
			# V.desc_dir = os.path.join( settings.PUF_DIR, V.vertex_id + 'desc.txt' )
		# V.save()
	# Edges = model.Edge.objects.all()
	# for E in Edges:
		# E.directory = os.path.join( settings.PUF_DIR, E.edge_id + '.txt' )
		# E.save()
	# A = model.Preamble.objects.get(preamble_id = 'AAAAAAAAAA')
	# A.directory = os.path.join( settings.BASE_DIR, 'static', 'AAAAAAAAAA.tex' )
	# A.save()
	# B = model.Preamble.objects.get(preamble_id = 'AAAAAAAAAB')
	# B.directory = os.path.join( settings.BASE_DIR, 'static', 'AAAAAAAAAB.tex' )
	# B.save()

def frontpage(request):
	return render(request, 'common/frontpage.html', {})
	
def profile(request, username):
	return render(request, 'common/profile_thisuser.html', {})
	
def SearchSite(request):
	return render(request, 'common/search_vertexes.html', {})