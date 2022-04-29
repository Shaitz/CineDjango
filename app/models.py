"""
Definition of models.
"""

from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator

class Pelicula(models.Model):
	titulo = models.CharField(max_length=100)
	direccion = models.CharField(max_length=60)
	anio = models.IntegerField(validators=[MaxValueValidator(99999999999)])
	genero = models.CharField(max_length=60)
	sinopsis = models.CharField(max_length=700)
	votos = models.IntegerField(validators=[MaxValueValidator(99999999999)])

	def __unicode__(self):
		return self.titulo

class Critico(models.Model):
	usuario_id = models.ForeignKey(User,on_delete=models.CASCADE)
	favoritas = models.ManyToManyField(Pelicula)

	def __unicode__(self):
		return unicode(self.usuario_id)