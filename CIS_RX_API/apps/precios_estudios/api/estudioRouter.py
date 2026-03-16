from rest_framework.routers import DefaultRouter
from apps.precios_estudios.api.estudioView import EstudioModelViewSet 

estudioRouter = DefaultRouter()
estudioRouter.register(prefix= 'estudio', viewset= EstudioModelViewSet, basename='estudio')