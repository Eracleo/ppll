from django.db import models

# Create your models here.
class Persona(models.Model):
    nombre = models.CharField(max_length=30)
    apellidos = models.CharField(max_length=60)
    doc_tipo = models.CharField(max_length=10)
    doc_nro = models.CharField(max_length=10)
    def __unicode__(self):
        return self.nombre