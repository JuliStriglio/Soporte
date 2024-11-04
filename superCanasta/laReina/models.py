from django.db import models

class Producto(models.Model):
    descripcion = models.CharField(max_length=255)
    supermercado = models.CharField(max_length=255)
    categoria = models.CharField(max_length=255)
    imagen = models.URLField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_act =  models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"{self.descripcion} - ${self.precio}"