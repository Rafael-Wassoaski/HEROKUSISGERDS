# Generated by Django 2.1 on 2020-02-18 17:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('relatorios', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='vistoria',
            name='foto',
            field=models.TextField(default='none'),
        ),
        migrations.AddField(
            model_name='vistoria',
            name='fotoCompilada',
            field=models.FileField(blank=True, null=True, upload_to=''),
        ),
    ]
