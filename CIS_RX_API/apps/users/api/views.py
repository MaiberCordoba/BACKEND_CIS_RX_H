from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from ..models import Usuario
from .serializers import UsuarioSerializer, UsuarioCreateSerializer

class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    
    def get_serializer_class(self):
        if self.action == 'create':
            return UsuarioCreateSerializer
        return UsuarioSerializer

    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'], url_path='me')
    def me(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)
    
    def partial_update(self, request, *args, **kwargs):
        user = self.get_object()
        data = request.data.copy()  # Copia mutable
        if 'password' in data:
            user.set_password(data['password'])
            user.save()
            del data['password']  # Eliminar para que no se envíe al serializador
        # Crear serializador con los datos modificados
        serializer = self.get_serializer(user, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)