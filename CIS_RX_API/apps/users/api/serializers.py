from rest_framework import serializers
from ..models import Usuario  # Importamos el modelo desde el nivel superior

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = [
            'id', 
            'username', 
            'email', 
            'first_name', 
            'last_name', 
            'rol', 
            'telefono', 
            'is_active'
        ]
        read_only_fields = ['id']

class UsuarioCreateSerializer(serializers.ModelSerializer):
    """Serializer especial para crear usuarios (maneja la contraseña)"""
    class Meta:
        model = Usuario
        fields = ['username', 'email', 'password', 'first_name', 'last_name', 'rol', 'telefono']
        extra_kwargs = {
            'password': {'write_only': True} 
        }

    def create(self, validated_data):
        # Usamos el método create_user de Django para que la contraseña se encripte
        user = Usuario.objects.create_user(**validated_data)
        return user