import os

from django.shortcuts import render

import SGMain.models as model
from users.models import CustomUser

def new_vertex(request):
	if not request.user or request.user.is_anonymous:
		return render(request, 'errors/401.html')
	if request.method == 'POST':
		form = forms.Add_New_Vertex_Form(request.POST, user = request.user)
		if 'save' in request.POST and form.is_valid():
			vertex = form.save(commit = False)
			vertex.user = request.user
			vid = tools.id_generator('V')
			while len( model.Vertex.objects.filter(vertex_id = vid) ):
				vid = tools.id_generator('V')
			vertex.vertex_id = vid
			dir = request.user.folder
			open( os.path.join(dir, vid + '.txt'), 'w+').close()
			open( os.path.join(dir, vid + 'desc.txt'), 'w+').close()
			vertex.save()
			messages.add_message(request, messages.SUCCESS, 'New vertex has been added.')
			return redirect('edit_vertex', vertex = vid)
	else:
		form = forms.Add_New_Vertex_Form(user = request.user)
	context = {'form': form}
	return render(request, 'graph/add_new_vertex.html', context)