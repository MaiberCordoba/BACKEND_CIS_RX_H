from rest_framework import serializers
from ...models import Arqueo, DetalleDenominacion, TransferenciaDetalle
from ..seriliazers.detalleDenominacionSerializer import DetalleDenominacionSerializer
from ..seriliazers.trasferenciaDetalleSerialiazer import TransferenciaDetalleSerializer 
from django.db import transaction
import datetime # Importante para la limpieza final

class ArqueoSerializer(serializers.ModelSerializer):
    detalles = DetalleDenominacionSerializer(many=True)
    transferencias = TransferenciaDetalleSerializer(many=True, required=False)

    fecha = serializers.DateField(required=False)
    hora = serializers.TimeField(required=False)

    class Meta:
        model = Arqueo
        fields = '__all__'
        read_only_fields = ['total_transferencias', 'total_efectivo_fisico', 'gran_total_real', 'diferencia']

    def create(self, validated_data):
        detalles_data = validated_data.pop('detalles')
        transferencias_data = validated_data.pop('transferencias', []) 

        # calculo efectivo 
        total_fisico = 0
        for item in detalles_data:
            subtotal_item = item['denominacion'] * item['cantidad']
            item['subtotal'] = subtotal_item 
            total_fisico += subtotal_item

        # calculo trasferencias
        total_trans = sum(t.get('valor', 0) for t in transferencias_data)

        # total
        gran_total = total_fisico + total_trans
        total_facturado = validated_data.get('total_facturado', 0)
        
        validated_data['total_efectivo_fisico'] = total_fisico
        validated_data['total_transferencias'] = total_trans
        validated_data['gran_total_real'] = gran_total
        validated_data['diferencia'] = gran_total - total_facturado

        with transaction.atomic():
            arqueo = Arqueo.objects.create(**validated_data)
            
            for d in detalles_data:
                DetalleDenominacion.objects.create(arqueo=arqueo, **d)
            
            for t in transferencias_data:
                TransferenciaDetalle.objects.create(arqueo=arqueo, **t)

        # funciones para evitar error en formato de fechas y hora 
        if isinstance(arqueo.fecha, datetime.datetime):
            arqueo.fecha = arqueo.fecha.date()
        if isinstance(arqueo.hora, datetime.datetime):
            arqueo.hora = arqueo.hora.time()

        return arqueo