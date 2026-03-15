from rest_framework import serializers
from ...models import DetalleDenominacion

class DetalleDenominacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetalleDenominacion
        fields = ['denominacion', 'cantidad', 'subtotal']
        read_only_fields = ['subtotal']


   