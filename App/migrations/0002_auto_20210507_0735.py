# Generated by Django 3.1.7 on 2021-05-07 07:35

import ckeditor.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='grade',
            name='homeWork',
        ),
        migrations.RemoveField(
            model_name='grade',
            name='student',
        ),
        migrations.AddField(
            model_name='grade',
            name='solution',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='App.studentsolution'),
        ),
        migrations.AddField(
            model_name='studentsolution',
            name='homeWork',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='App.homework'),
        ),
        migrations.AddField(
            model_name='studentsolution',
            name='teacher',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='App.teacher'),
        ),
        migrations.AlterField(
            model_name='grade',
            name='teacherComment',
            field=ckeditor.fields.RichTextField(blank=True),
        ),
        migrations.AlterField(
            model_name='homework',
            name='homeWorkContent',
            field=ckeditor.fields.RichTextField(blank=True),
        ),
        migrations.AlterField(
            model_name='studies',
            name='contentLink',
            field=ckeditor.fields.RichTextField(blank=True),
        ),
        migrations.AlterField(
            model_name='teachermessage',
            name='teacher',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='App.teacher'),
        ),
    ]
