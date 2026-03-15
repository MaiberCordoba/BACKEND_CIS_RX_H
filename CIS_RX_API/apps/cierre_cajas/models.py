from django.db import models
from django.utils.timezone import localdate , localtime
from ..users.models import Usuario

class Arqueo(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.SET_NULL,null=True, db_column='usuario_id')
    responsable_nombre = models.CharField(max_length=100)
    fecha = models.DateField(default=localdate)
    hora = models.TimeField(default=localtime)
    
    base_efectivo = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total_facturado = models.DecimalField(max_digits=12, decimal_places=2)
    
    total_transferencias = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total_efectivo_fisico = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    gran_total_real = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    diferencia = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    
    observaciones = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'finanza_arqueos' 

class DetalleDenominacion(models.Model):
    arqueo = models.ForeignKey(Arqueo, on_delete=models.SET_NULL, null=True, related_name='detalles', db_column='arqueo_id')
    denominacion = models.IntegerField()
    cantidad = models.IntegerField(default=0)
    subtotal = models.DecimalField(max_digits=12, decimal_places=2)

    class Meta:
        db_table = 'finanza_detalles_efectivo'

class TransferenciaDetalle(models.Model):
    arqueo = models.ForeignKey(Arqueo, on_delete=models.SET_NULL, null=True, related_name='transferencias', db_column='arqueo_id')
    valor = models.DecimalField(max_digits=12, decimal_places=2)
    numero_factura = models.CharField(max_length=50)

    class Meta:
        db_table = 'finanza_detalles_transferencias'