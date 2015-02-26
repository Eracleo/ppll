from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Pais(models.Model):
    nombre = models.CharField(max_length=30)
    def __unicode__(self):
        return self.nombre
DOC_TIPO = (
    ('dni','DNI'),
    ('pas','Passport'),
    )
class Persona(models.Model):
    nombre = models.CharField(max_length=30)
    apellidos = models.CharField(max_length=60)
    doc_tipo = models.CharField(max_length=3, choices=DOC_TIPO)
    doc_nro = models.CharField(max_length=10)
    pais = models.ForeignKey(Pais)
    # edad = models.IntegerField()
    creado = models.DateField(auto_now_add=True)
    email = models.CharField(blank=True)
    telefono = models.CharField(max_length=50, blank=True)
    cod_telefono = models.CharField(max_length=10, blank=True)
    def __unicode__(self):
        return self.nombre
class Paquete(models.Model):
    nombre = models.CharField(max_length=20)
    precio = models.FloatField(default=0)
    adelanto =models.FloatField(default=0) # Adelanto de pago
    descripcion = models.TextField(blank=True)
    user = models.ForeignKey(User)
    creado = models.DateField(auto_now_add=True, editable=False)
    estado = models.BooleanField(default=True)
    link = models.CharField(max_length=120)
    def __unicode__(self):
        return self.nombre
class Reserva(models.Model):
    paquete = models.ForeignKey(Paquete)
    cantidad_personas = models.IntegerField(default=0)
    fecha_viaje = models.DateField()
    precio = models.FloatField(default=0)
    user = models.ForeignKey(User)
    creado = models.DateTimeField(auto_now_add=True, editable=False)
    estado = models.BooleanField(default=True)
    def save(self, *args, **kwargs):
        self.user = self.paquete.user
        super(Reserva,self).save(*args,**kwargs)
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
    razon_social = models.CharField(max_length=100)
    direccion = models.CharField(max_length=120)
    ruc = models.CharField(max_length=11)
    web = models.CharField(max_length=64)
    paypal_email = models.CharField(max_length=100)
    paypal_code = models.CharField(max_length=50)
    user = models.ForeignKey(User)
    def __unicode__(self):
        return self.direccion