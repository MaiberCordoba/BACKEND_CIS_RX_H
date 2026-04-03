"""
URL configuration for CIS_RX_API project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path , include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from apps.cierre_cajas.api.routers.arqueoRouter import arqueoRouter
from apps.precios_estudios.api.estudioRouter import estudioRouter
from apps.inventario.api.routers.productosRouter import inventarioRouter
from apps.inventario.api.routers.movimientosRouter import movimientosRouter
from apps.inventario.api.routers.unidadesRouter import unidadesRouter 
from apps.inventario.api.routers.reportesRouter import reportesRouter

from apps.precios_estudios.api.cargaMasivaView import CargaMasivaEstudiosView

urlpatterns = [
    path('admin/', admin.site.urls),
    
    #login
    path('api/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    #modulos 
    path('api/', include('apps.users.api.routers')),
    path('api/', include(arqueoRouter.urls)),
    path('api/', include(estudioRouter.urls)),
    path('api/', include(inventarioRouter.urls)),
    path('api/', include(movimientosRouter.urls)),
    path('api/', include(unidadesRouter.urls)),
    path('api/', include(reportesRouter.urls)),
    
    
    #carga masiva estudios
    
     path('api/estudios/carga-masiva/', CargaMasivaEstudiosView.as_view(), name='carga_masiva_estudios'),
]
