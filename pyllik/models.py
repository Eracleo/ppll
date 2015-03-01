from django.db import models
from django.contrib.auth.models import User
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
    pais = models.ForeignKey(Pais)
    creado = models.DateField(auto_now_add=True, editable=False)
    editado = models.DateTimeField(auto_now=True, editable=False)
    email = models.EmailField(max_length=60,blank=True)
    cod_telefono = models.CharField(max_length=5, blank=True)
    telefono = models.CharField(max_length=50, blank=True)
    def __unicode__(self):
        return self.nombre
class Paquete(models.Model):
    # sku = identificador del Paquete
    nombre = models.CharField(max_length=20)
    precio = models.FloatField(default=0)
    porcentaje = models.FloatField(default=100)
    pre_pago = models.FloatField(default=0) # Adelanto de pago
    descripcion = models.TextField(blank=True)
    user = models.ForeignKey(User)
    creado = models.DateField(auto_now_add=True, editable=False)
    link = models.URLField(max_length=120, blank=True)
    estado = models.BooleanField(default=True)
    def __unicode__(self):
        return self.nombre
class Reserva(models.Model):
    paquete = models.ForeignKey(Paquete)
    cantidad_personas = models.IntegerField(default=0)
    fecha_viaje = models.DateField()
    precio = models.FloatField(default=0)
    modo_pago = models.CharField(max_length=2, choices=MODO_PAGO, default='pa')
    # llego_de = (recomendado, web, web_reserva, oficina)
    # nro re referencia al documento(id_paypal,nro_boleta,nro_factura)
    user = models.ForeignKey(User)
    creado = models.DateTimeField(auto_now_add=True, editable=False)
    pago_estado = models.CharField(max_length=2, choices=PAGO_ESTADO, default='re')
    def save(self, *args, **kwargs):
        self.user = self.paquete.user
        super(Reserva,self).save(*args,**kwargs)
    def __unicode__(self):
        return "Una reserva"
class ReservaDetalle(models.Model):
    reserva = models.ForeignKey(Reserva)
    persona = models.ForeignKey(Persona)
    creado = models.DateTimeField(auto_now_add=True, editable=False)
    def __unicode__(self):
        return "Detalle Reserva"
class Rubro(models.Model):
    nombre = models.CharField(max_length=120)
    def __unicode__(self):
        return self.nombre
class Empresa(models.Model):
    razon_social = models.CharField(max_length=100)
    direccion = models.CharField(max_length=120)
    ruc = models.CharField(max_length=11)
    web = models.URLField(max_length=64, blank=True)
    paypal_email = models.EmailField(max_length=100)
    paypal_code = models.CharField(max_length=50)
    nro_paquetes = models.IntegerField(default=1)
    user = models.ForeignKey(User)
    def __unicode__(self):
        return self.razon_social