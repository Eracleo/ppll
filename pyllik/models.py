# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from thumbs import ImageWithThumbsField
import uuid,random
def Abreviatura(razon_social):
    abreviatura = razon_social[:3]
    abreviatura += random.choice("abcdefghijklm")
    return abreviatura.upper()
class Pais(models.Model):
    nombre = models.CharField(max_length=30)
    def __unicode__(self):
        return self.nombre
class Rubro(models.Model):
    nombre = models.CharField(max_length=120)
    def __unicode__(self):
        return self.nombre
class Empresa(models.Model):
    rubro = models.ForeignKey(Rubro,default=1)
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
    abreviatura = models.CharField(max_length=4,unique=True,editable=False)
    paypal_email = models.EmailField(max_length=100,help_text="E-mail relacionado con paypal")
    paypal_at = models.CharField(max_length=64,help_text="Código de identicacion en paypal") # IdentityToken
    code = models.CharField(max_length=32,default=uuid.uuid1().hex,editable=False)
    creado = models.DateField(auto_now_add=True, editable=False)
    editado = models.DateTimeField(auto_now=True, editable=False)
    def save(self, *args, **kwargs):
        if len(self.abreviatura) < 2:
            self.abreviatura = Abreviatura(self.razon_social)
        super(Empresa,self).save(*args,**kwargs)
    def __unicode__(self):
        return self.razon_social
class TipoDocumento(models.Model):
    nombre = models.CharField(max_length=30)
    def __unicode__(self):
        return self.nombre
class Trabajador(models.Model):
    user = models.OneToOneField(User,primary_key=True)
    doc_nro = models.CharField(max_length=10,verbose_name="D. I.")
    direccion = models.CharField(max_length=60)
    email = models.CharField(max_length=60)
    telefono = models.CharField(max_length=60)
    celular = models.CharField(max_length=60)
    observaciones = models.TextField(blank=True)
    empresa = models.ForeignKey(Empresa)
    foto = ImageWithThumbsField(upload_to='logos_empresa', sizes=((150,250),))
    def __unicode__(self):
        return str(self.user)
class TrabajadorContacto(models.Model):
    nombre = models.CharField(max_length=30)
    apellidos = models.CharField(max_length=50)
    direccion = models.CharField(max_length=100)
    telefono = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    trabajador = models.ForeignKey(Trabajador)
    empresa = models.ForeignKey(Empresa)
    def __unicode__(self):
        return self.nombre
class TipoPasajero(models.Model):
    nombre = models.CharField(max_length=30)
    def __unicode__(self):
        return self.nombre
class Pasajero(models.Model):
    nombre = models.CharField(max_length=30)
    apellidos = models.CharField(max_length=60)
    doc_tipo = models.ForeignKey(TipoDocumento)
    doc_nro = models.CharField(max_length=10)
    email = models.EmailField(max_length=60,blank=True)
    telefono = models.CharField(max_length=50, blank=True)
    pais = models.ForeignKey(Pais,null=True, blank=True)
    tipo = models.ForeignKey(TipoPasajero,default=4,blank=True)
    observacion = models.TextField(blank=True)
    empresa = models.ForeignKey(Empresa,null=True, blank=True,editable=False)
    creado = models.DateField(auto_now_add=True, editable=False)
    editado = models.DateTimeField(auto_now=True, editable=False)
    def __unicode__(self):
        return self.nombre
BOOL_CHOICES = ((True, 'Habitilido'), (False, 'Deshabilitado'))
def sku(last_sku):
    sku = last_sku[:4]
    sku += str(int(last_sku[4:]) + 1).zfill(3)
    return sku;
class Paquete(models.Model):
    sku = models.CharField(max_length=7,unique=True,editable=False)
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
    def save(self, *args, **kwargs):
        if len(self.sku) < 7:
            empresa_id = self.empresa.id
            ultimo = Paquete.objects.filter(empresa_id = empresa_id).latest('id')
            self.sku = sku(ultimo.sku)
        super(Paquete,self).save(*args,**kwargs)
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
    tipo = models.ForeignKey(TipoCliente, default=1)
    observacion = models.TextField(blank=True)
    empresa = models.ForeignKey(Empresa,editable=False)
    creado = models.DateField(auto_now_add=True, editable=False)
    editado = models.DateTimeField(auto_now=True, editable=False)
    def __unicode__(self):
        return self.email
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
    reservado_mediante = models.ForeignKey(ReservadoMediante,default=1)
    cliente = models.ForeignKey(Cliente)
    estado = models.ForeignKey(EstadoReserva,verbose_name="Estado Reserva")
    estado_pago = models.ForeignKey(EstadoPago)
    code = models.CharField(max_length=32,default=uuid.uuid1().hex,editable=False)
    nuevo = models.BooleanField(default=False)
    creado = models.DateTimeField(auto_now_add=True, editable=False)
    editado = models.DateTimeField(auto_now=True, editable=False)
    empresa = models.ForeignKey(Empresa)
    def save(self, *args, **kwargs):
    # Esto esta mal
        self.empresa = self.paquete.empresa
        self.pre_pago = self.paquete.pre_pago
        self.precio = self.paquete.precio
        super(Reserva,self).save(*args,**kwargs)
    def __unicode__(self):
        return "Una reserva de "+str(self)
    def precioTotal(self):
        return int(self.cantidad_pasajeros) * self.precio
    def precioTotalPrePago(self):
        return int(self.cantidad_pasajeros) * self.pre_pago
class ComentarioReserva(models.Model):
    comentario = models.TextField()
    empresa = models.ForeignKey(Empresa)
    reserva = models.ForeignKey(Reserva)
    creado = models.DateTimeField(auto_now_add=True, editable=False)
    estado = models.BooleanField(default=True)
    def __unicode__(self):
        return "Comentario"
PAGO_CHOICES = ((True, 'ACEPTADO'), (False, 'DEVUELTO'))
class Pago(models.Model):
    reserva = models.ForeignKey(Reserva)
    precio = models.FloatField(default=0,verbose_name="Monto pagado")
    creado = models.DateTimeField(null=True,verbose_name="Fecha de pago")
    forma_pago = models.ForeignKey(FormaPago)
    estado = models.BooleanField(default=True,choices=PAGO_CHOICES)
    ip = models.GenericIPAddressField(null=True,blank=True)
    tx = models.CharField(max_length=64, blank=True)
    verificado = models.BooleanField(default=False)
    empresa = models.ForeignKey(Empresa)
    nuevo = models.BooleanField(default=False)
    def save(self, *args, **kwargs):
        self.empresa = self.reserva.empresa
        super(Pago,self).save(*args,**kwargs)