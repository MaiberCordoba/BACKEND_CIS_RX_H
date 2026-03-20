from django.db import models

class UnidadMedida(models.Model):
    GRUPOS = (
        ('Líquidos', 'Líquidos (Base: ml)'),
        ('Pesos', 'Pesos (Base: g)'),
        ('Unidades', 'Unidades (Base: Unidad)'),
    )
    nombre = models.CharField(max_length=50) 
    grupo = models.CharField(max_length=20, choices=GRUPOS)
    factor_conversion = models.DecimalField(max_digits=12, decimal_places=2)

    class Meta:
        db_table = 'inv_unidades_medida'

    def __str__(self):
        return f"{self.nombre} ({self.grupo})"

class Producto(models.Model):
    CATEGORIAS = (('Insumo', 'Insumo'), ('Residuo', 'Residuo'))
    nombre = models.CharField(max_length=100)
    categoria = models.CharField(max_length=20, choices=CATEGORIAS)
    
    # El producto nace amarrado a una unidad (y por ende a un grupo)
    unidad_medida = models.ForeignKey(UnidadMedida, on_delete=models.PROTECT, related_name='productos_base')
    stock_actual = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    
    costo_unitario_base = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    class Meta:
        db_table = 'inv_productos'

    def __str__(self):
        return self.nombre

class MovimientoInventario(models.Model):
    TIPOS = (('Entrada', 'Entrada'), ('Salida', 'Salida'))
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name='movimientos')
    tipo = models.CharField(max_length=10, choices=TIPOS)
    unidad_movimiento = models.ForeignKey(UnidadMedida, on_delete=models.PROTECT)
    cantidad = models.DecimalField(max_digits=12, decimal_places=2)
    precio_total = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    fecha = models.DateTimeField(auto_now_add=True)
    foto_evidencia = models.ImageField(upload_to='inventario/evidencias/', null=True, blank=True)
    observaciones = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'inv_movimientos'