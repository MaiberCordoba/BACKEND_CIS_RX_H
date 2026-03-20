from rest_framework.routers import DefaultRouter
from ..views import ProductoViewSet  

inventarioRouter = DefaultRouter()
inventarioRouter.register(prefix= 'productos', viewset= ProductoViewSet, basename='productos')