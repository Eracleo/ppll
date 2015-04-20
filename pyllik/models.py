# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from thumbs import ImageWithThumbsField
DOC_TIPO = (
    ('di','Document Identification'),
    ('ps','Passport'),
    )
PAGO_ESTADO = (
    ('re','En Reserva'),
    ('ad','Con Adelanto'),
    ('pc','Completado'),
    ('pc','Incompleto'),
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
class Rubro(models.Model):
    nombre = models.CharField(max_length=120)
    def __unicode__(self):
        return self.nombre
class Empresa(models.Model):
    rubro = models.ForeignKey(Rubro)
    razon_social = models.CharField(max_length=100)
    direccion = models.CharField(max_length=120)
    telefono = models.CharField(max_length=120, blank=True)
    ruc = models.CharField(max_length=11)
    web = models.URLField(max_length=64, blank=True)
    paypal_email = models.EmailField(max_length=100,help_text="E-mail relacionado con paypal")
    paypal_at = models.CharField(max_length=64,help_text="Código de identicacion en paypal") # IdentityToken
    nro_paquetes = models.IntegerField(default=5)
    logo = ImageWithThumbsField(upload_to='logos_empresa')
    terminos_condiciones = models.URLField(max_length=120, blank=True, help_text="URL Terminos y condiciones.")
    user = models.ForeignKey(User)
    abreviatura = models.CharField(max_length=3,unique=True)
    creado = models.DateField(auto_now_add=True, editable=False)
    editado = models.DateTimeField(auto_now=True, editable=False)
    def __unicode__(self):
        return self.razon_social
class Persona(models.Model):
    nombre = models.CharField(max_length=30)
    apellidos = models.CharField(max_length=60)
    doc_tipo = models.CharField(max_length=2, choices=DOC_TIPO)
    doc_nro = models.CharField(max_length=10)
    email = models.EmailField(max_length=60,blank=True)
    telefono = models.CharField(max_length=50, blank=True,help_text="Formato de Telefono: +512 123456789 o +51 123456789")
    pais = models.ForeignKey(Pais,null=True, blank=True)
    empresa = models.ForeignKey(Empresa,null=True, blank=True)
    creado = models.DateField(auto_now_add=True, editable=False)
    editado = models.DateTimeField(auto_now=True, editable=False)
    def __unicode__(self):
        return self.nombre
BOOL_CHOICES = ((True, 'Habitilido'), (False, 'Deshabilitado'))
class Paquete(models.Model):
    sku = models.CharField(max_length=6,unique=True)
    nombre = models.CharField(max_length=60,help_text="Coloque el nombre del paquete, tal como aparece en su sitio web.")
    precio = models.FloatField(default=0, validators=[MinValueValidator(0)],help_text="Coloque el precio del paquete, tal como aparece en su sitio web. Los precios son en Dólares Americanos (USD $)")
    porcentaje = models.FloatField(default=100, validators=[MinValueValidator(0),MaxValueValidator(100)],help_text="Coloque el porcentaje del Pre pago que el sistema va a cobrar por pasajero, el monto en USD $ se actualiza automáticamente.")
    pre_pago = models.FloatField(default=0, validators=[MinValueValidator(0)],help_text="Coloque el monto en USD $ del Pre pago que el sistema va a cobrar por pasajero, el monto en % se acutaliza automáticamente")
    descripcion = models.TextField(max_length=500, blank=True, help_text="Este es una pequeña descripción del paquete que está Ud. vendiendo. Debe concordar con lo que aparece en su página web.")
    empresa = models.ForeignKey(Empresa)
    link = models.URLField(max_length=120, blank=True, help_text="Coloque el link del Paquete que aparece en su página web. Verifique que sea el link correcto.")
    estado = models.BooleanField(default=True,choices=BOOL_CHOICES, help_text="Active el Estado si desea que este paquete este activo, si quita el check el paquete se desactivará y no podrá userse.")
    creado = models.DateField(auto_now_add=True, editable=False)
    editado = models.DateTimeField(auto_now=True, editable=False)
    def __unicode__(self):
        return self.nombre
class Reserva(models.Model):
    paquete = models.ForeignKey(Paquete)
    cantidad_personas = models.IntegerField()
    fecha_viaje = models.DateField()
    precio = models.FloatField(blank=True)
    pre_pago = models.FloatField(blank=True)
    modo_pago = models.CharField(max_length=2, choices=MODO_PAGO, default='pa')
    # llego_de = (recomendado, web, web_reserva, oficina)
    tx = models.CharField(max_length=64, blank=True)
    viajeros = models.ManyToManyField(Persona, blank=True)
    email = models.EmailField(max_length=100,blank=True)
    ip = models.GenericIPAddressField(null=True,blank=True)
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