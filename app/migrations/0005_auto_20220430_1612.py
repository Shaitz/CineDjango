# Generated by Django 2.2.28 on 2022-04-30 14:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_genero'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pelicula',
            name='genero',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='app.Genero'),
        ),
    ]
