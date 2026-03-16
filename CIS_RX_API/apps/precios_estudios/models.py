from django.db import models

class Estudio(models.Model):
    codigo = models.CharField(max_length=20, unique=True)
    nombre = models.CharField(max_length=255)
    
    precio_particular = models.DecimalField(max_digits=12, decimal_places=2)
    precio_medicos = models.DecimalField(max_digits=12, decimal_places=2)
    precio_previred = models.DecimalField(max_digits=12, decimal_places=2)
    precio_plan_paciente_frecuente = models.DecimalField(max_digits=12, decimal_places=2)

    class Meta:
        db_table = 'estudios_catalogo'
        verbose_name = 'Estudio'
        verbose_name_plural = 'Estudios'

    def __str__(self):
        return f"{self.codigo} - {self.nombre}"