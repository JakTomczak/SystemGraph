# Generated by Django 2.2.2 on 2019-06-26 11:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Discipline',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('polish_name', models.CharField(default='Nienazwana dyscyplina', max_length=60)),
            ],
        ),
        migrations.CreateModel(
            name='Edge_Class',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('polish_name', models.CharField(default='Nienazwana krawędź', max_length=60)),
            ],
            options={
                'verbose_name_plural': 'Edge Classes',
            },
        ),
        migrations.CreateModel(
            name='Path',
            fields=[
                ('path_id', models.CharField(default='TAAAAAAAAA', max_length=10, primary_key=True, serialize=False)),
                ('name', models.CharField(default='Nienazwana ścieżka', max_length=50)),
                ('description', models.CharField(max_length=200, null=True)),
                ('date', models.DateField(auto_now=True)),
                ('length', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Preamble',
            fields=[
                ('preamble_id', models.CharField(default='AAAAAAAAAA', max_length=10, primary_key=True, serialize=False)),
                ('title', models.CharField(default='My preamble', max_length=60)),
                ('description', models.CharField(max_length=200, null=True)),
                ('directory', models.CharField(default='C:\\Users\\Jakub\\git\\SystemGraph\\static\\AAAAAAAAAA.txt', max_length=200)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('polish_name', models.CharField(default='Nienazwany temat', max_length=60)),
            ],
        ),
        migrations.CreateModel(
            name='Vertex_Class',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('polish_name', models.CharField(default='Nienazwany wierzchołek', max_length=50)),
                ('polish_name_plural', models.CharField(default='Nienazwane wierzchołki', max_length=50)),
                ('bottom', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='onbottom', to='SGMain.Vertex_Class')),
                ('left', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='onleft', to='SGMain.Vertex_Class')),
                ('right', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='onright', to='SGMain.Vertex_Class')),
                ('top', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='ontop', to='SGMain.Vertex_Class')),
            ],
            options={
                'verbose_name_plural': 'Vertexes Classes',
            },
        ),
        migrations.CreateModel(
            name='Vertex',
            fields=[
                ('vertex_id', models.CharField(default='VAAAAAAAAA', max_length=10, primary_key=True, serialize=False)),
                ('date', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(default='default title', max_length=120)),
                ('shorttitle', models.CharField(blank=True, max_length=40, null=True)),
                ('submitted', models.BooleanField(default=False)),
                ('desc_dir', models.CharField(max_length=200, null=True)),
                ('content_dir', models.CharField(max_length=200, null=True)),
                ('discipline', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='SGMain.Discipline')),
                ('preamble', models.ForeignKey(default='AAAAAAAAAA', on_delete=django.db.models.deletion.SET_DEFAULT, to='SGMain.Preamble')),
                ('subject', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='SGMain.Subject')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('vertex_class', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='SGMain.Vertex_Class')),
            ],
            options={
                'verbose_name_plural': 'Vertices',
            },
        ),
        migrations.CreateModel(
            name='Path_Entry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('index', models.IntegerField()),
                ('path', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='SGMain.Path')),
                ('vertex', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='SGMain.Vertex')),
            ],
            options={
                'verbose_name_plural': 'Path Entries',
            },
        ),
        migrations.AddField(
            model_name='path',
            name='first',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='SGMain.Vertex'),
        ),
        migrations.AddField(
            model_name='path',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='Edge',
            fields=[
                ('edge_id', models.CharField(default='EAAAAAAAAA', max_length=10, primary_key=True, serialize=False)),
                ('validated', models.BooleanField(default=False)),
                ('directory', models.CharField(max_length=200, null=True)),
                ('links', models.CharField(blank=True, max_length=200)),
                ('edge_class', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='SGMain.Edge_Class')),
                ('preamble', models.ForeignKey(default='AAAAAAAAAA', on_delete=django.db.models.deletion.SET_DEFAULT, to='SGMain.Preamble')),
                ('predecessor', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='predecessor', to='SGMain.Vertex')),
                ('successor', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='successor', to='SGMain.Vertex')),
                ('user', models.ForeignKey(default=1, on_delete=django.db.models.deletion.SET_DEFAULT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]