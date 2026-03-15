from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from ..models import Usuario
from .serializers import UsuarioSerializer, UsuarioCreateSerializer

class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    
    # funcion para usar el serializador que encripta la contraseña al crear usuarios
    def get_serializer_class(self):
        if self.action == 'create':
            return UsuarioCreateSerializer
        return UsuarioSerializer

    permission_classes = [IsAuthenticated]