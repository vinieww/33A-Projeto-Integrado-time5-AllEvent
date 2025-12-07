from django.db import models
from django.contrib.auth.models import User 

class Categoria(models.Model):
    nome = models.CharField(max_length=100)

    def __str__(self):
        return self.nome

class Evento(models.Model):
    nome = models.CharField(max_length=200)
    local = models.CharField(max_length=200)
    data = models.DateTimeField('data do evento')
    descricao = models.TextField(blank=True)
    imagem = models.ImageField(upload_to='eventos_imagens/', null=True, blank=True)
    
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True, blank=True)

    favoritos = models.ManyToManyField(User, related_name='eventos_favoritos', blank=True)

    def __str__(self):
        return self.nome