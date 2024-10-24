from django.db import models

# models.py de tu app 'canasta'

class CanastaBasica(models.Model):
    descripcion = models.CharField(max_length=255)
    categoria = models.CharField(max_length=255)
    cantidad = models.IntegerField()



    def __str__(self):
        return self.descripcion