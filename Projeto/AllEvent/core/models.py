# Em core/models.py
from django.db import models

class Evento(models.Model):
    nome = models.CharField(max_length=200)
    local = models.CharField(max_length=200)
    data = models.DateTimeField('data do evento')
    descricao = models.TextField(blank=True)

    imagem = models.ImageField(upload_to='eventos_imagens/', null=True, blank=True)
    def __str__(self):
        return self.nome