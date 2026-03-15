from rest_framework import serializers
from ...models import TransferenciaDetalle

class TransferenciaDetalleSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransferenciaDetalle
        fields = ['valor', 'numero_factura']

