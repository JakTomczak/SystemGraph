# Generated by Django 2.2.3 on 2019-07-19 11:54

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CompilationData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fcode', models.CharField(max_length=20, null=True)),
                ('last_end_time', models.DateTimeField(default=django.utils.timezone.now)),
                ('step', models.IntegerField(default=-1)),
                ('state', models.CharField(default='IDLE', max_length=30)),
                ('messages', models.TextField(default='')),
            ],
        ),
        migrations.CreateModel(
            name='CompilationLaunch',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Discipline',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('polish_name', models.CharField(default='Nienazwana dyscyplina', max_length=60)),
                ('is_default', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Edge',
            fields=[
                ('edge_id', models.CharField(default='EAAAAAAAAA', max_length=10, primary_key=True, serialize=False)),
                ('validated', models.BooleanField(default=False)),
                ('directory', models.CharField(max_length=200, null=True)),
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
            name='Path_Entry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('index', models.IntegerField()),
            ],
            options={
                'verbose_name_plural': 'Path Entries',
            },
        ),
        migrations.CreateModel(
            name='Preamble',
            fields=[
                ('preamble_id', models.CharField(default='AAAAAAAAAA', max_length=10, primary_key=True, serialize=False)),
                ('title', models.CharField(default='My preamble', max_length=60)),
                ('description', models.CharField(max_length=200, null=True)),
                ('directory', models.CharField(default='/home/jakub/git/SystemGraph/compilationfiles/AAAAAAAAAA.txt', max_length=200)),
                ('is_default', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('polish_name', models.CharField(default='Nienazwany temat', max_length=60)),
                ('is_default', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Vertex_Class',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('polish_name', models.CharField(default='Nienazwany wierzchołek', max_length=50)),
                ('polish_name_plural', models.CharField(default='Nienazwane wierzchołki', max_length=50)),
                ('is_default', models.BooleanField(default=False)),
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
                ('is_default', models.BooleanField(default=False)),
                ('discipline', models.ForeignKey(default=1, on_delete=django.db.models.deletion.SET_DEFAULT, to='SGMain.Discipline')),
                ('preamble', models.ForeignKey(default='AAAAAAAAAA', on_delete=django.db.models.deletion.SET_DEFAULT, to='SGMain.Preamble')),
                ('subject', models.ForeignKey(default=1, on_delete=django.db.models.deletion.SET_DEFAULT, to='SGMain.Subject')),
            ],
            options={
                'verbose_name_plural': 'Vertices',
            },
        ),
    ]
