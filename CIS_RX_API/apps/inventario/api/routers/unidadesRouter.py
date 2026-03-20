from rest_framework.routers import DefaultRouter
from ..views import UnidadMedidaViewSet

unidadesRouter = DefaultRouter()
unidadesRouter.register(prefix='unidades', viewset=UnidadMedidaViewSet, basename='unidades')