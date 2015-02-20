from django.db import models

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
    # link = models.UrlField()
    creado = models.DateField()
    def __unicode__(self):
        return self.nombre
class Evento(models.Model):
    fecha_viaje = models.DateField()
    paquete = models.ForeignKey(Paquete)
    def __unicode__(self):
        return "Es un viaje"
class Reserva(models.Model):
    creado = models.DateTimeField()
    precio = models.FloatField()
    pagado = models.FloatField()
class ReservaDetalle(models.Model):
    evento = models.ForeignKey(Evento)
    persona = models.ForeignKey(Persona)
    reserva = models.ForeignKey(Reserva)
    precio = models.FloatField()
    def __unicode__(self):
        return "detalle reserva"