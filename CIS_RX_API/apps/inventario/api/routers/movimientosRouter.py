from rest_framework.routers import DefaultRouter
from ..views import MovimientoViewSet 

movimientosRouter = DefaultRouter()
movimientosRouter.register(prefix= 'movimientos', viewset=MovimientoViewSet, basename='movimientos')