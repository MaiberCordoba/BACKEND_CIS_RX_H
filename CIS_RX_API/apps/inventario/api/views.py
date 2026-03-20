from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Sum
from ..models import Producto, MovimientoInventario, UnidadMedida
from .serializers import ProductoSerializer, MovimientoSerializer, UnidadMedidaSerializer

class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer

class UnidadMedidaViewSet(viewsets.ModelViewSet):
    queryset = UnidadMedida.objects.all()
    serializer_class = UnidadMedidaSerializer

class MovimientoViewSet(viewsets.ModelViewSet):
    queryset = MovimientoInventario.objects.all()
    serializer_class = MovimientoSerializer

# VISTA EXCLUSIVA PARA REPORTES
class ReporteInventarioViewSet(viewsets.ViewSet):
    
    @action(detail=False, methods=['get'])
    def financiero(self, request):
        f_inicio = request.query_params.get('f_inicio')
        f_fin = request.query_params.get('f_fin')
        
        qs = MovimientoInventario.objects.filter(fecha__date__range=[f_inicio, f_fin])
        
        # Lo que se pagó al comprar
        total_compras = qs.filter(tipo='Entrada').aggregate(Sum('precio_total'))['precio_total__sum'] or 0
        
        # Lo que "valió" lo que se gastó o salió
        total_consumo = qs.filter(tipo='Salida').aggregate(Sum('precio_total'))['precio_total__sum'] or 0
        
        return Response({
            'periodo': {'inicio': f_inicio, 'fin': f_fin},
            'inversion_en_compras': total_compras, # Dinero que salió del banco para stock
            'valor_del_consumo': total_consumo,     # Dinero que "valió" lo que se usó en el mes
        })