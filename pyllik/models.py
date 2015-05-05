# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from thumbs import ImageWithThumbsField
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
    ruc = models.CharField(max_length=11)
    direccion = models.CharField(max_length=120)
    telefono = models.CharField(max_length=120, blank=True)
    claro = models.CharField(max_length=20, blank=True)
    movistar = models.CharField(max_length=20, blank=True)
    email = models.EmailField(max_length=64, blank=True)
    web = models.URLField(max_length=64, blank=True)
    logo = ImageWithThumbsField(upload_to='logos_empresa', sizes=((150,50),))
    terminos_condiciones = models.URLField(max_length=120, blank=True, help_text="URL Terminos y condiciones.")
    abreviatura = models.CharField(max_length=3,unique=True)
    paypal_email = models.EmailField(max_length=100,help_text="E-mail relacionado con paypal")
    paypal_at = models.CharField(max_length=64,help_text="Código de identicacion en paypal") # IdentityToken
    code = models.CharField(max_length=32,blank=True,editable=False)
    owner = models.ForeignKey(User,related_name='owner')
    trabajadores = models.ManyToManyField(User)
    creado = models.DateField(auto_now_add=True, editable=False)
    editado = models.DateTimeField(auto_now=True, editable=False)
    def __unicode__(self):
        return self.razon_social
class TipoDocumento(models.Model):
    nombre = models.CharField(max_length=30)
    def __unicode__(self):
        return self.nombre
class Trabajador(models.Model):
    direccion = models.CharField(max_length=60)
    user = models.ForeignKey(User)
    empresa = models.ForeignKey(Empresa)
    doc_tipo = models.ForeignKey(TipoDocumento)
    doc_nro = models.CharField(max_length=10)
    def __unicode__(self):
        return self.user
class Pasajero(models.Model):
    nombre = models.CharField(max_length=30)
    apellidos = models.CharField(max_length=60)
    doc_tipo = models.ForeignKey(TipoDocumento)
    doc_nro = models.CharField(max_length=10)
    email = models.EmailField(max_length=60,blank=True)
    telefono = models.CharField(max_length=50, blank=True,help_text="Formato de Telefono: +512 123456789 o +51 123456789")
    pais = models.ForeignKey(Pais,null=True, blank=True)
    empresa = models.ForeignKey(Empresa,null=True, blank=True,editable=False)
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
    empresa = models.ForeignKey(Empresa,editable=False)
    link = models.URLField(max_length=120, blank=True, help_text="Coloque el link del Paquete que aparece en su página web. Verifique que sea el link correcto.")
    estado = models.BooleanField(default=True,choices=BOOL_CHOICES, help_text="Active el Estado si desea que este paquete este activo, si quita el check el paquete se desactivará y no podrá userse.")
    creado = models.DateField(auto_now_add=True, editable=False)
    editado = models.DateTimeField(auto_now=True, editable=False)
    def __unicode__(self):
        return self.nombre
class TipoCliente(models.Model):
    nombre = models.CharField(max_length=30)
    def __unicode__(self):
        return self.nombre
class Cliente(models.Model):
    nombre = models.CharField(max_length=30,blank=True)
    apellidos = models.CharField(max_length=60,blank=True)
    doc_tipo = models.ForeignKey(TipoDocumento,null=True,blank=True)
    doc_nro = models.CharField(max_length=10,blank=True)
    email = models.EmailField(max_length=60)
    telefono = models.CharField(max_length=50, blank=True)
    celular = models.CharField(max_length=50, blank=True)
    pais = models.ForeignKey(Pais,null=True, blank=True)
    empresa = models.ForeignKey(Empresa,editable=False)
    creado = models.DateField(auto_now_add=True, editable=False)
    editado = models.DateTimeField(auto_now=True, editable=False)
    def __unicode__(self):
        return self.email
class Pregunta(models.Model):
    pregunta = models.TextField()
    cliente = models.ForeignKey(Cliente)
    user = models.ForeignKey(User)
    empresa = models.ForeignKey(Empresa)
    creado = models.DateTimeField(auto_now_add=True, editable=False)
    estado = models.BooleanField(default=True)
    def __unicode__(self):
        return "Pregunta"
class Respuesta(models.Model):
    pregunta = models.TextField()
    cliente = models.ForeignKey(Cliente)
    user = models.ForeignKey(User)
    empresa = models.ForeignKey(Empresa)
    creado = models.DateTimeField(auto_now_add=True, editable=False)
    editado = models.DateTimeField(auto_now=True, editable=False)
    def __unicode__(self):
        return "Pregunta"
class FormaPago(models.Model):
    nombre = models.CharField(max_length=30)
    def __unicode__(self):
        return self.nombre
class EstadoPago(models.Model):
    nombre = models.CharField(max_length=30)
    def __unicode__(self):
        return self.nombre
class EstadoReserva(models.Model):
    nombre = models.CharField(max_length=30)
    def __unicode__(self):
        return self.nombre
class ReservadoMediante(models.Model):
    nombre = models.CharField(max_length=30)
    def __unicode__(self):
        return self.nombre
class Reserva(models.Model):
    paquete = models.ForeignKey(Paquete)
    precio = models.FloatField(blank=True)
    pre_pago = models.FloatField(blank=True)
    # Porcentaje
    fecha_viaje = models.DateField()
    cantidad_pasajeros = models.IntegerField()
    pasajeros = models.ManyToManyField(Pasajero, blank=True)
    ip = models.GenericIPAddressField(null=True,blank=True)
    reservado_mediante = models.ForeignKey(ReservadoMediante)
    cliente = models.ForeignKey(Cliente)
    empresa = models.ForeignKey(Empresa)
    estado = models.ForeignKey(EstadoReserva)
    creado = models.DateTimeField(auto_now_add=True, editable=False)
    editado = models.DateTimeField(auto_now=True, editable=False)
    # Detalles de pago
    monto_pagado = models.FloatField(default=0)
    fecha_pago = models.DateTimeField(null=True)
    code = models.CharField(max_length=32,editable=False)
    tx = models.CharField(max_length=64, blank=True)
    forma_pago = models.ForeignKey(FormaPago)
    estado_pago = models.ForeignKey(EstadoPago)
    def save(self, *args, **kwargs):
        self.empresa = self.paquete.empresa
        self.pre_pago = self.paquete.pre_pago
        self.precio = self.paquete.precio
        super(Reserva,self).save(*args,**kwargs)
    def __unicode__(self):
        return "Una reserva de "+self.email
    def precioTotal(self):
        return int(self.cantidad_pasajeros) * self.precio
    def precioTotalPrePago(self):
        return int(self.cantidad_pasajeros) * self.pre_pago
class ComentarioReserva(models.Model):
    titulo = models.CharField(max_length=60)
    comentario = models.TextField()
    empresa = models.ForeignKey(Empresa)
    creado = models.DateTimeField(auto_now_add=True, editable=False)
    estado = models.BooleanField(default=True)
    def __unicode__(self):
        return "Comentario"