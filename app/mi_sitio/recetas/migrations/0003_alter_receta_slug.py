# Generated by Django 4.1.1 on 2022-12-16 11:40

import autoslug.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recetas', '0002_receta_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='receta',
            name='slug',
            field=autoslug.fields.AutoSlugField(editable=False, populate_from='nombre', unique=True),
        ),
    ]
