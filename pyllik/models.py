from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Pais(models.Model):
    nombre = models.CharField(max_length=30)
    def __unicode__(self):
        return self.nombre
class Persona(models.Model):
    nombre = models.CharField(max_length=30)
    apellidos = models.CharField(max_length=60)
    doc_tipo = models.CharField(max_length=10)
    doc_nro = models.CharField(max_length=10)
    pais = models.ForeignKey(Pais)
    edad = models.IntegerField()
    def __unicode__(self):
        return self.nombre
class Paquete(models.Model):
    nombre = models.CharField(max_length=20)
    precio = models.FloatField()
    descripcion = models.TextField()
    user = models.ForeignKey(User)
    creado = models.DateField()
    estado = models.BooleanField(default=True)
    def __unicode__(self):
        return self.nombre
class Reserva(models.Model):
    paquete = models.ForeignKey(Paquete)
    cantidad_personas = models.IntegerField(default=0)
    precio = models.FloatField()
    user = models.ForeignKey(User)
    creado = models.DateTimeField()
    estado = models.BooleanField(default=True)
    def __unicode__(self):
        return "Una reserva"
class ReservaDetalle(models.Model):
    reserva = models.ForeignKey(Reserva)
    persona = models.ForeignKey(Persona)
    def __unicode__(self):
        return "Detalle Reserva"
class Rubro(models.Model):
    nombre = models.CharField(max_length=120)
    def __unicode__(self):
        return self.nombre
class ContactoInfo(models.Model):
    direccion = models.CharField(max_length=120)
    def __unicode__(self):
        return self.direccion