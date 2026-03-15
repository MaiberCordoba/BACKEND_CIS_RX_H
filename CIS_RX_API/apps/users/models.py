from django.contrib.auth.models import AbstractUser
from django.db import models

class Usuario(AbstractUser):
    ROLES = (
        ('Facturador', 'Facturador'),
        ('Jefe', 'Jefe/Responsable'),
    )
    rol = models.CharField(max_length=20, choices=ROLES, default='Facturador')
    telefono = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(unique=True)
    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.rol})"