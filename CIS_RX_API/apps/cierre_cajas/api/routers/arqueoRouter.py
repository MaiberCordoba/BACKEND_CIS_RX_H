from rest_framework.routers import DefaultRouter
from apps.cierre_cajas.api.views.ArqueoView import ArqueoModelViewSet 

arqueoRouter = DefaultRouter()
arqueoRouter.register(prefix= 'arqueo', viewset= ArqueoModelViewSet, basename='arqueo')