from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
DOC_TIPO = (
    ('di','Document Identification'),
    ('ps','Passport'),
    )
PAGO_ESTADO = (
    ('re','En Reserva'),
    ('ad','Con Adelanto'),
    ('pc','Pago Completado'),
    ('ca','Cancelado'),
    )
MODO_PAGO = (
    ('pa','Paypay'),
    ('wu','Wester Union'),
    ('ba','Banco'),
    ('pe','Presencial'),
    ('ot','Otros'),
    )
class Pais(models.Model):
    nombre = models.CharField(max_length=30)
    def __unicode__(self):
        return self.nombre
class Persona(models.Model):
    nombre = models.CharField(max_length=30)
    apellidos = models.CharField(max_length=60)
    doc_tipo = models.CharField(max_length=2, choices=DOC_TIPO)
    doc_nro = models.CharField(max_length=10)
    email = models.EmailField(max_length=60,blank=True)
    cod_telefono = models.CharField(max_length=5, blank=True)
    telefono = models.CharField(max_length=50, blank=True)
    pais = models.ForeignKey(Pais, null=True, blank=True)
    creado = models.DateField(auto_now_add=True, editable=False)
    editado = models.DateTimeField(auto_now=True, editable=False)
    def __unicode__(self):
        return self.nombre

class Rubro(models.Model):
    nombre = models.CharField(max_length=120)
    def __unicode__(self):
        return self.nombre
class Empresa(models.Model):
    rubro = models.ForeignKey(Rubro)
    razon_social = models.CharField(max_length=100)
    direccion = models.CharField(max_length=120)
    ruc = models.CharField(max_length=11)
    web = models.URLField(max_length=64, blank=True)
    paypal_email = models.EmailField(max_length=100)
    paypal_code = models.CharField(max_length=50)
    nro_paquetes = models.IntegerField(default=1)
    logo = models.CharField(max_length=120, blank=True)
    user = models.ForeignKey(User)
    abreviatura = models.CharField(max_length=3)
    creado = models.DateField(auto_now_add=True, editable=False)
    editado = models.DateTimeField(auto_now=True, editable=False)
    def __unicode__(self):
        return self.razon_social
class Paquete(models.Model):
    sku = models.CharField(max_length=6)
    nombre = models.CharField(max_length=20)
    precio = models.FloatField(default=0, validators=[MinValueValidator(0)])
    porcentaje = models.FloatField(default=100, validators=[MinValueValidator(0),MaxValueValidator(100)])
    pre_pago = models.FloatField(default=0, validators=[MinValueValidator(0)])
    descripcion = models.TextField(max_length=500)
    empresa = models.ForeignKey(Empresa)
    link = models.URLField(max_length=120, blank=True)
    estado = models.BooleanField(default=True)
    creado = models.DateField(auto_now_add=True, editable=False)
    editado = models.DateTimeField(auto_now=True, editable=False)
    def __unicode__(self):
        return self.nombre
class Reserva(models.Model):
    paquete = models.ForeignKey(Paquete)
    cantidad_personas = models.IntegerField(default=0)
    fecha_viaje = models.DateField()
    precio = models.FloatField(blank=True)
    pre_pago = models.FloatField(blank=True)
    modo_pago = models.CharField(max_length=2, choices=MODO_PAGO, default='pa')
    # llego_de = (recomendado, web, web_reserva, oficina)
    tx = models.CharField(max_length=64, blank=True)
    viajeros = models.ManyToManyField(Persona, blank=True)
    email = models.EmailField(max_length=100,blank=True)
    empresa = models.ForeignKey(Empresa)
    pago_estado = models.CharField(max_length=2, choices=PAGO_ESTADO, default='re')
    creado = models.DateTimeField(auto_now_add=True, editable=False)
    def save(self, *args, **kwargs):
        self.empresa = self.paquete.empresa
        self.pre_pago = self.paquete.pre_pago
        self.precio = self.paquete.precio
        super(Reserva,self).save(*args,**kwargs)
    def __unicode__(self):
        return "Una reserva de "+self.email