from rest_framework.routers import DefaultRouter
from ..views import ReporteInventarioViewSet

reportesRouter = DefaultRouter()
reportesRouter.register(prefix='reportes', viewset=ReporteInventarioViewSet, basename='reportes')