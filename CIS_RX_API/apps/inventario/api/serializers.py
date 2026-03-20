from rest_framework import serializers
from ..models import Producto, MovimientoInventario, UnidadMedida
from django.db import transaction

class UnidadMedidaSerializer(serializers.ModelSerializer):
    class Meta:
        model = UnidadMedida
        fields = '__all__'

class ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = '__all__'

class MovimientoSerializer(serializers.ModelSerializer):
    class Meta:
        model = MovimientoInventario
        fields = '__all__'

    def create(self, validated_data):
        producto = validated_data['producto']
        tipo = validated_data['tipo']
        unidad = validated_data['unidad_movimiento']
        cantidad_reg = validated_data['cantidad']
        
        cantidad_base = cantidad_reg * unidad.factor_conversion

        with transaction.atomic():
            if tipo == 'Entrada':
                precio_pagado = validated_data.get('precio_total', 0)
                
                # CALCULO DE COSTO PROMEDIO PONDERADO
                valor_actual_stock = producto.stock_actual * producto.costo_unitario_base
                nuevo_total_valor = valor_actual_stock + precio_pagado
                nuevo_total_cantidad = producto.stock_actual + cantidad_base
                
                if nuevo_total_cantidad > 0:
                    producto.costo_unitario_base = nuevo_total_valor / nuevo_total_cantidad
                
                producto.stock_actual += cantidad_base

            else:
                # El valor de la salida es la cantidad que sale por el costo unitario que tiene el producto
                costo_salida = cantidad_base * producto.costo_unitario_base
                validated_data['precio_total'] = costo_salida # SE ASIGNA AUTOMÁTICAMENTE
                
                # Validación de stock
                if producto.stock_actual < cantidad_base:
                    raise serializers.ValidationError("Stock insuficiente.")
                
                producto.stock_actual -= cantidad_base

            producto.save()
            return super().create(validated_data)