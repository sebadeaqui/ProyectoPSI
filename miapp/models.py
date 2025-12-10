from django.db import models

class Practica(models.Model):
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100)
    # image_url puede ser opcional
    image_url = models.URLField(max_length=500, blank=True, null=True)
    
    def __str__(self):
        return self.username
    
    # NUEVO MODELO PARA CANCIONES
class Cancion(models.Model):
    titulo = models.CharField(max_length=200)
    artista = models.CharField(max_length=200)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    usuario = models.ForeignKey(Practica, on_delete=models.CASCADE, related_name='canciones')
    
    def __str__(self):
        return f"{self.titulo} - {self.artista}"