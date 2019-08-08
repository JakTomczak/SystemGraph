from django.contrib import admin

from .models import *

admin.site.register(Vertex_Class, admin.ModelAdmin)
admin.site.register(Preamble, admin.ModelAdmin)
admin.site.register(Discipline, admin.ModelAdmin)
admin.site.register(Section, admin.ModelAdmin)
admin.site.register(Subject, admin.ModelAdmin)
admin.site.register(Vertex, admin.ModelAdmin)
admin.site.register(Edge_Class, admin.ModelAdmin)
admin.site.register(Edge, admin.ModelAdmin)
admin.site.register(Edge_Proposition, admin.ModelAdmin)
admin.site.register(Path, admin.ModelAdmin)
admin.site.register(Path_Entry, admin.ModelAdmin)
admin.site.register(CompilationData, admin.ModelAdmin)
admin.site.register(CompilationLaunch, admin.ModelAdmin)